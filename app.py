import argparse
import sys

from gui import run_gui
from pdf_utils import generate_composite_pdf, save_pdf

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="Shipping Labels Merge Tool",
        description="Combine shipping labels into one PDF document with four labels per "
                    "page",
    )
    parser.add_argument(
        "--cli",
        help="Use the command-line interface",
        action='store_true',
    )
    parser.add_argument(
        "-f", "--files",
        required="--cli" in sys.argv,
        nargs="+",
        help="PDF files with one shipping label per page (positioned in the top-left "
             "corner and spawning a quarter of the page).",
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to the output file",
        required="--cli" in sys.argv,
    )

    args = parser.parse_args()

    if args.cli:
        composite_pdf = generate_composite_pdf(args.files)
        save_pdf(composite_pdf, args.output)
    else:
        run_gui()
