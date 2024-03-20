from fpdf import FPDF
import pathlib

def text_to_pdf(text, filename):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Courier', size=fontsize_pt)

    for line in text.split('\n'):
        pdf.ln(fontsize_mm)
        words = line.split()
        current_line = words[0]

        for word in words[1:]:
            if pdf.get_string_width(current_line + ' ' + word) < width_text:
                current_line += ' ' + word
            else:
                pdf.cell(0, fontsize_mm, current_line, ln=True)
                current_line = word

        pdf.cell(0, fontsize_mm, current_line, ln=True)

    pdf.output(filename, 'F')

def convert_text_to_pdf(input_files, output_files):
    for input_file, output_file in zip(input_files, output_files):
        try:
            text = pathlib.Path(input_file).read_text()
            text_to_pdf(text, output_file)
            print(f"Conversion for {input_file} saved to {output_file}")
        except Exception as e:
            print(f"Error during conversion: {str(e)}")

if __name__ == "__main__":
    input_files = ["fr_text_1_encrypted.txt", "fr_text_2_encrypted.txt", "fr_text_3_encrypted.txt"]
    output_files = ["text_1.pdf", "text_2.pdf", "text_3.pdf"]

    convert_text_to_pdf(input_files, output_files)
