"""Metadata-only admission checks; never reads tensor contents or changes downloads."""
import os
from pathlib import Path

OMITTED = 'omitted_by_owner_scope'

def pending_disposition(job, result_exists):
    # Existing evidence always wins, even if an amendment accidentally includes it.
    return job.get('disposition') if not result_exists and job.get('disposition') == OMITTED else None

def download_snapshot(roots, limit=20000):
    entries = []; blockers = []; count = 0
    for root in roots:
        root = Path(root)
        if not root.exists():
            continue
        def onerror(error):
            blockers.append(type(error).__name__)
        for directory, dirs, files in os.walk(root, onerror=onerror, followlinks=False):
            dirs[:] = sorted(d for d in dirs if d not in {'.git', '.venv', 'xet', 'node_modules'})
            for name in sorted(dirs + files):
                count += 1
                if count > limit:
                    return tuple(entries), ['metadata_scan_limit']
                p = Path(directory) / name
                if name.startswith('.local-staging') or name.endswith(('.part', '.incomplete', '.download')):
                    blockers.append(str(p.relative_to(root)))
                if name in files:
                    try:
                        st = p.stat(); entries.append((str(p), st.st_size, st.st_mtime_ns))
                    except OSError as error:
                        blockers.append(type(error).__name__)
    return tuple(entries), blockers

def extension_pending(root, plan):
    # A pending declaration prevents a misleading whole-study completion.
    name = plan.get('required_extension')
    if not name:
        return False
    import json
    extension = json.loads((root / name).read_text())
    return extension.get('status') != 'complete_with_evidence'

RESOURCE = 'unsupported_resource'
DEFERRED = 'deferred_resource_review'
BUDGET = 'unsupported_request_budget'
BUDGET_CASES = 'unsupported_request_budget_cases'

def reviewed_disposition(root, job, result):
    """Require concrete preserved evidence; never score a partial resource failure."""
    disposition=job.get('disposition')
    if disposition not in (RESOURCE,DEFERRED,BUDGET,BUDGET_CASES):return None
    import json
    evidence=job.get('disposition_evidence')
    if not evidence:raise RuntimeError('Missing resource review evidence')
    note=json.loads((Path(root)/evidence).read_text())
    if disposition==BUDGET_CASES:
        from retrieval_continuation import review_all_budget_cases
        return review_all_budget_cases(root,job,note,BUDGET_CASES)
    if disposition==BUDGET:
        import hashlib
        if job.get('kind')!='repo' or not result or result.get('kind')!='repo_task':
            raise RuntimeError('Repository budget audit cannot account for an unrun quality suite')
        if (not result or result.get('status')!='failed'
            or result.get('error')!='Declared per-request deadline exceeded'
            or note.get('disposition')!=BUDGET or note.get('run_id')!=job['id']
            or note.get('request_timeout_seconds')!=900
            or note.get('final_task_score','missing') is not None
            or note.get('completed_responses')!=len(result.get('turns',[]))):
            raise RuntimeError('Budget disposition requires the exact preserved attempted timeout')
        path=Path(root)/'results'/job['id']/'result.json'
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=note.get('result_sha256'):
            raise RuntimeError('Budget audit result hash mismatch')
        return disposition
    if note.get('disposition')!=RESOURCE or note.get('server_error')!='kIOGPUCommandBufferCallbackErrorOutOfMemory':raise RuntimeError('Missing concrete reviewed GPU resource failure')
    if disposition==RESOURCE:
        if note.get('run_id')!=job['id'] or not result or result.get('status')!='failed' or note.get('final_task_score') is not None:raise RuntimeError('Resource disposition does not match a preserved failed attempt')
    elif result is not None:raise RuntimeError('Cannot defer an already attempted result')
    return disposition


def gpu_safety_failures(root):
    import json
    path=Path(root)/'work/compute-safety-events.json'
    if not path.exists():return 0
    return sum(bool(e.get('count_toward_two_failure_stop')) for e in json.loads(path.read_text())['events'])
