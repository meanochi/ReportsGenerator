from __future__ import annotations

import argparse
import os
import sys

from config.container import Container
from src.domain.exceptions import AttendanceAppError


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Attendance PDF Modifier ETL Pipeline.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--input",
        metavar="INPUT_PDF",
        required=True,
        help="Path to the original scanned PDF file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="OUTPUT_PDF",
        required=False,
        help="Optional: path to save the modified PDF file.",
    )
    parser.add_argument(
        "--seed",
        metavar="SEED",
        default="",
        help="Optional deterministic seed suffix for reproducible variation sets.",
    )
    return parser.parse_args()


def _build_output_path(input_path: str, output_path: str | None) -> str:
    if output_path:
        return output_path

    dir_name = os.path.dirname(input_path)
    base_name = os.path.basename(input_path)
    name, ext = os.path.splitext(base_name)
    output_filename = f"{name}_GENERATED{ext}"
    return os.path.join(dir_name, output_filename) if dir_name else output_filename


def main() -> None:
    args = _parse_args()
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        sys.exit(1)

    output_path = _build_output_path(args.input, args.output)
    os.environ["ATTENDANCE_VARIATION_SEED"] = args.seed

    print(f"[*] Starting OCR process for: {args.input}. This might take a few seconds...")
    pipeline = Container().build_pipeline()

    try:
        pipeline.process(input_pdf_path=args.input, output_pdf_path=output_path)
        print(f"[+] Successfully generated modified PDF at: {output_path}")
    except AttendanceAppError as exc:
        print(f"[-] Application Error: {exc}")
        sys.exit(1)
    except Exception as exc:  # pragma: no cover - safety net for CLI
        print(f"[-] Unexpected Error occurred: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()