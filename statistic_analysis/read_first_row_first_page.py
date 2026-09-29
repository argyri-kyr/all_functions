
import pdfplumber
from pypdf import PdfReader, PdfWriter


from io import BytesIO
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def create_png_overlay_pdf(png_path, page_width, page_height, text_bottom_y, margin=20):
    page_width = float(page_width)
    page_height = float(page_height)
    text_bottom_y = float(text_bottom_y)
    margin = float(margin)

    img = Image.open(png_path)
    img_w, img_h = img.size

    # Available space BELOW the text
    available_width = page_width - 2 * margin
    available_height = text_bottom_y - margin

    scale = min(available_width / img_w, available_height / img_h, 1.0)

    draw_w = img_w * scale
    draw_h = img_h * scale

    draw_x = (page_width - draw_w) / 2

    # 🔥 CRITICAL FIX: image top is below text
    draw_y = text_bottom_y - margin - draw_h

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
    c.drawImage(
        ImageReader(img),
        draw_x,
        draw_y,
        width=draw_w,
        height=draw_h,
        mask="auto"
    )
    c.showPage()
    c.save()
    buffer.seek(0)

    return buffer


def overlay_png_plots_on_pages(input_pdf, output_pdf, header_to_png):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    with pdfplumber.open(input_pdf) as plumber_pdf:
        for i, page in enumerate(reader.pages):
            plumber_page = plumber_pdf.pages[i]
            text = plumber_page.extract_text()

            if text:
                first_row = text.splitlines()[0]

                header_title = (
                    first_row.split("/")[-1]
                    .split(".")[0]
                    .replace(" pt1", "")
                    .strip()
                )

                if header_title in header_to_png:
                    png_path = header_to_png[header_title]

                    page_width = float(page.mediabox.width)
                    page_height = float(page.mediabox.height)

                    # ✅ CORRECT Y POSITION
                    y_start = get_text_block_bottom_y(
                        plumber_page,
                        page_height,
                        padding=30
                    )

                    overlay_pdf = create_png_overlay_pdf(
                                png_path,
                                page_width,
                                page_height,
                                text_bottom_y=y_start,
                                margin=20
                            )

                    overlay_page = PdfReader(overlay_pdf).pages[0]
                    page.merge_page(overlay_page)

            writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)
        
        
def get_text_block_bottom_y(plumber_page, page_height, padding=20):
    """
    Returns the Y coordinate BELOW the last line of text on the page.
    Guaranteed not to overlap text.
    """

    if not plumber_page.chars:
        return page_height * 0.5

    # Find the LOWEST text on the page
    max_bottom = max(char["bottom"] for char in plumber_page.chars)

    # Convert to PDF coordinate system
    text_bottom_y = page_height - max_bottom

    return max(text_bottom_y - padding, padding)



def main():
    basepath = 'Q:/' 
    subno = 14434
    subjectpath = basepath + 'subject_' + str(subno) 
    report_pdf_path = f"{subjectpath}/individual_analysis_{subno}.pdf"
    new_report_pdf_path = f"{subjectpath}/individual_analysis_{subno}_new.pdf"

    header_to_png = {
            "Raven Score": "Q:/subject_14434/14434_indiv_analysis_plots/Raven Score pt1.png",
            "Phonological Syllables": "Q:/subject_14434/14434_indiv_analysis_plots/Phonological Syllables pt1.png",
            'Visual Orthographic Rec': "Q:/subject_14434/14434_indiv_analysis_plots/Visual Orthographic Rec pt2.png"
        }

    
    overlay_png_plots_on_pages(report_pdf_path, new_report_pdf_path, header_to_png)
    



main()