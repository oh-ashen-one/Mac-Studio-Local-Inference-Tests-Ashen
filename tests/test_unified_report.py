import copy,json,tempfile,unittest,sys
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import unified_report

class EvidenceReportTests(unittest.TestCase):
 def fixture(self,root,model='mimo-v2.6-flash-mopd',mistral=False):
  source='config/mistral-campaign-20261003.json' if mistral else 'config/unified-campaign.json'
  plan=json.loads((ROOT/source).read_text());plan['jobs']=[{k:v for k,v in j.items() if not k.startswith('disposition') and k not in ('case_continuation','result_run_id')} for j in plan['jobs'] if j['model_id']==model];plan.pop('required_extension',None)
  spec=next(x for x in json.loads((ROOT/plan['model_lock']).read_text())['models'] if x['id']==model)
  plan['model_lock']='config/lock.json';(root/'config').mkdir();(root/'config/plan.json').write_text(json.dumps(plan));(root/'config/lock.json').write_text(json.dumps({'models':[spec]}));(root/'work').mkdir()
  state={'status':'stopped','active':None,'jobs':[{**j,'status':'pending'} for j in plan['jobs']]};return plan,state
 def save(self,root,plan,state):
  (root/'config/plan.json').write_text(json.dumps(plan));(root/'work/state.json').write_text(json.dumps(state))
 def collect(self,root):
  with patch.object(unified_report,'ROOT',root):return unified_report.collect('config/plan.json','work/state.json')
 def test_exited_saved_result_is_not_lost_in_unvisited_live_row(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);plan,state=self.fixture(root);j=next(j for j in plan['jobs'] if j['kind']=='speed' and j['output_tokens']==2048);out=root/'results'/j['id'];out.mkdir(parents=True);(out/'result.json').write_text(json.dumps({'status':'complete','decode_tok_s':37,'context_fill_s':383,'input_tokens':200000,'output_tokens':2048}));(out/'campaign-telemetry.json').write_text('[]');self.save(root,plan,state)
   r=self.collect(root);self.assertEqual(r['completed_jobs'],1);self.assertEqual(r['models'][0]['sustained']['completed'],1);self.assertEqual(state['jobs'][0]['status'],'pending')
 def test_resource_failure_and_unrun_safety_deferral_stay_unscored(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);plan,state=self.fixture(root);j=next(j for j in plan['jobs'] if j['kind']=='repo' and j['max_turns']==20 and j['attempt']==2);k=next(j for j in plan['jobs'] if j['kind']=='repo' and j['max_turns']==20 and j['attempt']==3);out=root/'results'/j['id'];out.mkdir(parents=True);(out/'result.json').write_text(json.dumps({'status':'failed','passed':False}));e='audit.json';(root/e).write_text(json.dumps({'run_id':j['id'],'disposition':'unsupported_resource','server_error':'kIOGPUCommandBufferCallbackErrorOutOfMemory','final_task_score':None}));j.update(disposition='unsupported_resource',disposition_evidence=e,disposition_reason='Actual second GPU OOM');k.update(disposition='deferred_resource_review',disposition_evidence=e,disposition_reason='Required unrun cell under safety stop');self.save(root,plan,state)
   r=self.collect(root);self.assertEqual(r['resource_limited_jobs'],1);self.assertEqual(r['deferred_jobs'],1);self.assertEqual(r['models'][0]['repo']['20']['completed'],0);self.assertEqual(r['models'][0]['repo']['20']['passed'],0)
 def test_case_helper_complete_does_not_account_for_unreviewed_group(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);plan,state=self.fixture(root,'mistral-medium35-q4',True);j=next(j for j in plan['jobs'] if j['kind']=='quality' and j['suite']=='retrieval');j.update(case_continuation='review-required',result_run_id='separate-case-output');state['jobs']=copy.deepcopy([{**j,'status':'pending'} for j in plan['jobs']]);out=root/'results'/'separate-case-output';out.mkdir(parents=True);(out/'result.json').write_text(json.dumps({'status':'complete','attempted_cases':8,'unscored_request_budget_cases':8,'completed_cases':0}));(out/'campaign-telemetry.json').write_text('[]');self.save(root,plan,state)
   r=self.collect(root);self.assertEqual(r['completed_jobs'],0);self.assertEqual(r['models'][0]['quality']['retrieval']['status'],'needs_review');self.assertTrue(r['models'][0]['quality']['retrieval']['requires_full_case_review'])
