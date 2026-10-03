#!/usr/bin/env python3
"""Copy only finished M5 evidence through the private adapter; never run inference.

Run on the controller. Review and commit/push the resulting files normally.
After pushing, --sync-target preserves original raw evidence and fast-forwards
the target checkout. It never resets files, retries trials, or merges main.
"""
import argparse
import hashlib
import io
import inspect
import json
import re
import shlex
import shutil
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANCH = 'codex/long-context-dashboard-20261001'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def connection():
    m = json.loads((ROOT / 'config/machines.local.json').read_text())['studio-new']
    assert m['transport'] == 'ssh'
    args = ['ssh', '-i', m['identity_file'], '-o', 'BatchMode=yes',
            '-o', 'StrictHostKeyChecking=yes']
    for option in m.get('ssh_options', []):
        args += ['-o', option]
    return m, args + [m['target']]


def remote(code):
    m, args = connection()
    command = 'cd ' + shlex.quote(m['repository']) + ' && .venv/bin/python -c ' + shlex.quote(code)
    return subprocess.check_output(args + [command], cwd=ROOT)


def sanitize(data):
    # Native logs may contain incomplete UTF-8 token fragments. Redact known
    # private byte sequences without dropping or replacing unrelated raw bytes.
    m, _ = connection()
    for value, label in [(m['repository'], '<M5_REPO>'),
                         (str(Path(m['repository']).parent), '<M5_HOME>'),
                         (str(ROOT), '<CONTROLLER_REPO>'),
                         (str(Path.home()), '<CONTROLLER_HOME>'),
                         (m['target'], '<M5_SSH_TARGET>'),
                         (m['target'].split('@')[-1], '<M5_PRIVATE_HOST>')]:
        data = data.replace(value.encode('utf-8'), label.encode('utf-8'))
    return data


CAMPAIGNS = {
    'baseline': {'ledger':'work/unified-campaign.json','plan':'config/unified-campaign.json','aggregate':'results/unified-overnight-20261002','prefix':'u20261002-'},
    'mistral': {'ledger':'work/mistral-campaign.json','plan':'config/mistral-campaign-20261003.json','aggregate':'results/mistral-extension-20261003','prefix':'u20261003-'},
}

def harvest(campaign='baseline'):
    settings=CAMPAIGNS[campaign]
    ledger=settings['ledger']
    # The remote ledger's completion is set only after the child exits and its
    # telemetry is saved. Active/incomplete directories are never transferred.
    audit = json.loads(remote('''import json,pathlib,psutil
s=json.loads(pathlib.Path(''' + repr(ledger) + ''').read_text())
ids=[j['id'] for j in s['jobs'] if j['status']=='complete' and j['id']!=s.get('active') and pathlib.Path('results',j['id'],'campaign-telemetry.json').exists()]
if s['status']=='stopped' and not psutil.pid_exists(s['pid']):
 for j in s['jobs']:
  p=pathlib.Path('results',j['id']);f=p/('run.json' if j['kind']=='replay' else 'result.json')
  if f.exists() and json.loads(f.read_text()).get('status')=='failed' and (p/'completion-audit.json').exists():ids.append(j['id'])
print(json.dumps({'ids':ids,'state':s}))
'''))
    copied = []
    for run in audit['ids']:
        assert re.fullmatch(re.escape(settings['prefix'])+r'[a-z0-9-]+', run)
        destination = ROOT / 'results' / run
        if (destination / 'publication.json').exists():
            continue
        if destination.exists():
            raise RuntimeError('Unreviewed local result already exists: ' + run)
        archive = remote('''import io,json,pathlib,sys,tarfile,psutil
run=''' + repr(run) + '''
s=json.loads(pathlib.Path(''' + repr(ledger) + ''').read_text())
j=next(j for j in s['jobs'] if j['id']==run)
p=pathlib.Path('results')/run
if j['status']=='complete':
 assert s.get('active')!=run and (p/'campaign-telemetry.json').exists()
else:
 assert s['status']=='stopped' and not psutil.pid_exists(s['pid']) and (p/'completion-audit.json').exists()
 assert json.loads((p/('run.json' if j['kind']=='replay' else 'result.json')).read_text())['status']=='failed'
with tarfile.open(fileobj=sys.stdout.buffer,mode='w|') as t:
 for f in sorted(p.rglob('*')):
  assert not f.is_symlink()
  if f.is_file():t.add(f,arcname=str(f.relative_to(p)),recursive=False)
''')
        stage = ROOT / 'work/publication/unified' / run
        stage.mkdir(parents=True, exist_ok=True)
        receipt = {'run_id': run, 'scope': 'Exited child only, including explicitly audited failures; original M5 bytes retained', 'files': {}}
        with tarfile.open(fileobj=io.BytesIO(archive), mode='r:') as t:
            for member in t.getmembers():
                relative = Path(member.name)
                if not member.isfile() or relative.is_absolute() or '..' in relative.parts:
                    raise ValueError('Unsafe evidence archive member')
                original = t.extractfile(member).read()
                public = sanitize(original)
                path = stage / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(public)
                receipt['files'][str(relative)] = {'original_sha256': sha(original), 'published_sha256': sha(public)}
        (stage / 'publication.json').write_text(json.dumps(receipt, indent=2) + '\n')
        shutil.copytree(stage, destination)
        copied.append(run)
    # Save a timestamped aggregate, never an active primary result file. This
    # preserves accurate interim coverage while long quality suites are running.
    report_call='write()' if campaign=='baseline' else 'write('+repr(settings['plan'])+','+repr(ledger)+','+repr(settings['aggregate'])+')'
    remote("import sys;sys.path.insert(0,'scripts');from unified_report import write;"+report_call)
    aggregate=ROOT/settings['aggregate'];aggregate.mkdir(parents=True,exist_ok=True)
    for name in ['summary.json', 'README.md']:
        public = sanitize(remote("import pathlib,sys;sys.stdout.buffer.write(pathlib.Path(" + repr(settings['aggregate']+'/'+name) + ").read_bytes())"))
        (aggregate / name).write_bytes(public)
    print(json.dumps({'copied': copied, 'status': audit['state']['status'], 'active': audit['state'].get('active')}, indent=2))


