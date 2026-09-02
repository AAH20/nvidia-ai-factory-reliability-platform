import argparse
import json
from pathlib import Path

from .engine import analyze
from .io import load_case


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a synthetic or measured NVIDIA AI factory snapshot")
    parser.add_argument("case")
    parser.add_argument("--output")
    args = parser.parse_args()
    result = analyze(*load_case(json.loads(Path(args.case).read_text())))
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(rendered + "\n")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
