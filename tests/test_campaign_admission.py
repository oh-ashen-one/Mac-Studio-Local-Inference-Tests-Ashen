import unittest,tempfile,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from campaign_admission import pending_disposition,download_snapshot,extension_pending,OMITTED,reviewed_disposition,RESOURCE,DEFERRED,gpu_safety_failures
ROOT=Path(__file__).resolve().parents[1]
class AdmissionTests(unittest.TestCase):
 def test_existing_evidence_never_omitted(self):
  j={'disposition':OMITTED}
  self.assertIsNone(pending_disposition(j,True));self.assertEqual(pending_disposition(j,False),OMITTED)
 def test_partial_and_staging_block_without_mutation(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);(p/'.local-staging-test').mkdir();f=p/'.local-staging-test/a.part';f.write_bytes(b'abc')
   a,b=download_snapshot([p]);self.assertEqual(len(b),2);self.assertEqual(f.read_bytes(),b'abc')
   f.write_bytes(b'abcdef');self.assertNotEqual(a,download_snapshot([p])[0])
 def test_original_jobs_and_budgets_preserved(self):
  old=json.loads((ROOT/'config/archive/unified-campaign-pre-owner-scope-20261003.json').read_text());new=json.loads((ROOT/'config/unified-campaign.json').read_text())
  self.assertEqual(len(new['jobs']),234)
  for a,b in zip(old['jobs'],new['jobs']):self.assertEqual(a,{k:v for k,v in b.items() if not k.startswith('disposition')})
  omitted=[j for j in new['jobs'] if j.get('disposition')==OMITTED];self.assertEqual(len(omitted),18);self.assertTrue(all(j['model_id'] in ('qwen38-q4-gguf','qwen3.6-35b-a3b-vl-mtp-mxfp8') for j in omitted))
  self.assertTrue(extension_pending(ROOT,new))
 def test_extension_full_matrix(self):
  ext=json.loads((ROOT/'config/unified-extension-20261003.json').read_text())
  self.assertEqual(len(ext['jobs']),156)
  self.assertEqual(ext['status'],'cancelled_by_owner_scope')
  self.assertTrue(all(j['disposition']==OMITTED for j in ext['jobs']))
  for m in ext['models']:
   jobs=[j for j in ext['jobs'] if j['model_id']==m['id']];self.assertEqual(len(jobs),39)
   self.assertEqual(sum(j['kind']=='speed' for j in jobs),23)
if __name__=='__main__':unittest.main()

class ResourceReviewTests(unittest.TestCase):
 def test_only_preserved_failed_resource_attempt_can_be_handled(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);(root/'audit.json').write_text(json.dumps({'disposition':RESOURCE,'server_error':'kIOGPUCommandBufferCallbackErrorOutOfMemory','run_id':'failed-run','final_task_score':None}))
   job={'id':'failed-run','disposition':RESOURCE,'disposition_evidence':'audit.json'}
   self.assertEqual(reviewed_disposition(root,job,{'status':'failed'}),RESOURCE)
   with self.assertRaises(RuntimeError):reviewed_disposition(root,job,{'status':'complete'})
 def test_deferred_work_is_not_a_completed_or_unsupported_trial(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);(root/'audit.json').write_text(json.dumps({'disposition':RESOURCE,'server_error':'kIOGPUCommandBufferCallbackErrorOutOfMemory'}))
   job={'id':'unrun','disposition':DEFERRED,'disposition_evidence':'audit.json'}
   self.assertEqual(reviewed_disposition(root,job,None),DEFERRED)
   with self.assertRaises(RuntimeError):reviewed_disposition(root,job,{'status':'complete'})
 def test_two_gpu_failures_are_counted_without_erasing_attempts(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);(root/'work').mkdir();p=root/'work/compute-safety-events.json'
   p.write_text(json.dumps({'events':[{'run_id':'first','count_toward_two_failure_stop':True},{'run_id':'second','count_toward_two_failure_stop':True}]}))
   self.assertEqual(gpu_safety_failures(root),2)
   self.assertEqual(len(json.loads(p.read_text())['events']),2)
