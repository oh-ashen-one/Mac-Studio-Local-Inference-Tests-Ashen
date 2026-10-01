#!/usr/bin/env python3
"""Measure a fresh 200K context fill and post-fill decode on one local model."""
import argparse,datetime,json,os,signal,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from models import digest,verify
from bench import canonical_hash,timing_summary,preflight
from first_test import shared_gpu_slot,write_json,Telemetry,stop,safety


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--allow-inference',action='store_true');p.add_argument('--model',required=True)
    p.add_argument('--tokens',type=int,default=200000);p.add_argument('--output-tokens',type=int,default=256)
    p.add_argument('--run-id',required=True);p.add_argument('--machine',choices=['studio-old','studio-new'],default='studio-new');a=p.parse_args()
    if not a.allow_inference:p.error('Explicit owner authorization and --allow-inference required')
    signal.signal(signal.SIGTERM,lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    spec=next(m for m in json.loads((ROOT/'config/models.lock.json').read_text())['models'] if m['id']==a.model)
    out=ROOT/'results'/a.run_id;out.mkdir(parents=True,exist_ok=False)
    result={'kind':'long_context','model_id':a.model,'machine_id':a.machine,'requested_input_tokens':a.tokens,'requested_output_tokens':a.output_tokens,'status':'starting','started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'model_revision':spec['revision'],'model_lock_sha256':digest(ROOT/'config/models.lock.json'),'runtime_lock_sha256':digest(ROOT/'requirements-macos-arm64.lock'),'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'prefix_cache':'fresh; no reused context','cold_definition':'Empty KV/state cache, not a cold filesystem or reboot. Model load and tokenization excluded from context-fill time.','condition':'alone','sample_count':1}
    def update():write_json(ROOT/'work/long-context-live.json',result);write_json(out/'result.json',result)
    update();process=None
    try:
        with shared_gpu_slot() as slot:
            result['gpu_slot']=slot;result['preflight']=safety(a.machine)
            result['status']='verifying_files';update();verify(spec,ROOT/'models'/a.model)
            corpus=ROOT/'work/context-corpus.txt';result['corpus_sha256']=digest(corpus)
            if spec['backend']=='dwarfstar':
                import csv,io
                result['status']='filling_context';update();started=time.perf_counter()
                cmd=[str(ROOT/'vendor/dwarfstar/ds4-bench'),'-m',str(ROOT/'models'/a.model/spec['files'][0]['path']),'--metal','--prompt-file',str(corpus),'--ctx-start',str(a.tokens),'--ctx-max',str(a.tokens),'--gen-tokens',str(a.output_tokens),'--prefill-chunk','2048']
                with (out/'native.stdout').open('w') as stdout,(out/'native.stderr').open('w') as stderr:
                    process=subprocess.Popen(cmd,cwd=ROOT/'vendor/dwarfstar',stdout=stdout,stderr=stderr,start_new_session=True)
                    with Telemetry(process.pid) as telemetry:
                        while process.poll() is None:
                            result['process_elapsed_s']=time.perf_counter()-started
                            if telemetry.rows:
                                sample=telemetry.rows[-1]
                                result['available_memory_gib']=sample['available_bytes']/1024**3
                                if sample['available_bytes']<12*1024**3 or sample['swap_bytes']-telemetry.rows[0]['swap_bytes']>2*1024**3:raise RuntimeError('Memory-pressure limit reached')
                            if result['process_elapsed_s']>7200:raise TimeoutError('Two-hour run budget reached')
                            update();time.sleep(2)
                write_json(out/'telemetry.json',telemetry.rows)
                if process.returncode:raise RuntimeError('Native benchmark failed; inspect stderr; no automatic restart')
                rows=list(csv.DictReader(io.StringIO((out/'native.stdout').read_text())))
                if len(rows)!=1 or int(rows[0]['prefill_tokens'])!=a.tokens:raise RuntimeError('Native input counter mismatch')
                row=rows[0];result.update({'status':'complete','input_tokens':a.tokens,'output_tokens':int(row['gen_tokens']),'prefill_tok_s':float(row['prefill_tps']),'context_fill_s':a.tokens/float(row['prefill_tps']),'context_fill_definition':'Derived from native full-prefill token/time counters; excludes model load','decode_tok_s':float(row['gen_steady_tps']),'native_row':row,'native_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT/'vendor/dwarfstar',text=True).strip()})
            else:
                import mlx.core as mx,psutil
                from mlx_lm import load
                from mlx_lm.generate import generate_step
                result['status']='loading_model';update();start=time.perf_counter()
                model,tokenizer,config=load(str(ROOT/'models'/a.model),return_config=True);mx.synchronize()
                result['model_load_s']=time.perf_counter()-start
                maximum=(config.get('text_config') or config).get('max_position_embeddings')
                if maximum and a.tokens+a.output_tokens>maximum:raise RuntimeError('Requested total exceeds declared model context')
                result['declared_context_limit']=maximum;result['status']='tokenizing';update()
                text=corpus.read_text();start=time.perf_counter();ids=tokenizer.encode(text,add_special_tokens=False)
                if len(ids)<a.tokens:raise RuntimeError('Corpus does not contain enough tokens')
                ids=ids[:a.tokens];result['tokenization_s']=time.perf_counter()-start;result['input_token_ids_sha256']=canonical_hash(ids)
                mx.clear_cache();mx.reset_peak_memory();mx.set_memory_limit(int(psutil.virtual_memory().total*.82))
                before=psutil.virtual_memory().available;swap=psutil.swap_memory().used
                samples=[];prefix_done_s=None;start=time.perf_counter()
                def progress(done,total):
                    nonlocal prefix_done_s
                    elapsed=time.perf_counter()-start
                    if done==total-1:prefix_done_s=elapsed
                    sample={'tokens':done,'elapsed_s':elapsed,'available_bytes':psutil.virtual_memory().available,'metal_active_bytes':mx.get_active_memory(),'swap_bytes':psutil.swap_memory().used};samples.append(sample)
                    if sample['available_bytes']<12*1024**3 or sample['swap_bytes']-swap>2*1024**3:raise RuntimeError('Memory-pressure limit reached')
                    if elapsed>7200:raise TimeoutError('Two-hour run budget reached')
                    result.update({'status':'filling_context','filled_tokens':done,'input_tokens':total,'context_elapsed_s':elapsed,'available_memory_gib':sample['available_bytes']/1024**3});update()
                tokens=[];times=[];generator=generate_step(mx.array(ids),model,max_tokens=a.output_tokens,prefill_step_size=2048,prompt_progress_callback=progress)
                try:
                    for token,_ in generator:
                        now=time.perf_counter();tokens.append(int(token));times.append(now)
                        if len(tokens)==1:result.update({'status':'decoding','context_fill_s':now-start,'filled_tokens':a.tokens});update()
                    mx.synchronize()
                finally:generator.close()
                result.update(timing_summary(start,times,time.perf_counter()))
                result.update({'status':'complete','input_tokens':a.tokens,'context_fill_s':times[0]-start,'context_fill_definition':'Full uncached input to first generated token, including the first-token step; excludes load/tokenization','prefix_prefill_s':prefix_done_s,'prefill_tok_s':(a.tokens-1)/prefix_done_s if prefix_done_s else None,'prefill_tokens_timed':a.tokens-1,'output_text':tokenizer.decode(tokens),'output_token_ids':tokens,'peak_metal_bytes':mx.get_peak_memory(),'observed_system_memory_delta_bytes':max(0,before-min(x['available_bytes'] for x in samples)),'swap_increase_bytes':psutil.swap_memory().used-swap,'kv_quantization':None,'prefill_chunk':2048,'speculation':False,'settings':'Fixed-token decode continues through EOS for comparable work; this is not a correctness score.'})
                write_json(out/'prefill-timeline.json',samples)
            result['finished_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();update()
    except BaseException as exc:
        result['status']='failed';result['error']=str(exc).replace(str(ROOT),'<repo>');update();raise
    finally:stop(process)


if __name__=='__main__':main()
