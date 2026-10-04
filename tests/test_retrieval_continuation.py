import datetime
import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import retrieval_continuation as rc
import unified_campaign as campaign


@pytest.fixture
def reviewed(tmp_path, monkeypatch):
    root = tmp_path
    for relative, names in rc.FROZEN_FUNCTIONS.items():
        p = root / relative
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('\n'.join(('class ' if name == 'Telemetry' else 'def ') + name
                               + (':' if name == 'Telemetry' else '():') + '\n    pass\n'
                               for name in names))
    for relative in rc.FROZEN_FILES:
        p = root / relative
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists():
            p.write_text('pass\n')
    (root / 'config').mkdir()
    lock = root / 'config/mistral-models.lock.json'
    lock.write_text('{"fixture": true}')
    (root / 'work').mkdir()
    corpus = root / 'work/context-corpus.txt'
    corpus.write_text('frozen fixture corpus')
    parent = root / 'results' / rc.PARENT
    (parent / rc.CASE_IDS[0]).mkdir(parents=True)
    start = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0) - datetime.timedelta(minutes=30)
    result = {'kind': 'useful_work', 'model_id': rc.MODEL, 'suite': 'retrieval',
              'status': 'failed', 'error': rc.DEADLINE_ERROR, 'cases': [], 'planned_cases': 9,
              'active_case': rc.CASE_IDS[0], 'model_lock_sha256': rc.sha(lock),
              'source_commit': 'test-source', 'started_at_utc': start.isoformat()}
    (parent / 'result.json').write_text(json.dumps(result))
    request = {'case': {'seed': 101, 'position': 0.1, 'actual_prompt_tokens_preflight': 200014}}
    request_path = parent / rc.CASE_IDS[0] / 'request.json'
    request_path.write_text(json.dumps(request))
    audit = {'kind': 'retrieval_individual_case_request_budget_review', 'run_id': rc.PARENT,
             'attempted_case_id': rc.CASE_IDS[0], 'result_sha256': rc.sha(parent / 'result.json'),
             'case_request_sha256': rc.sha(request_path), 'completed_responses': 0,
             'request_timeout_seconds': 900, 'final_task_score': None,
             'actual_final_server_usage': None, 'whole_suite_disposition': None,
             'new_gpu_safety_event': False, 'owned_driver_and_workers_exited': True,
             'native_template_calibration_tokens': 200014, 'required_unrun_case_ids': rc.CASE_IDS[1:]}
    (parent / 'completion-audit.json').write_text(json.dumps(audit))
    manifest = {'kind': 'reviewed_retrieval_remaining_cases', 'model_id': rc.MODEL,
                'parent_run_id': rc.PARENT, 'continuation_run_id': rc.PARENT + '-remaining-r1',
                'request_policy': rc.POLICY, 'remaining_case_ids': rc.CASE_IDS[1:],
                'original_job_budget_seconds': 86400,
                'original_job_deadline_utc': (start + datetime.timedelta(seconds=86400)).isoformat(),
                'model_lock': 'config/mistral-models.lock.json', 'model_lock_sha256': rc.sha(lock),
                'corpus_sha256': rc.sha(corpus), 'parent_result_sha256': rc.sha(parent / 'result.json'),
                'parent_audit_sha256': rc.sha(parent / 'completion-audit.json'),
                'first_case_request_sha256': rc.sha(request_path),
                'frozen_function_sha256': {path: {name: rc.function_sha(root / path, name) for name in names}
                                          for path, names in rc.FROZEN_FUNCTIONS.items()},
                'frozen_file_sha256': {path: rc.sha(root / path) for path in rc.FROZEN_FILES}}
    relative = 'config/review.json'
    (root / relative).write_text(json.dumps(manifest))
    monkeypatch.setattr(rc.subprocess, 'check_output', lambda args, **kw:
                        (root / args[2].split(':', 1)[1]).read_bytes())
    return root, relative, manifest, start


def test_only_eight_untouched_cases_and_original_deadline_are_admitted(reviewed):
    root, path, m, start = reviewed
    x = rc.validate(root, path, rc.MODEL, m['continuation_run_id'], start + datetime.timedelta(minutes=30))
    assert x['remaining_case_ids'] == rc.CASE_IDS[1:]
    assert x['remaining_job_budget_seconds'] == 84600
    assert rc.CASE_IDS[0] not in x['remaining_case_ids']


