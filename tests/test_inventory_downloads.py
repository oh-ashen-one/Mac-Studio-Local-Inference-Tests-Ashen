import json
from inventory_downloads import describe


def test_partial_shards_and_draft_component_are_not_ready_models(tmp_path):
    (tmp_path/'config.json').write_text(json.dumps({'model_type':'qwen3_5_moe','quantization':{'bits':4}}))
    (tmp_path/'model-00001-of-00004.safetensors').write_bytes(b'complete-shard-fixture')
    (tmp_path/'model-00002-of-00004.safetensors.part').write_bytes(b'partial-fixture')
    row=describe(tmp_path,'example/model','.local-staging-v2','draft')
    assert row['status']=='downloading'
    assert row['weight_files_expected']==4
    assert row['weight_files_present']==1
    assert row['missing_files']==3
    assert row['partial_files']==1
    assert row['bytes_present']==len(b'complete-shard-fixture')
    assert row['component']=='draft'
