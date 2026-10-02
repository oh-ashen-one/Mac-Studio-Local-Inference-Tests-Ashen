"""Resolve standard or explicitly selected additional model locks without loading weights."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def resolve_model(identifier,lock_path=None):
    lock_path=Path(lock_path) if lock_path else ROOT/'config/models.lock.json'
    if not lock_path.is_absolute():lock_path=ROOT/lock_path
    spec=next(m for m in json.loads(lock_path.read_text())['models'] if m['id']==identifier)
    storage=spec.get('storage')
    if storage:
        relative=Path(storage['relative_path'])
        if relative.is_absolute() or '..' in relative.parts:raise ValueError('Unsupported model storage')
        if storage['kind']=='huggingface_cache':
            directory=Path.home()/relative
            if not directory.is_relative_to(Path.home()/'.cache/huggingface/hub'):raise ValueError('Model path outside declared cache')
        elif storage['kind']=='repository_models':directory=ROOT/'models'/relative
        else:raise ValueError('Unsupported model storage')
    else:directory=ROOT/'models'/identifier
    if (directory/'config.json').exists():
        config=json.loads((directory/'config.json').read_text())
        if config.get('model_file'):raise ValueError('Custom model code requires separate review; refusing automatic execution')
    return spec,directory,lock_path
