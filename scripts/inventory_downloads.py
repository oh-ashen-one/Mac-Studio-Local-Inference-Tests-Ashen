#!/usr/bin/env python3
"""Inspect model filenames and metadata; never load weights or operate a model app."""
import argparse
import datetime
import json
import re
from pathlib import Path


def describe(folder, name, revision=None, component=None):
    settings = json.loads((folder / 'config.json').read_text())
    index = folder / 'model.safetensors.index.json'
    wanted = set(json.loads(index.read_text()).get('weight_map', {}).values()) if index.exists() else set()
    wanted = {f for f in wanted if isinstance(f, str) and f.endswith('.safetensors') and not Path(f).is_absolute() and '..' not in Path(f).parts}
    files = list(folder.glob('*.safetensors'))
    present = [p for p in files if p.is_file()]
    partials = [p for p in folder.iterdir() if p.is_file() and p.name.endswith(('.part', '.incomplete', '.download'))]
    declared = [int(m.group(1)) for p in present + partials if (m := re.search(r'-of-(\d+)\.safetensors', p.name))]
    expected = len(wanted) or (max(declared) if declared else 1 if (folder/'model.safetensors').exists() or (folder/'model.safetensors.part').exists() else None)
    missing = sum(not (folder/f).is_file() for f in wanted) if wanted else max(0, expected-len(present)) if expected else None
    if not present and not partials and not wanted:
        return None
    quant = settings.get('quantization') or settings.get('quantization_config') or {}
    bits = quant.get('bits') if isinstance(quant, dict) else None
    dtype = settings.get('dtype') or settings.get('torch_dtype')
    staging = bool(revision and 'staging' in revision)
    return {
        'name': name + (' · ' + component if component else ''),
        'model_family_id': name,
        'component': component,
        'revision': revision,
        'revision_kind': 'download snapshot identifier; not assumed to be a source Git commit',
        'format': 'MLX' if bits else 'Safetensors ' + str(dtype or 'precision unverified'),
        'precision': str(bits) + '-bit metadata' if bits else dtype,
        'precision_warning': 'Name mentions MXFP8 but config default differs; verify final tensor precision' if 'mxfp8' in name.lower() and bits != 8 else None,
        'model_type': settings.get('model_type'),
        'bytes_present': sum(p.stat().st_size for p in present),
        'weight_files_present': len(present),
        'weight_files_expected': expected,
        'missing_files': missing,
        'partial_files': len(partials),
        'status': 'downloading' if partials or missing or staging else 'files_present',
        'verification': 'Not checksum-verified; runtime compatibility and provenance pending. Partial-file sizes are not treated as downloaded progress.',
    }


def scan(home, include_darkbloom_models=False):
    rows, seen = [], set()
    roots = [home/'.lmstudio/models', home/'.cache/lm-studio/models', home/'.cache/huggingface/hub']
    if include_darkbloom_models:
        # Weight directories only: never inspect application/account databases or use the app/CLI.
        roots += [home/'.darkbloom/models', home/'.darkbloom/cache/models', home/'Library/Caches/darkbloom/models', home/'Library/Application Support/Darkbloom/models']
    for root in roots:
        if not root.is_dir():
            continue
        for config in root.rglob('config.json'):
            if root.name == 'hub' and 'snapshots' not in config.parts:
                continue
            folder = config.parent
            try:
                key = str(folder.resolve())
                if key in seen:
                    continue
                seen.add(key)
                parts = folder.relative_to(root).parts
                revision = component = None
                if parts[0].startswith('models--'):
                    name = parts[0][8:].replace('--', '/')
                    if 'snapshots' in parts:
                        position = parts.index('snapshots')
                        revision = parts[position+1]
                        component = '/'.join(parts[position+2:]) or None
                else:
                    name = '/'.join(parts)
                row = describe(folder, name, revision, component)
                if row:
                    rows.append(row)
            except (OSError, ValueError, TypeError):
                continue
        for file in root.rglob('*.gguf'):
            try:
                key = str(file.resolve())
                if key in seen or not file.is_file():
                    continue
                seen.add(key)
                rows.append({'name': file.name, 'format': 'GGUF', 'bytes_present': file.stat().st_size, 'status': 'files_present', 'verification': 'Presence only; completeness, tensor metadata and checksum pending'})
            except OSError:
                continue
        for file in root.rglob('*.gguf.part'):
            rows.append({'name': file.name, 'format': 'GGUF', 'bytes_present': 0, 'partial_files': 1, 'status': 'downloading', 'verification': 'Incomplete file; logical partial size is not download progress'})
    return sorted(rows, key=lambda r: (r.get('model_family_id', r['name']).lower(), bool(r.get('component'))))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--machine', required=True)
    parser.add_argument('--include-darkbloom-model-files', action='store_true', help='Explicit owner authorization to inspect downloaded weight metadata; never operate Darkbloom')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = {'machine_id': args.machine, 'observed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'method': 'Model-directory metadata and stat only; no app/CLI launch or weight loading', 'models': scan(Path.home(), args.include_darkbloom_model_files)}
    text = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    else:
        print(text)


if __name__ == '__main__':
    main()
