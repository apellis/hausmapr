import textwrap

import pytest

from hausmapr import evaluate, reference

REF = textwrap.dedent(
    """
    room: test
    units: mm
    walls:
      C1-C2: [3000, 3002]
      C2-C3: [4000, 4010]
    ceiling_height:
      centre: [2440, null]
    openings:
      - id: door
        width: [810, 812]
    """
)


@pytest.fixture
def ref_path(tmp_path):
    path = tmp_path / "ref.yaml"
    path.write_text(REF)
    return path


def test_check_flags_missing_and_disagreeing(ref_path):
    _, ms = reference.load(ref_path)
    missing, disagreeing = reference.check(ms)
    assert [m.key for m in missing] == ["ceiling_height/centre"]
    assert [m.key for m in disagreeing] == ["walls/C2-C3"]


def test_inches_convert_to_mm(tmp_path):
    path = tmp_path / "in.yaml"
    path.write_text("units: in\nwalls:\n  C1-C2: [100, 100]\n")
    _, ms = reference.load(path)
    assert ms[0].mean == pytest.approx(2540.0)


def test_score_reports_loa_and_gate(ref_path, tmp_path):
    est = tmp_path / "est.yaml"
    est.write_text("units: mm\nwalls:\n  C1-C2: 3021\n  C2-C3: 3965\nopenings:\n  - id: door\n    width: 800\n")
    rows, summary = evaluate.score(ref_path, est)
    assert summary["compared"] == 3
    assert summary["max_error_mm"] == pytest.approx(40.0)
    assert summary["loa"] == "LOA20"
    assert summary["passes_m1_gate"]


def test_loa_band_edges():
    assert evaluate.loa_band(0.5) == "LOA50"
    assert evaluate.loa_band(15) == "LOA30"
    assert evaluate.loa_band(51) == "LOA10"
    assert evaluate.loa_band(200) == "worse than LOA10"


def test_marker_pdf_renders_and_is_detectable(tmp_path):
    import cv2

    from hausmapr import markers

    pdf = tmp_path / "board.pdf"
    markers.render_letter_pdf(pdf)
    assert pdf.stat().st_size > 0

    art = markers.board().generateImage((600, 800), marginSize=20)
    corners, ids, _, _ = cv2.aruco.CharucoDetector(markers.board()).detectBoard(art)
    assert ids is not None and len(ids) == (markers.SQUARES_X - 1) * (markers.SQUARES_Y - 1)
