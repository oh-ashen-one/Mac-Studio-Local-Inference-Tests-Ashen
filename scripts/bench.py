#!/usr/bin/env python3
"""Sequential, pinned MLX setup checks and fixed-token hardware benchmarks."""
import argparse
import contextlib
import datetime
import fcntl
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import random
import signal
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from models import digest, verify


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def timing_summary(start, token_times, end):
    n = len(token_times)
    span = token_times[-1] - token_times[0] if n > 1 else 0
    return {'output_tokens': n,
            'ttft_s': token_times[0] - start if n else None,
            'decode_tok_s': (n - 1) / span if span > 0 else None,
            'generation_wall_s': end - start}


def synthetic_prompt(tokenizer, target, seed):
    # This is a declared synthetic fixed-length workload, not a truncated user request.
    rng = random.Random(seed)
    text = 'Summarize the following fictional inventory in detail.\n'
    block = '\n'.join(f'Item {i}: {rng.randrange(1000)} units; status ready.' for i in range(100))
    while True:
        ids = tokenizer.encode(text, add_special_tokens=False)
        if len(ids) >= target:
            return ids[:target]
        text += block + '\n'


def append(path, record):
    with path.open('a') as stream:
        stream.write(json.dumps(record, ensure_ascii=False) + '\n')
        stream.flush()
        os.fsync(stream.fileno())


def preflight(machine, exclusive):
    import psutil
    chip = subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string'], text=True).strip()
    expected = {'studio-old': 'Apple M3 Ultra', 'studio-new': 'Apple M5 Ultra'}[machine]
    if chip != expected:
        raise RuntimeError(f'{machine} expects {expected}; observed {chip}')
    for proc in psutil.process_iter(['name', 'status']):
        name = (proc.info['name'] or '').lower()
        if any(x in name for x in ('unrealeditor', 'unity', 'blender', 'godot')) and proc.info['status'] == psutil.STATUS_ZOMBIE:
            raise RuntimeError('A renderer is stuck exiting; postpone GPU work')
    if exclusive:
        # Conservative gate: a live server/app may be idle, but ask its owner to close it.
        blockers = []
        for proc in psutil.process_iter(['name']):
            name = (proc.info['name'] or '').lower()
            if name in ('exo', 'lm studio', 'ollama') or name.startswith(('mlx_lm.server', 'llama-server')):
                blockers.append(name)
        if blockers:
            raise RuntimeError('Reserved benchmark window required; other model services are present: ' + ', '.join(sorted(set(blockers))))
    return {'chip': chip, 'available_memory_bytes': psutil.virtual_memory().available,
            'swap_used_bytes': psutil.swap_memory().used,
            'load_average': list(os.getloadavg())}


