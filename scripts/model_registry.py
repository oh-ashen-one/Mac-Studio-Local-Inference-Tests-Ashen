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
        if storage['kind']!='huggingface_cache' or relative.is_absolute() or '..' in relative.parts:raise ValueError('Unsupported model storage')
        directory=Path.home()/relative
        if not directory.is_relative_to(Path.home()/'.cache/huggingface/hub'):raise ValueError('Model path outside declared cache')
    else:directory=ROOT/'models'/identifier
    return spec,directory,lock_path
