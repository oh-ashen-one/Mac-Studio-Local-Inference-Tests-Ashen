#!/usr/bin/env python3
"""Install the audited official Darkbloom package after benchmark workloads exit."""
import hashlib,json,subprocess,sys,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from first_test import safety,shared_gpu_slot,write_json

def main():
    safety()
    if int(subprocess.check_output(['sw_vers','-productVersion'],text=True).split('.')[0])<27:raise RuntimeError('Do not enroll in legacy MDM; this installer plan requires macOS 27+')
    if (Path.home()/'.darkbloom/Darkbloom.app').exists():raise RuntimeError('Existing installation preserved; inspect it instead of overwriting')
    lock=json.loads((ROOT/'config/darkbloom-install.lock.json').read_text())
    current=json.load(urllib.request.urlopen('https://api.darkbloom.dev/v1/releases/latest'))
    if any(current[k]!=lock[k] for k in ['version','bundle_hash','binary_hash','metallib_hash']):raise RuntimeError('Official release changed; review new release before installation')
    script=urllib.request.urlopen(lock['installer_url']).read()
    if hashlib.sha256(script).hexdigest()!=lock['installer_sha256']:raise RuntimeError('Installer changed; review before running')
    path=ROOT/'work/darkbloom-reviewed-install.sh';path.write_bytes(script)
    with shared_gpu_slot():
        with (ROOT/'work/darkbloom-install.log').open('w') as log:subprocess.run(['/bin/bash',str(path)],stdin=subprocess.DEVNULL,stdout=log,stderr=log,check=True)
    app=Path.home()/'.darkbloom/Darkbloom.app'
    subprocess.run(['codesign','--verify','--deep','--strict',str(app)],check=True)
    actual=hashlib.sha256((app/'Contents/MacOS/darkbloom').read_bytes()).hexdigest()
    if actual!=lock['binary_hash']:raise RuntimeError('Installed binary does not match pinned release')
    write_json(ROOT/'hardware/darkbloom-install.json',{'version':lock['version'],'backend':lock['backend'],'binary_sha256':actual,'signature_valid':True,'provider_started':False,'account_linked_by_this_task':False,'earnings_measurement':None,'notes':'Official installer runtime check only. No model download, provider serving, login or payout setup was initiated.'})
    print('Darkbloom installed and verified. Account linking and serving have not started.')
if __name__=='__main__':main()
