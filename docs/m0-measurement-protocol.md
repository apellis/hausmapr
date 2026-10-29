# M0 measurement protocol

Goal: a reference set of measurements for three rooms that the M1 reconstructions get scored against. We need about 5 mm agreement between two passes to judge a 5 cm (LOA20) target fairly.

Rooms:

| Room id | Room | Why it's useful |
| --- | --- | --- |
| `guest_room` | Guest room | Baseline |
| `pocket_office` | Pocket office | Small and tight, hard to get overlap in photos |
| `emilys_room` | Emily's room | Clutter on walls and floor |

## Before you start

1. Clear what you can from the base of each wall so the laser hits the wall, not furniture.
2. Sketch the room from above on paper. Number the corners clockwise starting from the door hinge side (C1, C2, ...). A wall is named by its two corners, e.g. `C1-C2`.
3. Copy `data/reference/TEMPLATE.yaml` to `data/reference/<room id>.yaml`.

## What to measure

Measure everything in millimetres, or in inches if that's easier; set `units` in the file to match.

1. **Wall lengths**, floor level, corner to corner, for every wall.
2. **Diagonals**: at least two corner-to-corner diagonals across the floor. They tell us whether the room is square.
3. **Ceiling height**: at the centre and near two corners.
4. **Every door, window and opening**: width and height of the opening (inside the trim), the sill height for windows, and the distance from the nearest corner to the opening's edge.
5. **Anything notable** (closet, bulkhead, built-in, radiator): width, depth and height, under `features`.

## Two passes

Do the whole room twice, ideally on different days or with someone else doing the second pass. Put both readings in the file. `hausmapr reference check` flags any pair more than 5 mm apart so you can re-measure it.

## Photos for M1 (same visit)

See `docs/m1-capture-protocol.md`. Taking them on the same day keeps furniture in the same place.
