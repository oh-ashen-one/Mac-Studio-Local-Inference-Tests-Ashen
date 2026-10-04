"""Hash-bound selection of untouched retrieval cases; no runtime imports."""
import ast
import datetime
import hashlib
import json
import subprocess
from pathlib import Path

MODEL = 'mistral-medium35-q4'
PARENT = 'u20261003-mistral35-retrieval'
DEADLINE_ERROR = 'Declared per-request deadline exceeded'
CASE_IDS = [f'needle-{position}-{seed}' for seed in [101, 202, 303]
            for position in [0.1, 0.5, 0.9]]
POLICY = {'input_tokens': 200000, 'output_tokens': 512, 'temperature': 0,
          'seed_base': 1729, 'request_timeout_seconds': 900,
          'cache_sequences': 0, 'context_per_slot': 262144, 'slots': 1}
FROZEN_FUNCTIONS = {'scripts/unified_quality.py': ['retrieval_packet'],
                    'scripts/unified_server.py': ['chat', 'chat_payload', 'server'],
                    'scripts/first_test.py': ['safety', 'shared_gpu_slot', 'Telemetry']}
FROZEN_FILES = ['scripts/unified_server.py', 'scripts/first_test.py',
                'scripts/bench.py', 'scripts/models.py', 'scripts/model_registry.py']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_function_sha(source, name):
    node = next(n for n in ast.parse(source).body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.name == name)
    return hashlib.sha256(ast.get_source_segment(source, node).encode()).hexdigest()


def function_sha(path, name):
    return source_function_sha(Path(path).read_text(), name)


def original_function_sha(root, commit, path, name):
    source = subprocess.check_output(['git', 'show', commit + ':' + path], cwd=root).decode()
    return source_function_sha(source, name)


