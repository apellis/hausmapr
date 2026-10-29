"""Command line entry point: `hausmapr <command>`."""

import argparse
import sys

from hausmapr import evaluate, reference


def cmd_reference_check(args):
    _, measurements = reference.load(args.path)
    missing, disagreeing = reference.check(measurements, args.tolerance)
    for m in missing:
        print(f"missing second pass: {m.key}")
    for m in disagreeing:
        print(f"re-measure {m.key}: passes differ by {m.spread:.1f} mm")
    print(f"{len(measurements)} measurements, {len(missing)} incomplete, {len(disagreeing)} over {args.tolerance} mm")
    return 1 if disagreeing else 0


def cmd_score(args):
    rows, summary = evaluate.score(args.reference, args.estimate)
    for key, ref_mm, est_mm, err in sorted(rows, key=lambda r: -r[3]):
        print(f"{key:40s} ref {ref_mm:8.1f}  est {est_mm:8.1f}  err {err:6.1f} mm  {evaluate.loa_band(err)}")
    print(summary)
    return 0 if summary["passes_m1_gate"] else 1


def cmd_marker(args):
    from hausmapr import markers

    markers.render_letter_pdf(args.out)
    print(f"wrote {args.out}; print at 100% scale and check one square is 25 mm")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="hausmapr")
    sub = parser.add_subparsers(required=True)

    ref = sub.add_parser("reference", help="reference measurement tools").add_subparsers(required=True)
    p = ref.add_parser("check", help="check two-pass agreement")
    p.add_argument("path")
    p.add_argument("--tolerance", type=float, default=reference.PASS_TOLERANCE_MM)
    p.set_defaults(func=cmd_reference_check)

    p = sub.add_parser("score", help="score an estimate against a reference")
    p.add_argument("reference")
    p.add_argument("estimate")
    p.set_defaults(func=cmd_score)

    p = sub.add_parser("marker", help="write the printable scale board PDF")
    p.add_argument("--out", default="markers/charuco_letter.pdf")
    p.set_defaults(func=cmd_marker)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
