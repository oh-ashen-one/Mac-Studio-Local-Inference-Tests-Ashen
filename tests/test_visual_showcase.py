import hashlib
import json
import struct
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import build_visual_showcase
import preview


def test_showcase_percentages_are_bound_to_five_run_frozen_measurements():
    d=build_visual_showcase.build_data()
    assert len(d['models'])==5
    assert d['source_sha256']==hashlib.sha256((ROOT/'results/research-report-20261004/source-summaries.json').read_bytes()).hexdigest()
    for p in d['pairs']:
        assert p['ours']['n']==5
        assert p['context']==p['reference']['context_tokens']
        assert p['reported_rate_increase_percent']==(p['ours']['median']/p['reference']['decode_tps']-1)*100
    assert d['scope']==dict(completed=183,unscored=11,owner_omitted=1,required_remaining=0)
    assert d['market_values']['dgx_spark_short_serving']==37.3
    assert d['market_values']['rtx5090_8k_mtp3_reported']==98.2
    market=next(c for c in d['cards'] if c['id']=='market')
    assert 'Prompt lengths, precision, acceleration and timers differ' in market['alt']
    assert market['brands']==['apple','nvidia','qwen']


def test_every_infographic_matches_manifest_and_has_reviewed_high_resolution():
    d=build_visual_showcase.build_data();manifest=json.loads((ROOT/'outputs/visual-showcase-manifest.json').read_text())
    assert len(d['cards'])==5
    for card in d['cards']:
        p=ROOT/'viewer/assets'/Path(card['png']).name
        assert hashlib.sha256(p.read_bytes()).hexdigest()==manifest['graphics'][card['id']]['png']
        assert struct.unpack('>II',p.read_bytes()[16:24])==(card['width'],card['height'])
        assert card['width']>=1500
        for brand in card['brands']:
            logo=ROOT/'viewer/assets/logos'/(brand+'.svg')
            assert logo.is_file() and '<script' not in logo.read_text().lower()


def test_asset_route_cannot_read_private_files_or_escape_through_symlinks(tmp_path,monkeypatch):
    monkeypatch.setattr(preview,'ROOT',tmp_path)
    assets=tmp_path/'viewer/assets';assets.mkdir(parents=True)
    (assets/'chart.png').write_bytes(b'public')
    private=tmp_path/'config';private.mkdir();(private/'machines.local.json').write_text('private')
    (assets/'escape.json').symlink_to(private/'machines.local.json')
    assert preview.asset_file('/assets/chart.png')==assets/'chart.png'
    for path in ['/assets/../../config/machines.local.json','/assets/%2e%2e/%2e%2e/config/machines.local.json',
                 '/assets/%2Fetc/passwd','/assets/escape.json','/config/machines.local.json','/assets/missing.png']:
        assert preview.asset_file(path) is None


def test_full_research_page_preserves_retained_workload_counts():
    d=build_visual_showcase.build_data()
    assert d['study_counts']==dict(models=5,cold_speed_runs=100,sustained_runs=15,coding_cases=820,serving_requests=900,replay_requests=840,structured_cases=120,retrieval_attempts=45)
    assert len(d['historical_models'])==2
    assert all(m['historical_comparison'] for m in d['historical_models'])
    assert all(m['completed_jobs']==30 and m['omitted_jobs']==9 for m in d['historical_models'])


def test_optional_portfolio_build_preview_stays_inside_public_directory(tmp_path):
    public=tmp_path/'public';public.mkdir()
    (public/'index.html').write_text('study')
    (public/'chart.js').write_text('public chart')
    private=tmp_path/'private.json';private.write_text('private')
    (public/'escape.json').symlink_to(private)
    assert preview.site_file('/portfolio/benchmark/mac-studio',public)==public/'index.html'
    assert preview.site_file('/portfolio/chart.js',public)==public/'chart.js'
    assert preview.site_file('/portfolio/benchmark',None) is None
    for path in ['/portfolio/../private.json','/portfolio/%2e%2e/private.json',
                 '/portfolio/%2Fetc/passwd','/portfolio/.env','/portfolio/escape.json',
                 '/portfolio/missing.js','/private.json']:
        assert preview.site_file(path,public) is None


def test_full_research_quality_limits_are_not_zero_accuracy_scores():
    d=build_visual_showcase.build_data();rows={q['id']:q for q in d['quality_results']}
    m=rows['mistral-medium35-q4']
    assert m['retrieval']['passed'] is None and not m['retrieval']['scored']
    assert m['retrieval']['attempted']==9
    assert m['repo']['8']['passed'] is None and m['repo']['8']['budget_limited']==5
    assert m['repo']['20']['passed'] is None and m['repo']['20']['budget_limited']==3
    mi=rows['mimo-v2.6-flash-mopd']['repo']['20']
    assert mi['passed'] is None and mi['resource_limited']==2 and mi['owner_omitted']==1