def validate(root, relative, model_id, run_id=None, now=None):
    root = Path(root)
    relative = Path(relative)
    if relative.is_absolute() or '..' in relative.parts:
        raise RuntimeError('Continuation manifest must be task-relative')
    m = json.loads((root / relative).read_text())
    if (model_id != MODEL or m.get('model_id') != MODEL
            or m.get('parent_run_id') != PARENT
            or m.get('kind') != 'reviewed_retrieval_remaining_cases'
            or m.get('request_policy') != POLICY
            or m.get('remaining_case_ids') != CASE_IDS[1:]
            or m.get('model_lock') != 'config/mistral-models.lock.json'
            or m.get('original_job_budget_seconds') != 86400):
        raise RuntimeError('Continuation cannot alter the original retrieval cases or budgets')
    if run_id is not None and run_id != m.get('continuation_run_id'):
        raise RuntimeError('Continuation output identity mismatch')
    if m.get('continuation_run_id') != PARENT + '-remaining-r1':
        raise RuntimeError('Unexpected continuation output identity')
    parent = root / 'results' / PARENT
    result = json.loads((parent / 'result.json').read_text())
    audit = json.loads((parent / 'completion-audit.json').read_text())
    request = json.loads((parent / CASE_IDS[0] / 'request.json').read_text())
    pins = {'parent_result_sha256': parent / 'result.json',
            'parent_audit_sha256': parent / 'completion-audit.json',
            'first_case_request_sha256': parent / CASE_IDS[0] / 'request.json',
            'model_lock_sha256': root / m['model_lock'],
            'corpus_sha256': root / 'work/context-corpus.txt'}
    if any(sha(path) != m.get(key) for key, path in pins.items()):
        raise RuntimeError('Continuation evidence or frozen input hash changed')
    if (result.get('kind') != 'useful_work' or result.get('suite') != 'retrieval'
            or result.get('status') != 'failed' or result.get('error') != DEADLINE_ERROR
            or result.get('model_id') != MODEL
            or result.get('planned_cases') != 9
            or result.get('cases') != [] or result.get('active_case') != CASE_IDS[0]
            or result.get('model_lock_sha256') != m['model_lock_sha256']
            or audit.get('kind') != 'retrieval_individual_case_request_budget_review'
            or audit.get('run_id') != PARENT or audit.get('attempted_case_id') != CASE_IDS[0]
            or audit.get('result_sha256') != m['parent_result_sha256']
            or audit.get('case_request_sha256') != m['first_case_request_sha256']
            or audit.get('completed_responses') != 0
            or audit.get('request_timeout_seconds') != 900
            or audit.get('final_task_score', 'missing') is not None
            or audit.get('actual_final_server_usage', 'missing') is not None
            or audit.get('whole_suite_disposition', 'missing') is not None
            or audit.get('new_gpu_safety_event') is not False
            or audit.get('owned_driver_and_workers_exited') is not True
            or audit.get('required_unrun_case_ids') != CASE_IDS[1:]
            or request.get('case', {}).get('seed') != 101
            or request.get('case', {}).get('position') != 0.1
            or not 200000 <= request.get('case', {}).get('actual_prompt_tokens_preflight', 0) <= 200032
            or audit.get('native_template_calibration_tokens') != request['case']['actual_prompt_tokens_preflight']):
        raise RuntimeError('Only the independently audited first attempted case can be excluded')
    function_table = m.get('frozen_function_sha256', {})
    if {path: sorted(names) for path, names in function_table.items()} != {path: sorted(names) for path, names in FROZEN_FUNCTIONS.items()}:
        raise RuntimeError('Missing frozen request/runtime/guard source proof')
    for path, functions in function_table.items():
        for name, expected in functions.items():
            if (function_sha(root / path, name) != expected
                    or original_function_sha(root, result['source_commit'], path, name) != expected):
                raise RuntimeError('Frozen request builder, runtime adapter or guard changed')
    file_table = m.get('frozen_file_sha256', {})
    if sorted(file_table) != sorted(FROZEN_FILES):
        raise RuntimeError('Missing complete frozen adapter/guard file proof')
    for path, expected in file_table.items():
        original = subprocess.check_output(['git', 'show', result['source_commit'] + ':' + path], cwd=root)
        if sha(root / path) != expected or hashlib.sha256(original).hexdigest() != expected:
            raise RuntimeError('Frozen adapter or guard file changed')
    start = datetime.datetime.fromisoformat(result['started_at_utc']).replace(microsecond=0)
    deadline = start + datetime.timedelta(seconds=86400)
    if m.get('original_job_deadline_utc') != deadline.isoformat():
        raise RuntimeError('Original retrieval job deadline cannot be extended')
    now = now or datetime.datetime.now(datetime.timezone.utc)
    remaining = (deadline - now).total_seconds()
    if remaining <= 0:
        raise RuntimeError('Original retrieval group job budget exhausted')
    return {**m, 'remaining_job_budget_seconds': remaining}


def case_budget_failure(exc, ident, case, elapsed, request_sha256):
    if type(exc) is not TimeoutError or str(exc) != DEADLINE_ERROR:
        raise exc
    return {'case_id': ident, 'seed': case['seed'], 'expected': case['expected'],
            'passed': None, 'status': 'unscored_request_budget', 'error': str(exc),
            'request_timeout_seconds': 900, 'wall_s': elapsed,
            'request_sha256': request_sha256,
            'native_template_calibration_tokens': case['actual_prompt_tokens_preflight'],
            'actual_final_server_usage': None, 'final_task_score': None}


def partial_stream_observation(exc):
    """Retain already observed text without modifying the frozen HTTP client."""
    frame = exc.__traceback__
    while frame is not None:
        code = frame.tb_frame.f_code
        if code.co_name == 'chat' and Path(code.co_filename).name == 'unified_server.py':
            state = frame.tb_frame.f_locals
            return {'available': True, 'scope': 'Partial client state at actual error; not a complete response or final usage.',
                    'output_observed': state.get('text'), 'reasoning_observed': state.get('reasoning'),
                    'usage_so_far': state.get('usage'), 'first_output_s': state.get('first'),
                    'finish_reason_so_far': state.get('finish'), 'stream_chunks_observed': state.get('chunks')}
        frame = frame.tb_next
    return {'available': False, 'scope': 'No frozen chat frame available; final response and usage unknown.'}


def continuation_counts(cases):
    return {'attempted_cases': len(cases),
            'completed_cases': sum('usage' in c for c in cases),
            'passed_cases': sum(c.get('passed') is True for c in cases),
            'unscored_request_budget_cases': sum(c.get('status') == 'unscored_request_budget' for c in cases)}
