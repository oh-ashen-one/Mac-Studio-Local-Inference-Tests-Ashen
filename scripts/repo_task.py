#!/usr/bin/env python3
"""Fixed Django task tools and sandboxed regression evaluation. No model launch here."""
import argparse,hashlib,io,json,os,resource,shutil,subprocess,sys,tarfile,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'vendor/django-task'
VENV=ROOT/'vendor/repo-task-venv'
TASK=json.loads((ROOT/'config/repo-task.json').read_text())

def prepare():
    if not BASE.exists():
        data=urllib.request.urlopen('https://api.github.com/repos/django/django/tarball/'+TASK['base_commit'],timeout=120).read()
        stage=ROOT/'work/django-source';stage.mkdir(exist_ok=True)
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:archive.extractall(stage,filter='data')
        candidates=list(stage.glob('django-*'))
        if len(candidates)!=1:raise RuntimeError('Unexpected repository archive layout')
        candidates[0].rename(BASE);stage.rmdir()
    uv=str(ROOT/'.tools/uv') if (ROOT/'.tools/uv').exists() else shutil.which('uv')
    if not VENV.exists():subprocess.run([uv,'venv','--python','3.10.19',str(VENV)],check=True)
    subprocess.run([uv,'pip','install','--python',str(VENV/'bin/python'),'asgiref==3.3.4','pytz==2021.1','sqlparse==0.4.1'],check=True)
    print('Public task source and isolated evaluator prepared; no inference.')

def profile(workspace):
    python_home=(VENV/'bin/python').resolve().parents[1]
    paths=[workspace.resolve(),VENV.resolve(),python_home]
    reads=' '.join('(subpath '+json.dumps(str(x))+')' for x in paths)
    return '(version 1)(deny default)(allow process-exec)(allow process-fork)(allow sysctl-read)(allow mach-lookup)(allow file-read-metadata)(allow file-read* file-map-executable (literal "/") (subpath "/System") (subpath "/private/preboot") (subpath "/private/var/db/dyld") (subpath "/private/var/db/com.apple.dyld") (subpath "/private/var/run/com.apple.dyld") (subpath "/usr") (subpath "/Library/Apple") (literal "/dev/urandom") (literal "/dev/random") (literal "/dev/null") '+reads+')(allow file-write* (subpath '+json.dumps(str(workspace.resolve()))+'))'

def evaluate(candidate,out):
    out.mkdir(parents=True,exist_ok=False);tree=out/'tree';shutil.copytree(BASE,tree)
    for f in candidate.glob('django/db/migrations/*.py'):shutil.copyfile(f,tree/f.relative_to(candidate))
    subprocess.run(['/usr/bin/patch','-p1','-i',str(ROOT/'config/repo-eval/django-14500-tests.patch')],cwd=tree,check=True,capture_output=True)
    tmp=tree/'.task-tmp';tmp.mkdir();env={'PATH':'/usr/bin:/bin','HOME':str(tmp),'TMPDIR':str(tmp),'PYTHONPATH':str(tree),'PYTHONDONTWRITEBYTECODE':'1','LANG':'en_US.UTF-8'}
    command=['/usr/bin/sandbox-exec','-p',profile(tree),str(VENV/'bin/python'),'-B','tests/runtests.py','migrations.test_executor.ExecutorTests','--parallel','1','--verbosity','1']
    def limits():resource.setrlimit(resource.RLIMIT_CPU,(60,60));resource.setrlimit(resource.RLIMIT_NOFILE,(128,128))
    result=subprocess.run(command,cwd=tree,env=env,capture_output=True,text=True,timeout=120,preexec_fn=limits)
    text=(result.stdout+result.stderr).replace(str(ROOT),'<repo>');(out/'test.log').write_text(text)
    report={'exit_code':result.returncode,'passed':result.returncode==0,'summary':text[-4000:]}
    (out/'evaluation.json').write_text(json.dumps(report,indent=2)+'\n');shutil.rmtree(tree)
    return report

def fresh(path):shutil.copytree(BASE,path)

def act(request,candidate,evaluation_dir):
    action=request.get('action')
    if action=='test':return evaluate(candidate,evaluation_dir)
    if action=='finish':return {'finished':True}
    relative=Path(request.get('path',''))
    path=(candidate/relative).resolve()
    if not path.is_relative_to(candidate.resolve()) or not path.is_file():raise ValueError('Path is not an existing repository file')
    if action=='read':return {'path':str(relative),'text':path.read_text()[:30000]}
    if action=='replace':
        if relative.parent!=Path('django/db/migrations') or relative.suffix!='.py':raise ValueError('Edit only django/db/migrations/*.py; tests are immutable')
        old=request.get('old','');new=request.get('new','');text=path.read_text()
        if not old or text.count(old)!=1 or len(new)>30000:raise ValueError('Replacement must match exactly one nonempty source span')
        path.write_text(text.replace(old,new,1));return {'edited':str(relative)}
    raise ValueError('Use read, replace, test or finish')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prepare',action='store_true');p.add_argument('--check-baseline',action='store_true');a=p.parse_args()
    if a.prepare:prepare()
    if a.check_baseline:
        out=ROOT/'work/repo-baseline';print(evaluate(BASE,out))
