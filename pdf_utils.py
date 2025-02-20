from pypdf import PaperSize, PdfReader, PdfWriter, Transformation

class Position:
    upper_left  = 0
    lower_left  = 1
    upper_right = 2
    lower_right = 3

class UnexpectedPositionException(Exception):
    pass

def create_transformation_for_page(page, position):
    if (position == Position.upper_left):
        return Transformation().translate(0, 0)

    if (position == Position.upper_right):
        return Transformation().translate(page.mediabox.width, 0)

    if (position == Position.lower_left):
        return Transformation().translate(0, -page.mediabox.height)

    if (position == Position.lower_right):
        return Transformation().translate(page.mediabox.width, -page.mediabox.height)

    raise UnexpectedPositionException

def generate_composite_pdf(input_files, available_positions):
    if len(input_files) == 0:
        print("No input files chosen")
        return

    writer = PdfWriter()
    out_page = None

    no_available_positions = len(available_positions)

    for ix, file in enumerate(input_files):
        if ix % no_available_positions == 0 or out_page is None:
            out_page = writer.add_blank_page(
                width  = PaperSize.A4.width,
                height = PaperSize.A4.height,
            )

        reader = PdfReader(file)
        page = reader.pages[0]

        # Crop to the size of the label;
        # Expect the label to be spawning the top-left quarter of the page
        page.mediabox.lower_right = (page.mediabox.right / 2, page.mediabox.top / 2)

        out_page.merge_transformed_page(
            page,
            create_transformation_for_page(
                page,
                available_positions[ix % no_available_positions],
            ),
        )

    return writer

def save_pdf(pdf_writer, output_file):
    with open(output_file, "wb") as output_handle:
        pdf_writer.write(output_handle)
