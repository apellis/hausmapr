# hausmapr

Turn phone photos of a home's interior into a measured 3D model and the deliverables a design-build firm expects (E57 point cloud, DXF/PDF plans, later IFC).

Spec, feasibility study and phased plan: https://claude.ai/artifact/MbpP9tr2LCzGXUtAAFG28R

## Where we are

Milestone M0: build reference measurements for three test rooms, then M1: reconstruct one room offline and score it against them (gate: 95th-percentile error within 50 mm, i.e. LOA20).

- [M0 supplies](docs/m0-supplies.md)
- [M0 measurement protocol](docs/m0-measurement-protocol.md)
- [M1 photo capture protocol](docs/m1-capture-protocol.md)
- Printable scale board: [markers/charuco_letter.pdf](markers/charuco_letter.pdf)

## Setup

```
python3 -m venv .venv && . .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Commands

```
hausmapr reference check data/reference/guest_room.yaml   # two-pass agreement
hausmapr score data/reference/guest_room.yaml estimate.yaml  # error and LOA band
hausmapr marker --out markers/charuco_letter.pdf            # regenerate the board
```
