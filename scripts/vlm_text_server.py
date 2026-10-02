"""MLX-LM's loopback server with the pinned MLX-VLM text loader only.

The parent campaign owns the GPU slot, telemetry, deadline and shutdown.
No provider software, adapter, draft model, remote code or network model fetch.
"""
import os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from text_runtime import load_text

def main():
    os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1')
    mimo_xml_tools='--mimo-xml-tools' in sys.argv
    if mimo_xml_tools:sys.argv.remove('--mimo-xml-tools')
    if '--host' not in sys.argv or sys.argv[sys.argv.index('--host')+1]!='127.0.0.1':
        raise ValueError('Only explicitly selected loopback serving is permitted')
    expected=Path(sys.argv[sys.argv.index('--model')+1]).resolve()
    import mlx.core as mx,psutil
    import mlx_lm.server as server
    mx.set_memory_limit(int(psutil.virtual_memory().total*.82))
    def load(model_path,adapter_path=None,tokenizer_config=None,**kwargs):
        if Path(model_path).resolve()!=expected or adapter_path or kwargs:
            raise ValueError('Only the pinned base model is permitted')
        model,tokenizer,_=load_text(expected,'mlx-vlm',mimo_xml_tools=mimo_xml_tools)
        return model,tokenizer
    server.load=load
    server.main()

if __name__=='__main__':main()
