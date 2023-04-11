from pypdf import PdfReader, PdfWriter

def generate_composite_pdf(input_files, output_file):
    writer = PdfWriter()

    if not isinstance(input_files, list):
        input_files = [input_files]

    for pos, file in enumerate(input_files):
        reader = PdfReader(file)
        writer.add_page(reader.pages[0])

    with open(output_file, "wb") as output_handle:
        writer.write(output_handle)
