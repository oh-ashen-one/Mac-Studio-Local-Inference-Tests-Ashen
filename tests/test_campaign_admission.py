import unittest,tempfile,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from campaign_admission import pending_disposition,download_snapshot,extension_pending,OMITTED
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
  self.assertFalse(extension_pending(ROOT,new))
 def test_extension_full_matrix(self):
  ext=json.loads((ROOT/'config/unified-extension-20261003.json').read_text())
  self.assertEqual(len(ext['jobs']),156)
  self.assertEqual(ext['status'],'cancelled_by_owner_scope')
  self.assertTrue(all(j['disposition']==OMITTED for j in ext['jobs']))
  for m in ext['models']:
   jobs=[j for j in ext['jobs'] if j['model_id']==m['id']];self.assertEqual(len(jobs),39)
   self.assertEqual(sum(j['kind']=='speed' for j in jobs),23)
if __name__=='__main__':unittest.main()
