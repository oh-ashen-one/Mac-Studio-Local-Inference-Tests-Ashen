#!/usr/bin/env python3
"""Download immutable public artifacts and verify every file against the lock."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import time

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def verify(model, directory):
    failures = []
    for item in model['files']:
        path = directory / item['path']
        if not path.is_file() or path.stat().st_size != item['bytes']:
            failures.append(item['path'] + ': missing or wrong size')
        elif digest(path) != item['sha256']:
            failures.append(item['path'] + ': SHA256 mismatch')
    if failures:
        raise ValueError('; '.join(failures))
    return len(model['files'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['download', 'verify'])
    parser.add_argument('--model', default='all')
    parser.add_argument('--directory', type=Path, default=ROOT / 'models')
    args = parser.parse_args()
    lock_path = ROOT / 'config/models.lock.json'
    lock = json.loads(lock_path.read_text())
    selected = [m for m in lock['models'] if args.model in ('all', m['id'])]
    if not selected:
        parser.error('Unknown model ID')
    args.directory.mkdir(parents=True, exist_ok=True)
    needed = sum(f['bytes'] for m in selected for f in m['files']
                 if not (args.directory / m['id'] / f['path']).is_file())
    if args.action == 'download' and shutil.disk_usage(args.directory).free < needed + 100 * 1024**3:
        raise RuntimeError('Insufficient free space: preserve at least 100 GiB headroom')
    report = {'lock_sha256': digest(lock_path), 'models': [], 'started_at': time.time()}
    for model in selected:
        directory = args.directory / model['id']
        print(json.dumps({'event': 'start', 'model': model['id'], 'bytes': model['total_bytes']}), flush=True)
        if args.action == 'download':
            os.environ.setdefault('HF_XET_NUM_CONCURRENT_RANGE_GETS', '4')
            os.environ.setdefault('HF_HUB_DOWNLOAD_TIMEOUT', '120')
            from huggingface_hub import snapshot_download
            snapshot_download(repo_id=model['repo'], revision=model['revision'],
                              local_dir=directory, max_workers=4,
                              allow_patterns=[f['path'] for f in model['files']])
        count = verify(model, directory)
        item = {'id': model['id'], 'revision': model['revision'], 'verified_files': count,
                'bytes': model['total_bytes'], 'sha256_verified': True}
        report['models'].append(item)
        print(json.dumps({'event': 'verified', **item}), flush=True)
        state = ROOT / 'work/model-verification.json'
        state.parent.mkdir(exist_ok=True)
        temp = state.with_suffix('.tmp')
        temp.write_text(json.dumps(report, indent=2) + '\n')
        temp.replace(state)
    print('All selected model files verified.', flush=True)


if __name__ == '__main__':
    main()
