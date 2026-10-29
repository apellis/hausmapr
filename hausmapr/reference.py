"""Load reference (ground-truth) room measurements and check pass-to-pass agreement."""

from dataclasses import dataclass
from pathlib import Path

import yaml

MM_PER_INCH = 25.4
PASS_TOLERANCE_MM = 5.0
OPENING_DIMS = ("offset", "width", "height", "sill")
FEATURE_DIMS = ("width", "depth", "height")


@dataclass
class Measurement:
    key: str  # e.g. "walls/C1-C2" or "openings/door_main/width"
    passes: list  # readings in mm, None where missing

    @property
    def values(self):
        return [p for p in self.passes if p is not None]

    @property
    def mean(self):
        vals = self.values
        return sum(vals) / len(vals) if vals else None

    @property
    def spread(self):
        vals = self.values
        return max(vals) - min(vals) if len(vals) > 1 else None


def _to_mm(passes, units):
    if units not in ("mm", "in"):
        raise ValueError(f"units must be 'mm' or 'in', got {units!r}")
    scale = MM_PER_INCH if units == "in" else 1.0
    return [None if p is None else float(p) * scale for p in passes]


def flatten(doc):
    """Turn a reference or estimate YAML document into {key: [readings in mm]}."""
    units = doc.get("units", "mm")
    out = {}
    for section in ("walls", "diagonals", "ceiling_height"):
        for name, passes in (doc.get(section) or {}).items():
            out[f"{section}/{name}"] = _to_mm(_as_list(passes), units)
    for opening in doc.get("openings") or []:
        for dim in OPENING_DIMS:
            if dim in opening:
                out[f"openings/{opening['id']}/{dim}"] = _to_mm(_as_list(opening[dim]), units)
    for feature in doc.get("features") or []:
        for dim in FEATURE_DIMS:
            if dim in feature:
                out[f"features/{feature['id']}/{dim}"] = _to_mm(_as_list(feature[dim]), units)
    return out


def _as_list(value):
    return value if isinstance(value, list) else [value]


def load(path):
    doc = yaml.safe_load(Path(path).read_text())
    return doc, [Measurement(k, v) for k, v in flatten(doc).items()]


def check(measurements, tolerance_mm=PASS_TOLERANCE_MM):
    """Return (missing, disagreeing) measurement lists."""
    missing = [m for m in measurements if len(m.values) < 2]
    disagreeing = [m for m in measurements if m.spread is not None and m.spread > tolerance_mm]
    return missing, disagreeing
