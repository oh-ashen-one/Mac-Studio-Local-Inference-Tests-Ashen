"""Explicit independent text runtime; importing this module never loads weights."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def runtime_lock(backend):
    return ROOT/('config/requirements-mlx-vlm.lock' if backend=='mlx-vlm' else 'requirements-macos-arm64.lock')

def exclude_mimo_draft(weights):
    # This pinned package includes three optional MTP draft layers. Base-model
    # decoding does not use them. Retain strict checking for EVERY other key.
    draft=[k for k in weights if k.startswith(('model.mtp.','language_model.model.mtp.'))]
    if len(draft)!=42:raise ValueError('Unexpected MiMo draft layout; expected exactly 42 MTP tensors')
    return {k:v for k,v in weights.items() if k not in draft}

def tokenizer_options(folder,config,mimo_xml_tools=False):
    options={'local_files_only':True,'trust_remote_code':False}
    if mimo_xml_tools:
        template=(Path(folder)/'chat_template.jinja').read_text()
        if config.get('model_type')!='mimo_v2' or '<tool_call><function=' not in template or '<parameter=' not in template:
            raise ValueError('Reviewed XML override applies only to the declared MiMo grammar')
        options['tool_parser_type']='qwen3_coder'
    return options

def load_text(folder,backend='mlx-lm',mimo_xml_tools=False):
    folder=Path(folder)
    config=json.loads((folder/'config.json').read_text())
    if config.get('model_file'):
        raise ValueError('Custom model code is not permitted')
    options=tokenizer_options(folder,config,mimo_xml_tools)
    if backend=='mlx-lm':
        from mlx_lm import load
        return load(str(folder),return_config=True)
    if backend!='mlx-vlm':raise ValueError('Unknown independent runtime')
    import mlx.nn as nn
    from mlx_vlm.utils import load_model
    from mlx_lm.utils import load_tokenizer
    # Use the upstream architecture-specific sanitizer, including its MTP and
    # MXFP4 handling. Retain only the language backbone for this text-only test.
    original_sanitize=None
    if config.get('model_type')=='mimo_v2':
        from mlx_vlm.models.mimo_v2 import Model
        original_sanitize=Model.sanitize
        def sanitize(self,weights):return original_sanitize(self,exclude_mimo_draft(weights))
        Model.sanitize=sanitize
    try:
        full=load_model(folder,lazy=False,strict=True,trust_remote_code=False,local_files_only=True)
    finally:
        if original_sanitize is not None:Model.sanitize=original_sanitize
    class TextBackbone(nn.Module):
        def __init__(self,inner):
            super().__init__();self.inner=inner
        def __call__(self,inputs,cache=None,**kwargs):
            return self.inner(inputs,cache=cache,**kwargs).logits
        @property
        def layers(self):return self.inner.layers
        def make_cache(self):return self.inner.make_cache()
    model=TextBackbone(full.language_model)
    tokenizer=load_tokenizer(folder,tokenizer_config_extra=options,eos_token_ids=config.get('eos_token_id'))
    return model,tokenizer,config
