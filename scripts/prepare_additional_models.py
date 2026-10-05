#!/usr/bin/env python3
"""Pin and hash completed owner-downloaded packages, without loading or modifying them."""
import argparse,datetime,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from models import digest
from first_test import write_json

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--catalog',type=Path,required=True);a=p.parse_args()
    if subprocess.check_output(['sysctl','-n','machdep.cpu.brand_string'],text=True).strip()!='Apple M5 Ultra':raise RuntimeError('Preparation target must be M5')
    hub=Path.home()/'.cache/huggingface/hub'
    if list(hub.rglob('*.part')) or list(hub.rglob('*.incomplete')) or list(hub.glob('models--*/snapshots/*staging*')):raise RuntimeError('Download batch still incomplete')
    catalog={m['id']:m for m in json.loads(a.catalog.read_text())['models']}
    lock={'schema_version':1,'cohort':'owner-darkbloom-downloads-20261001','note':'Separate additional cohort; original pinned three models unchanged. Files are read in place; provider not used for inference.','models':[]}
    receipt={'status':'verifying','started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'models':[]}
    for path in sorted(hub.glob('models--*/snapshots/*/.darkbloom-manifest.json')):
        manifest=json.loads(path.read_text());identifier=manifest['model_id'];entry=catalog.get(identifier)
        if not entry:raise RuntimeError('Model missing from pinned catalog: '+identifier)
        if manifest['version']!=entry['version'] or manifest['aggregate_sha256']!=entry['aggregate_sha256']:raise RuntimeError('Catalog/package revision mismatch: '+identifier)
        folder=path.parent;config=json.loads((folder/'config.json').read_text());files=[]
        receipt.update(active_model=identifier);write_json(ROOT/'work/additional-preparation.json',receipt)
        for f in manifest['files']:
            name=f['path'];relative=Path(name)
            if relative.is_absolute() or '..' in relative.parts:raise RuntimeError('Unsafe manifest path')
            target=folder/relative
            if not target.is_file() or target.stat().st_size!=f['size_bytes']:raise RuntimeError('File missing or wrong size: '+name)
            if digest(target)!=f['sha256']:raise RuntimeError('File hash mismatch: '+name)
            files.append({'path':name,'bytes':f['size_bytes'],'sha256':f['sha256']})
            receipt.update(verified_files=len(files),expected_files=len(manifest['files']));write_json(ROOT/'work/additional-preparation.json',receipt)
        model={'id':identifier,'display_name':entry['display_name'],'repo':entry['hugging_face_id'],'revision':manifest['version'],'source_revision':entry.get('metadata',{}).get('hub_revision'),'artifact_manifest_sha256':manifest['aggregate_sha256'],'catalog_source':'https://api.darkbloom.dev/v1/models/catalog?type=text','quantization':entry['quantization']+' catalog; '+str((config.get('quantization') or {}).get('bits','unknown'))+'-bit config default','backend':'mlx','model_type':config['model_type'],'context_limit':entry['max_context_length'],'storage':{'kind':'huggingface_cache','relative_path':str(folder.relative_to(Path.home()))},'total_bytes':sum(f['bytes'] for f in files),'files':files,'chat_template_kwargs':{'enable_thinking':False},'speculation':False,'vision_audio_testing':False}
        lock['models'].append(model);receipt['models'].append({'id':identifier,'verified_files':len(files),'sha256_verified':True,'total_bytes':model['total_bytes']});print('Verified',identifier,len(files),'files',flush=True)
    if not lock['models']:raise RuntimeError('No completed package receipts found')
    write_json(ROOT/'config/additional-models.lock.json',lock);receipt.update(status='files_verified_runtime_pending',lock_sha256=digest(ROOT/'config/additional-models.lock.json'),finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());write_json(ROOT/'work/additional-preparation.json',receipt)
if __name__=='__main__':main()
