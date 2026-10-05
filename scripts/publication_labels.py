"""Presentation corrections only; never changes model/runtime provenance locks."""
QWEN36 = 'qwen3.6-35b-a3b-vl-mtp-mxfp8'
CORRECTED_NAME = 'Qwen 3.6 35B A3B · 4-bit MLX (affine; 8-bit gates)'
CORRECTED_PRECISION = '4-bit affine MLX, group size 64; gate/shared-expert-gate overrides use 8 bits'
def public_spec(spec):
    if spec['id'] != QWEN36:
        return dict(spec)
    return dict(spec, display_name=CORRECTED_NAME, quantization=CORRECTED_PRECISION,
                original_catalog_precision=spec.get('quantization'),
                precision_correction='docs/QWEN36-PRECISION-CORRECTION.md')