@pytest.mark.parametrize('change', [
    {'remaining_case_ids': rc.CASE_IDS}, {'remaining_case_ids': rc.CASE_IDS[2:]},
    {'original_job_budget_seconds': 90000}, {'request_policy': {**rc.POLICY, 'request_timeout_seconds': 7200}},
    {'request_policy': {**rc.POLICY, 'input_tokens': 80000}}, {'frozen_function_sha256': {}},
    {'frozen_file_sha256': {}}, {'continuation_run_id': 'retry-parent'},
])
def test_retry_omission_budget_input_or_source_policy_changes_are_rejected(reviewed, change):
    root, path, m, _ = reviewed
    (root / path).write_text(json.dumps({**m, **change}))
    with pytest.raises(RuntimeError):
        rc.validate(root, path, rc.MODEL)


def test_modified_actual_evidence_and_changed_source_are_rejected(reviewed):
    root, path, m, _ = reviewed
    file = root / 'results' / rc.PARENT / 'result.json'
    original = file.read_bytes()
    file.write_bytes(original + b' ')
    with pytest.raises(RuntimeError, match='hash changed'):
        rc.validate(root, path, rc.MODEL)
    file.write_bytes(original)
    (root / 'scripts/unified_server.py').write_text('def chat():\n    return "changed"\n')
    with pytest.raises((RuntimeError, StopIteration)):
        rc.validate(root, path, rc.MODEL)


def test_expired_original_budget_or_different_identity_cannot_start(reviewed):
    root, path, m, start = reviewed
    with pytest.raises(RuntimeError, match='budget exhausted'):
        rc.validate(root, path, rc.MODEL, now=start + datetime.timedelta(days=1))
    with pytest.raises(RuntimeError):
        rc.validate(root, path, 'different-model')
    with pytest.raises(RuntimeError, match='identity mismatch'):
        rc.validate(root, path, rc.MODEL, 'different-output')


def test_case_timeout_is_unscored_and_never_fabricates_final_usage():
    case = {'seed': 101, 'expected': {'answer': 'fixture'}, 'actual_prompt_tokens_preflight': 200014}
    row = rc.case_budget_failure(TimeoutError(rc.DEADLINE_ERROR), rc.CASE_IDS[1], case, 905, 'request-sha')
    assert row['passed'] is None and row['final_task_score'] is None and row['actual_final_server_usage'] is None
    assert 'usage' not in row
    assert rc.continuation_counts([row, {'usage': {}, 'passed': True}, {'usage': {}, 'passed': False}]) == {
        'attempted_cases': 3, 'completed_cases': 2, 'passed_cases': 1, 'unscored_request_budget_cases': 1}
    for error in [RuntimeError(rc.DEADLINE_ERROR), TimeoutError('GPU failure'), ValueError('Memory guard')]:
        with pytest.raises(type(error)):
            rc.case_budget_failure(error, rc.CASE_IDS[1], case, 905, 'request-sha')


def test_observed_partial_text_is_retained_without_fabricating_completion():
    namespace = {}
    code = "def chat():\n    text='partial answer'\n    reasoning=''\n    usage={}\n    first=899.5\n    chunks=[{'elapsed_s':899.5}]\n    finish=None\n    raise TimeoutError('Declared per-request deadline exceeded')\n"
    exec(compile(code, 'scripts/unified_server.py', 'exec'), namespace)
    try:
        namespace['chat']()
    except TimeoutError as error:
        saved = rc.partial_stream_observation(error)
    assert saved['available'] and saved['output_observed'] == 'partial answer'
    assert saved['usage_so_far'] == {} and saved['finish_reason_so_far'] is None
    assert 'actual_final_server_usage' not in saved


def test_command_retains_frozen_profile_and_default_jobs_unchanged(reviewed, monkeypatch):
    root, path, m, _ = reviewed
    monkeypatch.setattr(campaign, 'ROOT', root)
    job = {'id': rc.PARENT, 'kind': 'quality', 'suite': 'retrieval', 'model_id': rc.MODEL,
           'result_run_id': m['continuation_run_id'], 'case_continuation': path}
    command, budget = campaign.command_for(job, {'runtime': 'llama-cpp', 'extension': True}, m['model_lock'])
    assert '--retrieval-continuation' in command and m['continuation_run_id'] in command and 0 < budget < 86400
    ordinary = {k: v for k, v in job.items() if k not in ['result_run_id', 'case_continuation']}
    command, budget = campaign.command_for(ordinary, {'runtime': 'llama-cpp'})
    assert budget == 86400 and '--retrieval-continuation' not in command and rc.PARENT in command
    with pytest.raises(RuntimeError):
        campaign.command_for({**job, 'suite': 'humaneval'}, {'runtime': 'llama-cpp'})


