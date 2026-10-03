"""Admission gate for a separately pinned extension; no model-runtime imports."""
import hashlib,json
from pathlib import Path

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()

def require_qualified(root,plan,specs):
    root=Path(root)
    for spec in specs.values():
        if not spec.get('extension') or not spec.get('execution_ready'):
            raise RuntimeError('Extension is not explicitly qualified: '+spec['id'])
        receipt=spec.get('qualification_receipt')
        if not receipt:raise RuntimeError('Missing extension qualification receipt')
        q=json.loads((root/receipt).read_text())
        for key in ['artifact_hashes_verified','runtime_load_passed','exact_token_count_passed','task_interface_passed','long_context_metadata_passed']:
            if q.get(key) is not True:raise RuntimeError('Unpassed qualification gate: '+key)
        if q.get('model_revision')!=spec['revision']:raise RuntimeError('Qualification revision mismatch')
        native=spec['native_runtime']
        if digest(root/native['lock'])!=q.get('runtime_lock_sha256'):raise RuntimeError('Qualified runtime lock changed')
        if digest(root/native['server'])!=q.get('native_server_sha256'):raise RuntimeError('Qualified runtime binary changed')
        # The receipt must refer to exactly the admitted model artifact list.
        if q.get('model_files')!=spec['files']:raise RuntimeError('Qualified artifact list changed')
