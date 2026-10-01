"""Explicit independent text runtime; importing this module never loads weights."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def runtime_lock(backend):
    return ROOT/('config/requirements-mlx-vlm.lock' if backend=='mlx-vlm' else 'requirements-macos-arm64.lock')

def load_text(folder,backend='mlx-lm'):
    folder=Path(folder)
    config=json.loads((folder/'config.json').read_text())
    if config.get('model_file'):
        raise ValueError('Custom model code is not permitted')
    if backend=='mlx-lm':
        from mlx_lm import load
        return load(str(folder),return_config=True)
    if backend!='mlx-vlm':raise ValueError('Unknown independent runtime')
    import mlx.nn as nn
    from mlx_vlm.utils import load_model
    from mlx_lm.utils import load_tokenizer
    # Use the upstream architecture-specific sanitizer, including its MTP and
    # MXFP4 handling. Retain only the language backbone for this text-only test.
    full=load_model(folder,lazy=False,strict=True,trust_remote_code=False,local_files_only=True)
    class TextBackbone(nn.Module):
        def __init__(self,inner):
            super().__init__();self.inner=inner
        def __call__(self,inputs,cache=None,**kwargs):
            return self.inner(inputs,cache=cache,**kwargs).logits
        @property
        def layers(self):return self.inner.layers
        def make_cache(self):return self.inner.make_cache()
    model=TextBackbone(full.language_model)
    tokenizer=load_tokenizer(folder,tokenizer_config_extra={'local_files_only':True,'trust_remote_code':False},eos_token_ids=config.get('eos_token_id'))
    return model,tokenizer,config