@pytest.fixture
def all_nine_budget_cases(reviewed):
    root, path, m, start = reviewed
    folder = root / 'results' / m['continuation_run_id']
    folder.mkdir()
    profile = {'runtime_lock_sha256': 'runtime', 'native_binary_sha256': 'binary',
               'requested_context_per_slot': 262144, 'slots': 1, 'prompt_cache_sequences': 0}
    (root / 'results' / rc.PARENT / 'server-config.json').write_text(json.dumps(profile))
    (folder / 'server-config.json').write_text(json.dumps(profile))
    proofs = [{'case_id': rc.CASE_IDS[0], 'request_sha256': m['first_case_request_sha256']}]
    cases = []
    for ident in rc.CASE_IDS[1:]:
        p = folder / ident
        p.mkdir()
        case = {'seed': int(ident.rsplit('-', 1)[1]), 'position': float(ident.split('-')[1]),
                'actual_prompt_tokens_preflight': 200014, 'expected': {'answer': 'fixture'}}
        (p / 'request.json').write_text(json.dumps({'case': case}))
        row = rc.case_budget_failure(TimeoutError(rc.DEADLINE_ERROR), ident, case, 902, rc.sha(p / 'request.json'))
        (p / 'request-budget-failure.json').write_text(json.dumps(row))
        cases.append(row)
        proofs.append({'case_id': ident, 'request_sha256': row['request_sha256'],
                       'failure_sha256': rc.sha(p / 'request-budget-failure.json')})
    result = {'status': 'complete', 'requires_completion_review': True,
              'attempted_cases': 8, 'completed_cases': 0, 'unscored_request_budget_cases': 8,
              'cases': cases, 'model_lock_sha256': m['model_lock_sha256'],
              'finished_at_utc': (start + datetime.timedelta(hours=3)).isoformat()}
    (folder / 'result.json').write_text(json.dumps(result))
    disposition = 'unsupported_request_budget_cases'
    note = {'kind': 'retrieval_all_original_cases_request_budget_review', 'disposition': disposition,
            'run_id': rc.PARENT, 'continuation_run_id': m['continuation_run_id'],
            'case_ids': rc.CASE_IDS, 'attempted_cases': 9, 'completed_responses': 0,
            'unscored_cases': 9, 'final_task_score': None, 'actual_final_server_usage': None,
            'request_timeout_seconds': 900, 'new_gpu_safety_events': 0,
            'owned_driver_and_workers_exited': True, 'parent_result_sha256': m['parent_result_sha256'],
            'continuation_result_sha256': rc.sha(folder / 'result.json'), 'cases': proofs}
    job = {'id': rc.PARENT, 'kind': 'quality', 'suite': 'retrieval', 'model_id': rc.MODEL,
           'case_continuation': path, 'result_run_id': m['continuation_run_id']}
    return root, job, note, disposition, folder


def test_all_nine_real_case_proofs_required_before_group_accounting(all_nine_budget_cases):
    root, job, note, disposition, _ = all_nine_budget_cases
    assert rc.review_all_budget_cases(root, job, note, disposition) == disposition
    for change in [{'attempted_cases': 1}, {'case_ids': rc.CASE_IDS[:1]},
                   {'cases': note['cases'][:-1]}, {'final_task_score': False},
                   {'request_timeout_seconds': 7200}, {'completed_responses': 1},
                   {'new_gpu_safety_events': 1}]:
        with pytest.raises(RuntimeError):
            rc.review_all_budget_cases(root, job, {**note, **change}, disposition)


def test_missing_or_modified_case_cannot_inherit_other_timeout(all_nine_budget_cases):
    root, job, note, disposition, folder = all_nine_budget_cases
    (folder / rc.CASE_IDS[-1] / 'request.json').write_text('{"different":true}')
    with pytest.raises(RuntimeError, match='request hash changed'):
        rc.review_all_budget_cases(root, job, note, disposition)


def test_altered_native_cache_profile_cannot_pass_case_review(all_nine_budget_cases):
    root, job, note, disposition, folder = all_nine_budget_cases
    p = folder / 'server-config.json';profile = json.loads(p.read_text());profile['slots'] = 2
    p.write_text(json.dumps(profile))
    with pytest.raises(RuntimeError, match='profile changed'):
        rc.review_all_budget_cases(root, job, note, disposition)


def test_other_quality_suite_cannot_use_retrieval_case_disposition(all_nine_budget_cases):
    root, job, note, disposition, _ = all_nine_budget_cases
    with pytest.raises(RuntimeError):
        rc.review_all_budget_cases(root, {**job, 'suite': 'humaneval'}, note, disposition)
