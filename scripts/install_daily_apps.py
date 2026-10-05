#!/usr/bin/env python3
"""Copy verified installed macOS app bundles to an explicitly identified new Studio.

Copies application code only. Never copies home/Library settings or credentials,
launches apps, overwrites existing apps, changes Gatekeeper, or uses sudo.
"""
import argparse
import datetime
import json
from pathlib import Path
import plistlib
import re
import shlex
import subprocess
import uuid

APPS=['Wispr Flow','Notion','Screen Studio','Todoist','Ghostty','Notion Calendar','Grok Bot','ChatGPT','Claude']
ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host',required=True)
    parser.add_argument('--identity',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_.-]+@[A-Za-z0-9_.-]+',args.host):
        parser.error('Expected an explicit user@hostname')
    ssh=['ssh','-i',str(args.identity),'-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=10',args.host]
    def remote(script,check=True):
        return subprocess.run(ssh+[script],capture_output=True,text=True,check=check,timeout=120)
    chip=remote('sysctl -n machdep.cpu.brand_string').stdout.strip()
    if chip!='Apple M5 Ultra':raise SystemExit('Unexpected target chip; refusing app installation: '+chip)
    remote('test -w /Applications')
    stage='/tmp/ashen-app-setup-'+uuid.uuid4().hex
    remote('umask 077; mkdir '+shlex.quote(stage))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    report={'target_chip':chip,'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'method':'Signed app-bundle transfer over verified SSH; no settings or credentials copied','apps':[]}
    try:
        for name in APPS:
            bundle=name+'.app';source=Path('/Applications')/bundle
            with (source/'Contents/Info.plist').open('rb') as f:info=plistlib.load(f)
            expected={'app':name,'bundle_id':info['CFBundleIdentifier'],'version':info.get('CFBundleShortVersionString')}
            target='/Applications/'+bundle
            if remote('test ! -e '+shlex.quote(target),check=False).returncode:
                report['apps'].append({**expected,'status':'already_present_not_modified'})
                print(name+': already exists, preserved',flush=True);continue
            subprocess.run(['codesign','--verify','--deep','--strict',str(source)],check=True,capture_output=True)
            print('Transferring '+name,flush=True)
            producer=subprocess.Popen(['/usr/bin/tar','-cf','-','-C','/Applications',bundle],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            consumer=subprocess.Popen(ssh+['/usr/bin/tar -xf - -C '+shlex.quote(stage)],stdin=producer.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            producer.stdout.close()
            out,err=consumer.communicate(timeout=1800)
            producer_err=producer.stderr.read();producer.wait(timeout=60)
            if producer.returncode or consumer.returncode:
                raise RuntimeError('Transfer failed for '+name+': '+(err+producer_err).decode(errors='replace'))
            staged=stage+'/'+bundle
            remote('/usr/bin/codesign --verify --deep --strict '+shlex.quote(staged))
            actual_id=remote('/usr/libexec/PlistBuddy -c '+shlex.quote('Print :CFBundleIdentifier')+' '+shlex.quote(staged+'/Contents/Info.plist')).stdout.strip()
            actual_version=remote('/usr/libexec/PlistBuddy -c '+shlex.quote('Print :CFBundleShortVersionString')+' '+shlex.quote(staged+'/Contents/Info.plist')).stdout.strip()
            if (actual_id,actual_version)!=(expected['bundle_id'],expected['version']):
                raise RuntimeError('Transferred app identity/version mismatch: '+name)
            remote('test ! -e '+shlex.quote(target)+' && /bin/mv '+shlex.quote(staged)+' '+shlex.quote(target))
            remote('/usr/bin/codesign --verify --deep --strict '+shlex.quote(target))
            assessment=remote('/usr/sbin/spctl --assess --type execute --verbose=2 '+shlex.quote(target),check=False)
            row={**expected,'status':'installed','signature_valid':True,'gatekeeper_accepted':assessment.returncode==0,
                 'gatekeeper_assessment':(assessment.stdout+assessment.stderr).strip()}
            report['apps'].append(row)
            args.output.write_text(json.dumps(report,indent=2)+'\n')
            print(name+': installed and signature verified',flush=True)
    finally:
        # Only the unique, task-created staging directory is removed.
        remote('/bin/rm -rf '+shlex.quote(stage),check=False)
        report['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('App transfer complete. No apps were launched.',flush=True)


if __name__=='__main__':main()