def active_controls(root,pid_exists):
    paths=['work/unified-campaign.json','work/mistral-campaign.json',
           'work/mistral-qualification-driver.json','work/mistral-preparation.json']
    active=[]
    for name in paths:
        p=Path(root)/name
        if p.exists():
            pid=json.loads(p.read_text()).get('pid')
            if pid and pid_exists(pid):active.append(name)
    return active


def aggregate_files():
    return {f'results/{name}/{file}'
            for name in ['unified-overnight-20261002','mistral-extension-20261003']
            for file in ['summary.json','README.md']}


def preserve_aggregate(root,relative):
    # Only our generated reports may be moved aside without a per-run receipt.
    assert relative in aggregate_files(),'Unknown aggregate path'
    p=Path(root)/relative
    assert p.is_file() and not p.is_symlink()
    data=p.read_bytes();digest=hashlib.sha256(data).hexdigest()
    backup=Path(root)/'work/published-backup/aggregates'/digest/relative
    backup.parent.mkdir(parents=True,exist_ok=True)
    if backup.exists():assert backup.read_bytes()==data
    else:backup.write_bytes(data)
    assert hashlib.sha256(backup.read_bytes()).hexdigest()==digest
    return backup


def sync_target():
    print(remote('''import hashlib,json,pathlib,subprocess,psutil
from pathlib import Path
''' + inspect.getsource(active_controls) + inspect.getsource(aggregate_files) + inspect.getsource(preserve_aggregate) + '''
def git(*a):return subprocess.check_output(['git',*a])
branch=''' + repr(BRANCH) + '''
assert git('branch','--show-current').decode().strip()==branch
subprocess.run(['git','fetch','origin',branch],check=True)
target='origin/'+branch
subprocess.run(['git','merge-base','--is-ancestor','HEAD',target],check=True)
states=[json.loads(p.read_text()) for p in [pathlib.Path('work/unified-campaign.json'),pathlib.Path('work/mistral-campaign.json')] if p.exists()]
state=states[0]
changes=git('diff','--name-only','HEAD..'+target).decode().splitlines()
holders=pathlib.Path.home()/'.cache/gpu-slot/holders'
live_gpu=any(psutil.pid_exists(json.loads(p.read_text()).get('pid',0)) for p in holders.glob('*.json'))
if active_controls(pathlib.Path.cwd(),psutil.pid_exists) or live_gpu:
 allowed={'config/extension-runtime-candidates.json','scripts/publication_labels.py','tests/test_publication.py','scripts/harvest_unified.py','scripts/unified_report.py','scripts/report_additional.py','scripts/report_unified_speed.py','config/requirements-plotting.lock','scripts/preview.py','HANDOFF.md','README.md'}
 assert all(p in allowed or p.startswith(('results/','viewer/','docs/','outputs/','hardware/')) for p in changes),'Refusing to change executing runtime code'
conflicts=set(git('ls-files','--others','--exclude-standard').decode().splitlines()) & set(git('ls-tree','-r','--name-only',target).decode().splitlines())
runs={p.split('/')[1] for p in conflicts if p.startswith(('results/u20261002-','results/u20261003-'))}
assert all(p.startswith(('results/u20261002-','results/u20261003-')) or p in aggregate_files() for p in conflicts),'Unrelated untracked conflict'
for run in sorted(runs):
 state=next(s for s in states if any(j['id']==run for j in s['jobs']))
 j=next(j for j in state['jobs'] if j['id']==run)
 if j['status']=='complete':assert run!=state.get('active')
 else:
  import psutil
  assert state['status']=='stopped' and not psutil.pid_exists(state['pid'])
  assert pathlib.Path('results',run,'completion-audit.json').exists()
 receipt=json.loads(git('show',target+':results/'+run+'/publication.json'))
 source=pathlib.Path('results')/run
 for f in source.rglob('*'):
  if f.is_file():
   expected=receipt['files'][str(f.relative_to(source))]
   actual=hashlib.sha256(f.read_bytes()).hexdigest()
   assert actual in expected.values(),'Original evidence changed: '+str(f)
 dest=pathlib.Path('work/published-backup')/run
 assert not dest.exists()
 dest.parent.mkdir(parents=True,exist_ok=True)
 source.rename(dest)
# Aggregate is reproducible and may have changed after the report snapshot.
# The first publication is untracked; preserve it before adopting the copy.
head_files=set(git('ls-tree','-r','--name-only','HEAD').decode().splitlines())
for relative in sorted(aggregate_files()):
 p=pathlib.Path(relative)
 if p.exists() and (relative in conflicts or git('diff','--',relative)):
  preserve_aggregate(pathlib.Path.cwd(),relative)
  if relative in head_files:p.write_bytes(git('show','HEAD:'+relative))
  else:p.unlink()
subprocess.run(['git','merge','--ff-only',target],check=True)
print('Original bytes preserved; target fast-forwarded')
''').decode())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sync-target', action='store_true')
    parser.add_argument('--campaign',choices=list(CAMPAIGNS),default='baseline')
    args = parser.parse_args()
    sync_target() if args.sync_target else harvest(args.campaign)
