import pdfplumber
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os
from textwrap import wrap
from reportlab.lib.styles import ParagraphStyle

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE_DIR, "fonts")

NOTO_REGULAR = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")
NOTO_BOLD = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")

pdfmetrics.registerFont(TTFont("NotoSans", NOTO_REGULAR))
pdfmetrics.registerFont(TTFont("NotoSans-Bold", NOTO_BOLD))

# ================== CONFIG ==================

PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT = 40

PRIMARY = colors.HexColor("#2F80ED")
SECONDARY = colors.HexColor("#27AE60")
LIGHT_BG = colors.HexColor("#F5F7FB")
TEXT = colors.HexColor("#333333")

REC_STYLE = ParagraphStyle(
    name="Rec",
    fontName="NotoSans",
    fontSize=11,
    leading=14,
    textColor="black",
)

# ================== DRAW HELPERS ==================

def draw_title(c, title):
    c.setFillColor(PRIMARY)
    c.setFont("NotoSans-Bold", 20)
    c.drawString(LEFT, PAGE_HEIGHT - 60, title)


def draw_wrapped_text(c, text, x, y, max_chars=95, leading=14):
    c.setFillColor(TEXT)
    c.setFont("NotoSans", 10)

    for line in wrap(text, max_chars):
        c.drawString(x, y, line)
        y -= leading

    return y


def draw_recommendation(c, text, y_top):
    padding_x = 15
    padding_y = 12
    leading = 14
    max_chars = 95

    lines = wrap(text, max_chars)
    text_height = len(lines) * leading

    title_height = 30
    box_height = padding_y * 2 + title_height + text_height

    # ---- BOX ----
    c.setFillColor(LIGHT_BG)
    c.roundRect(
        LEFT,
        y_top - box_height,
        PAGE_WIDTH - 2 * LEFT,
        box_height,
        radius=12,
        fill=1,
        stroke=0
    )

    # ---- TITLE ----
    c.setFillColor(SECONDARY)
    c.setFont("NotoSans-Bold", 11)
    c.drawString(
        LEFT + padding_x,
        y_top - padding_y - 11,
        "Σύσταση"
    )

    # ---- TEXT ----
    text_y = y_top - padding_y - title_height
    draw_wrapped_text(
        c,
        text,
        LEFT + padding_x,
        text_y,
        max_chars=max_chars,
        leading=leading
    )

    return y_top - box_height - 20



def draw_stats(c, text, y):
    c.setFillColor(TEXT)
    c.setFont("NotoSans", 9)
    c.drawString(LEFT, y, f"📊 {text}")


def insert_image(c, path_to_image, image_width, image_height, y):
    """
    Inserts an image from disk at a fixed position.
    """
    if not path_to_image:
        return

    if not os.path.exists(path_to_image):
        print(f"⚠ Image not found: {path_to_image}")
        return

    x = LEFT + 20
    y_pos = y - image_height

    c.drawImage(
        path_to_image,
        x,
        y_pos,
        width=image_width,
        height=image_height,
        preserveAspectRatio=True,
        mask="auto"
    )

# ================== TEXT → IMAGE PATH ==================

def clean_image_path(imagefilepath):
    """
    Converts:
    imageFile Q:/subject_14434/.../Raven Score pt1.png
    →
    images/Raven Score pt1.png
    """
    if not imagefilepath.lower().startswith("imagefile"):
        return None

    raw_path = imagefilepath.split("imageFile", 1)[-1].strip()

    return raw_path

# ================== PAGE PARSING ==================

def extract_page_data(page):
    text = page.extract_text() or ""
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    title = "Αποτελέσματα Ανάλυσης Eyeradar"

    imagefilepath = ""
    recommendation = ""
    stats = ""
    extra = []

    for lineno, line in enumerate(lines):
        if lineno == 0:
            imagefilepath = line

        if (line.startswith("recommendation")) or (lineno==1 and lines[lineno+1].startswith("recommendation")):
            recommendation = recommendation + "\n" + line.replace("recommendation", "").strip()

        if line.startswith("stats"):
            stats = line.replace("stats", "").strip()

        if "⟶" in line:
            extra.append(line)

    return {
        "title": title,
        "imagefilepath": imagefilepath,
        "recommendation": recommendation,
        "stats": stats,
        "extra": extra
    }

# ================== EXTRA / ANSWERS STRUCTURE ==================

def structure_extra(extra_lines):
    result = {}
    current_section = None

    for lineno in range(len(extra_lines)):
        line = extra_lines[lineno]
        line = line.strip()
        if not line:
            continue

        if 'Σωστό' in line or 'Λάθος' in line or 'Παρατονισμός' in line:
            current_section = line.split(" ")[0]
            line = line.split(" ")[1:]
            line = ' '.join(line)
            result[current_section] = []

        if current_section and "⟶" in line:
            left, right = line.split("⟶", 1)
            result[current_section].append((left, right))

    return result


# ================== MAIN PROCESS ==================

IMAGE_BOTTOM_MARGIN = 60
IMAGE_WIDTH = 500
IMAGE_HEIGHT = 280

def beautify_pdf(input_pdf, output_pdf):
    with pdfplumber.open(input_pdf) as pdf:
        c = canvas.Canvas(output_pdf, pagesize=A4)

        for page in pdf.pages:
            data = extract_page_data(page)

            # ---- TITLE ----
            if(page.page_number==1):
                draw_title(c, data["title"])

            # ---- TEXT CONTENT ----
            y = PAGE_HEIGHT - 100

            if data["recommendation"]:
                y = draw_recommendation(c, data["recommendation"], y)

            if data["stats"]:
                draw_stats(c, data["stats"], y)
                y -= 30

            extra = data.get("extra")
            if extra:
                structured = structure_extra(extra)

                for section, pairs in structured.items():
                    c.setFont("NotoSans-Bold", 11)
                    c.drawString(LEFT, y, section)
                    y -= 16

                    c.setFont("NotoSans", 11)
                    for left, right in pairs:
                        c.drawString(LEFT + 20, y, f"{left} → {right}")
                        y -= 14

                    y -= 10

            # ---- IMAGE AT PAGE BOTTOM ----
            image_path = clean_image_path(data["imagefilepath"])

            insert_image(
                c,
                image_path,
                image_width=480,
                image_height=260,
                y=IMAGE_BOTTOM_MARGIN + IMAGE_HEIGHT
            )

            c.showPage()

        c.save()
        
# ================== RUN ==================

if __name__ == "__main__":
    basepath = 'Q:/' 
    subno = 14434
    subjectpath = basepath + 'subject_' + str(subno) 
    INPUT_PDF = f"{subjectpath}/individual_analysis_{subno}_new.pdf"
    OUTPUT_PDF = f"{subjectpath}/individual_analysis_{subno}_bautify.pdf"

    if os.path.exists(OUTPUT_PDF):
        os.remove(OUTPUT_PDF)
        
    beautify_pdf(INPUT_PDF, OUTPUT_PDF)
    print("✅ PDF redesigned successfully")
