#!/usr/bin/env python3
"""Read model-file metadata only. Never load weights, query a model app, or change downloads."""
import argparse,datetime,json
from pathlib import Path


def scan(home):
    rows=[];seen=set()
    roots=[home/'.lmstudio/models',home/'.cache/lm-studio/models',home/'.cache/huggingface/hub']
    for root in roots:
        if not root.is_dir():continue
        for config in root.rglob('config.json'):
            if 'snapshots' not in config.parts and root.name=='hub':continue
            folder=config.parent
            try:
                settings=json.loads(config.read_text());index=folder/'model.safetensors.index.json';wanted=set(json.loads(index.read_text()).get('weight_map',{}).values()) if index.exists() else set()
                files=list(folder.glob('*.safetensors'));present=[p for p in files if p.is_file()]
                if not files and not wanted:continue
                key=str(folder.resolve())
                if key in seen:continue
                seen.add(key);relative=folder.relative_to(root);parts=relative.parts
                if parts[0].startswith('models--'):
                    name=parts[0][8:].replace('--','/');revision=parts[parts.index('snapshots')+1] if 'snapshots' in parts else None
                    partials=list((root/parts[0]/'blobs').glob('*.incomplete'))
                else:name='/'.join(parts);revision=None;partials=list(folder.glob('*.incomplete'))
                missing=sum(not (folder/f).is_file() for f in wanted)
                quant=settings.get('quantization') or settings.get('quantization_config') or {};bits=quant.get('bits');dtype=settings.get('dtype') or settings.get('torch_dtype')
                fmt='MLX' if bits else ('Safetensors '+str(dtype or 'precision unverified'))
                rows.append({'name':name,'revision':revision,'format':fmt,'precision':str(bits)+'-bit' if bits else dtype,'model_type':settings.get('model_type'),'bytes_present':sum(p.stat().st_size for p in present),'weight_files_present':len(present),'weight_files_expected':len(wanted) or None,'missing_files':missing,'partial_files':len(partials),'status':'downloading' if missing or partials else 'files_present','verification':'Not checksum-verified; not benchmarked'})
            except (OSError,ValueError,TypeError):continue
        for file in root.rglob('*.gguf'):
            try:
                key=str(file.resolve())
                if key in seen or not file.is_file():continue
                seen.add(key);rows.append({'name':file.name,'revision':None,'format':'GGUF','precision':None,'bytes_present':file.stat().st_size,'weight_files_present':1,'weight_files_expected':None,'missing_files':None,'partial_files':0,'status':'files_present','verification':'Presence only; completeness, tensor metadata and checksum need verification'})
            except OSError:continue
        for file in root.rglob('*.gguf.part'):
            rows.append({'name':file.name,'format':'GGUF','bytes_present':file.stat().st_size,'status':'downloading','verification':'Incomplete file'})
    return sorted(rows,key=lambda r:r['name'].lower())


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--machine',required=True);p.add_argument('--output',type=Path);a=p.parse_args()
    result={'machine_id':a.machine,'observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Model-directory filenames, JSON metadata and stat only; no model or app launched','models':scan(Path.home())}
    data=json.dumps(result,indent=2)+'\n'
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(data)
    else:print(data)
if __name__=='__main__':main()
