import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import harvest_unified


def test_invalid_utf8_does_not_bypass_private_path_redaction(monkeypatch):
    machine = {'repository': '/private/test-m5/project',
               'target': 'benchmark@192.0.2.1'}
    monkeypatch.setattr(harvest_unified, 'connection', lambda: (machine, []))
    original = (b'\xefbroken\xff /private/test-m5/project/result.json '
                b'/private/test-m5/cache benchmark@192.0.2.1 192.0.2.1\x00')
    expected = (b'\xefbroken\xff <M5_REPO>/result.json '
                b'<M5_HOME>/cache <M5_SSH_TARGET> <M5_PRIVATE_HOST>\x00')
    assert harvest_unified.sanitize(original) == expected
    assert original.startswith(b'\xefbroken\xff /private/test-m5/project')


def test_utf8_and_non_private_binary_bytes_remain_intact(monkeypatch):
    machine = {'repository': '/private/test-m5/project',
               'target': 'benchmark@192.0.2.1'}
    monkeypatch.setattr(harvest_unified, 'connection', lambda: (machine, []))
    original = 'Native output: \u03bb \u4e2d'.encode('utf-8') + b'\xff\x00\xef'
    assert harvest_unified.sanitize(original) == original