def worker(args, model_spec, output):
    if model_spec.get('backend') == 'dwarfstar':
        from native import run_native
        return run_native(args, model_spec, output)
    import mlx.core as mx
    import psutil
    from mlx_lm import load
    from mlx_lm.generate import generate_step
    directory = ROOT / 'models' / model_spec['id']
    verify(model_spec, directory)
    before = preflight(args.machine, args.suite == 'core')
    if before['available_memory_bytes'] < model_spec['total_bytes'] * 1.25 + 20 * 1024**3:
        raise RuntimeError('Insufficient available memory for conservative load budget')
    versions = {p: importlib.metadata.version(p) for p in ('mlx', 'mlx-lm', 'mlx-metal', 'transformers', 'numpy')}
    started = time.perf_counter()
    model, tokenizer, model_config = load(str(directory), return_config=True)
    mx.synchronize()
    load_s = time.perf_counter() - started
    context_limit = (model_config.get('text_config') or model_config).get('max_position_embeddings')
    config = json.loads((ROOT / 'config/campaign.json').read_text())
    if args.suite == 'core':
        cases = []
        offsets = [0, 4, 7]
        counts = [4, 3, 3]
        for cell in config['core_cells']:
            for i in range(2):
                cases.append({**cell, 'repeat': -i-1, 'warmup': True, 'prompt_seed': 100+i})
            for i in range(counts[args.session]):
                repeat = offsets[args.session] + i
                cases.append({**cell, 'repeat': repeat, 'warmup': False, 'prompt_seed': 1729+repeat})
        # Shuffle cells, retaining their two warmups before recorded repeats.
        grouped = [cases[i:i+counts[args.session]+2] for i in range(0, len(cases), counts[args.session]+2)]
        random.Random(702+args.session).shuffle(grouped)
        cases = [c for group in grouped for c in group]
    elif args.suite == 'pilot':
        cases = [{'id':'setup-speed','input_tokens':512,'output_tokens':32,'repeat':0,'warmup':False,'prompt_seed':1729}]
    else:
        cases = [{'id':'setup-reply','input_tokens':None,'output_tokens':128,'repeat':0,'warmup':False,'prompt_seed':1729}]
    for case in cases:
        if args.suite in ('core', 'pilot'):
            ids = synthetic_prompt(tokenizer, case['input_tokens'], case['prompt_seed'])
        else:
            ids = tokenizer.apply_chat_template(
                [{'role':'user','content':'Reply with the single word READY.'}],
                tokenize=True, add_generation_prompt=True, **model_spec['chat_template_kwargs'])
        if context_limit and len(ids) + case['output_tokens'] > context_limit:
            raise RuntimeError('Requested context exceeds model declaration')
        mx.random.seed(case['prompt_seed'])
        mx.clear_cache()
        mx.reset_peak_memory()
        record = {'schema_version':1,'kind':'hardware_microbenchmark' if args.suite=='core' else ('setup_pilot' if args.suite=='pilot' else 'setup_smoke'),
                  'run_id':str(uuid.uuid4()),'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'machine_id':args.machine,'model_id':model_spec['id'],'model_revision':model_spec['revision'],
                  'model_lock_sha256':digest(ROOT/'config/models.lock.json'),
                  'runtime_lock_sha256':digest(ROOT/'requirements-macos-arm64.lock'),
                  'campaign_sha256':digest(ROOT/'config/campaign.json'),
                  'harness_source_sha256':digest(Path(__file__)),
                  'harness_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                  'runtime_versions':versions,'os_build':subprocess.check_output(['sw_vers','-buildVersion'],text=True).strip(),
                  'session':args.session,'cell':case,'input_tokens':len(ids),'input_token_ids_sha256':canonical_hash(ids),
                  'load_s':load_s,'preflight':before,'settings':{'temperature':0,'kv_quantization':None,'prefix_reuse':False,
                    'speculation':False,'prefill_step_size':2048,'fixed_token_mode':args.suite in ('core','pilot'),
                    'chat_template_kwargs':model_spec['chat_template_kwargs'] if args.suite=='smoke' else None}}
        swap_before = psutil.swap_memory().used
        token_times, tokens = [], []
        start = time.perf_counter()
        generator = generate_step(mx.array(ids), model, max_tokens=case['output_tokens'], prefill_step_size=2048)
        finish = 'length'
        try:
            for token, _ in generator:
                now = time.perf_counter()
                if args.suite == 'smoke' and token in tokenizer.eos_token_ids:
                    finish = 'stop'
                    break
                tokens.append(int(token)); token_times.append(now)
                if now-start > config['request_timeout_s']:
                    raise TimeoutError('Request exceeded declared timeout')
            generator.close()
            mx.synchronize()
            end = time.perf_counter()
            record.update(timing_summary(start, token_times, end))
            record.update({'status':'ok','finish_reason':finish,'ready_marker_seen':('READY' in tokenizer.decode(tokens)) if args.suite=='smoke' else None,'peak_metal_bytes':mx.get_peak_memory(),
                           'process_rss_bytes':psutil.Process().memory_info().rss,
                           'swap_delta_bytes':psutil.swap_memory().used-swap_before,
                           'output_token_ids':tokens,'output_text':tokenizer.decode(tokens)})
            if not tokens:
                record['status'] = 'empty_output'
        except Exception as exc:
            record.update({'status':'error','error':str(exc).replace(str(ROOT),'<repo>'),
                           'partial_output_tokens':len(tokens)})
            append(output,record)
            raise
        finally:
            generator.close()
        append(output,record)
        print(json.dumps({'model':model_spec['id'],'cell':case['id'],'status':record['status'],
                          'kind':record['kind'],'tokens':len(tokens)}), flush=True)
        if args.suite=='smoke' and not record['ready_marker_seen']:
            raise RuntimeError('Smoke reply missing READY marker')
        if record['status']!='ok':
            raise RuntimeError('Setup produced no output')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--machine', choices=['studio-old','studio-new'], required=True)
    parser.add_argument('--suite', choices=['smoke','pilot','core'], default='smoke')
    parser.add_argument('--model', default='all')
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--session',type=int,choices=[0,1,2],default=0)
    parser.add_argument('--allow-inference', action='store_true', help='Use only after the owner explicitly starts GPU testing')
    parser.add_argument('--worker',action='store_true',help=argparse.SUPPRESS)
    args=parser.parse_args()
    if not args.allow_inference:
        parser.error('Preparation-only mode: no models will load. Ask the owner to start testing before using --allow-inference.')
    specs=json.loads((ROOT/'config/models.lock.json').read_text())['models']
    selected=[m for m in specs if args.model in ('all',m['id'])]
    if not selected: parser.error('Unknown model ID')
    args.output=args.output.resolve(); args.output.parent.mkdir(parents=True,exist_ok=True)
    if args.worker:
        if len(selected)!=1: parser.error('Worker requires one model')
        worker(args,selected[0],args.output)
        return
    preflight(args.machine,args.suite=='core')
    lock_path=ROOT/'work/inference.lock';lock_path.parent.mkdir(exist_ok=True)
    with lock_path.open('w') as lock:
        try: fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: raise RuntimeError('Another benchmark process owns this checkout')
        sessions=range(3) if args.suite=='core' else [0]
        failures=[]
        for session in sessions:
            for model in selected:
                cmd=[sys.executable,str(Path(__file__).resolve()),'--worker','--machine',args.machine,
                     '--allow-inference','--suite',args.suite,'--model',model['id'],'--session',str(session),'--output',str(args.output)]
                try:
                    # A parent watchdog also catches GPU stalls before the first token.
                    p=subprocess.Popen(cmd,cwd=ROOT,start_new_session=True)
                    try:
                        p.wait(timeout=129600 if args.suite=='core' else 2400)
                    except subprocess.TimeoutExpired:
                        os.killpg(p.pid, signal.SIGTERM)
                        try: p.wait(timeout=60)
                        except subprocess.TimeoutExpired:
                            os.killpg(p.pid, signal.SIGKILL); p.wait()
                        raise RuntimeError('Worker watchdog timeout; stopped task-owned process group')
                    if p.returncode: raise RuntimeError('Worker failed; exit '+str(p.returncode))
                except (subprocess.TimeoutExpired,RuntimeError) as exc:
                    failures.append(model['id'])
                    append(args.output,{'schema_version':1,'kind':'worker_failure','machine_id':args.machine,
                           'model_id':model['id'],'session':session,'suite':args.suite,'status':'failed','error':str(exc)})
                    # Stop this campaign on failure; never auto-retry or launch more GPU work.
                    break
            if failures: break
        if failures: raise SystemExit('Failed models: '+', '.join(failures))


if __name__=='__main__':
    main()
