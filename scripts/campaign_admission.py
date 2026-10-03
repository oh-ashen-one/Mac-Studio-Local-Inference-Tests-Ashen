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
