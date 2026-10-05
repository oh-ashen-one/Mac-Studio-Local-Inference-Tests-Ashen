#!/usr/bin/env python3
"""Hold one GPU slot for a fixed idle Blender scene while the official replay runs."""
import argparse,json,os,signal,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from first_test import shared_gpu_slot,stop,write_json,safety

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--allow-inference',action='store_true');p.add_argument('--run-id',required=True);p.add_argument('--machine',choices=['studio-old','studio-new'],default='studio-new');a=p.parse_args()
    if not a.allow_inference:p.error('Owner authorization and --allow-inference required')
    signal.signal(signal.SIGTERM,lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    safety(a.machine);app=Path('/Applications/Blender.app');subprocess.run(['codesign','--verify','--deep','--strict',str(app)],check=True)
    dialogs=subprocess.run(['pgrep','-fl','UserNotificationCenter|CoreServicesUIAgent'],capture_output=True,text=True)
    if dialogs.returncode==0:raise RuntimeError('A system dialog process is present; resolve it before launching another GUI tool')
    blender=runner=None
    with shared_gpu_slot() as slot:
        try:
            script=ROOT/'work/blender-fixture.py';script.write_text('import bpy,json,os\nfrom pathlib import Path\nbpy.context.scene.render.engine="BLENDER_WORKBENCH"\nPath(os.environ["ASHEN_BLENDER_RECEIPT"]).write_text(json.dumps({"pid":os.getpid(),"version":bpy.app.version_string,"scene":"Factory cube, camera and light; idle solid viewport; no render","objects":sorted(o.name for o in bpy.data.objects),"window_size":[1280,720]}))\n')
            env=dict(os.environ,ASHEN_BLENDER_RECEIPT=str(ROOT/'work/blender-condition.json'),BLENDER_USER_CONFIG=str(ROOT/'work/blender-config'))
            (ROOT/'work/blender-condition.json').unlink(missing_ok=True)
            with (ROOT/'work/blender-condition.log').open('w') as log:
                blender=subprocess.Popen([str(app/'Contents/MacOS/Blender'),'--factory-startup','--disable-autoexec','--no-splash','--window-geometry','100','100','1280','720','--python',str(script)],env=env,stdout=log,stderr=log,start_new_session=True)
                for _ in range(60):
                    if blender.poll() is not None:raise RuntimeError('Owned Blender exited; no automatic restart')
                    if (ROOT/'work/blender-condition.json').exists():break
                    time.sleep(1)
                else:raise TimeoutError('Blender fixture did not initialize')
                receipt=json.loads((ROOT/'work/blender-condition.json').read_text());receipt['slot']=slot;write_json(ROOT/'work/blender-condition.json',receipt)
                time.sleep(10)
                runner=subprocess.Popen([sys.executable,str(ROOT/'scripts/run_agentperf.py'),'--allow-inference','--condition','blender-open','--run-id',a.run_id,'--machine',a.machine],cwd=ROOT,start_new_session=True)
                while runner.poll() is None:
                    if blender.poll() is not None:raise RuntimeError('Blender exited during the condition; paired run invalid')
                    time.sleep(2)
                if runner.returncode:raise RuntimeError('Blender-condition replay failed')
        finally:stop(runner);stop(blender)
if __name__=='__main__':main()
