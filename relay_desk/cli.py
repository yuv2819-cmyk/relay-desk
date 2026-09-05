from __future__ import annotations

import argparse
import json
import sys

from .pipeline import run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="relay-desk",
        description="Run a question through researcher -> drafter -> critic.",
    )
    parser.add_argument("question", nargs="*", help="The question to work")
    parser.add_argument("--offline", action="store_true", help="No API calls")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of markdown")
    args = parser.parse_args(argv)

    question = " ".join(args.question).strip()
    if not question:
        question = sys.stdin.read().strip()
    if not question:
        parser.error("Pass a question or pipe text on stdin.")

    result = run(question, offline_mode=args.offline)
    if args.json:
        print(json.dumps(result.as_dict(), indent=2))
    else:
        print(result.as_markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
