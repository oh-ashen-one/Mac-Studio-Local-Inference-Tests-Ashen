#!/usr/bin/env python3
"""Owner-authorized download-only retry of the exact failed Qwen catalog package."""
import argparse,datetime,json,os,signal,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODEL='qwen3.6-35b-a3b-vl-mtp-mxfp8'

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allow-download',action='store_true')
    args=parser.parse_args()
    if not args.allow_download:parser.error('Explicit owner download authorization required')
    if subprocess.check_output(['sysctl','-n','machdep.cpu.brand_string'],text=True).strip()!='Apple M5 Ultra':raise RuntimeError('Wrong target host')
    import psutil
    for proc in psutil.process_iter(['pid','name']):
        if proc.pid==os.getpid():continue
        try:
            for opened in proc.open_files():
                if MODEL in opened.path and opened.path.endswith(('.part','.incomplete')):raise RuntimeError('A downloader already owns Qwen partial files; preserve it')
        except (psutil.AccessDenied,psutil.NoSuchProcess):pass
    app=Path.home()/'.darkbloom/Darkbloom.app'
    subprocess.run(['codesign','--verify','--deep','--strict',str(app)],check=True,capture_output=True)
    directory=ROOT/'work/qwen-download-retry';directory.mkdir(exist_ok=True)
    receipt={'model_id':MODEL,'kind':'download_only_retry','status':'starting','started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'provider_started':False,'inference_started':False,'command':['darkbloom','models','download',MODEL]}
    def save():
        p=directory/'status.json';tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(receipt,indent=2)+'\n');tmp.replace(p)
    save();child=None
    signal.signal(signal.SIGTERM,lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    try:
        with (directory/'download.log').open('w') as log:
            child=subprocess.Popen([str(app/'Contents/MacOS/darkbloom'),'models','download',MODEL],env=dict(os.environ,DARKBLOOM_NO_UPDATE_CHECK='1'),stdin=subprocess.DEVNULL,stdout=log,stderr=log,start_new_session=True)
            receipt.update(status='downloading',pid=child.pid);save();started=time.monotonic()
            while child.poll() is None:
                if time.monotonic()-started>14400:raise TimeoutError('Four-hour download budget reached')
                time.sleep(5)
            receipt.update(status='download_command_completed' if child.returncode==0 else 'failed',exit_code=child.returncode,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());save()
            if child.returncode:raise RuntimeError('Download-only command failed; retain log and diagnose without enabling provider')
    except BaseException as exc:
        receipt.update(status='failed',error=str(exc).replace(str(Path.home()),'<home>'));save();raise
    finally:
        if child and child.poll() is None:
            child.terminate()
            try:child.wait(timeout=60)
            except subprocess.TimeoutExpired:child.kill();child.wait()

if __name__=='__main__':main()
