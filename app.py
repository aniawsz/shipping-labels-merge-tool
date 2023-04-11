import argparse

from pdf_utils import generate_composite_pdf

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
            prog="Shipping Labels Merge Tool",
            description="Combine shipping labels into one PDF document with four labels "
                        "per page",
            )
    parser.add_argument(
            "files",
            nargs="+",
            help="PDF files with one shipping label per page (positioned in the "
                 "top-left corner).",
            )
    parser.add_argument("output", help="Path to the output file")

    args = parser.parse_args()

    composite_pdf = generate_composite_pdf(args.files, args.output)
