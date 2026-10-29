"""Score a reconstruction's measurements against the reference, using USIBD LOA bands."""

from pathlib import Path

import yaml

from hausmapr import reference

# Upper bound of each band in mm (USIBD LOA, 95% confidence). Bands to be
# confirmed against the full LOA spec v3.1.
LOA_BANDS = [("LOA50", 1), ("LOA40", 5), ("LOA30", 15), ("LOA20", 50), ("LOA10", 150)]
M1_GATE_MM = 50.0


def loa_band(error_mm):
    for name, upper in LOA_BANDS:
        if error_mm <= upper:
            return name
    return "worse than LOA10"


def percentile_95(values):
    if not values:
        return None
    ordered = sorted(values)
    idx = max(0, int(round(0.95 * len(ordered))) - 1)
    return ordered[idx]


def score(reference_path, estimate_path):
    """Compare an estimate YAML (same schema, one value per key) with the reference.

    Returns rows of (key, reference_mm, estimate_mm, error_mm) and a summary dict.
    """
    _, ref = reference.load(reference_path)
    est = reference.flatten(yaml.safe_load(Path(estimate_path).read_text()))
    rows = []
    for m in ref:
        if m.mean is None or m.key not in est:
            continue
        est_vals = [v for v in est[m.key] if v is not None]
        if not est_vals:
            continue
        rows.append((m.key, m.mean, est_vals[0], abs(est_vals[0] - m.mean)))
    errors = [r[3] for r in rows]
    p95 = percentile_95(errors)
    summary = {
        "compared": len(rows),
        "reference_total": sum(1 for m in ref if m.mean is not None),
        "max_error_mm": max(errors) if errors else None,
        "p95_error_mm": p95,
        "loa": loa_band(p95) if p95 is not None else None,
        "passes_m1_gate": p95 is not None and p95 <= M1_GATE_MM,
    }
    return rows, summary
