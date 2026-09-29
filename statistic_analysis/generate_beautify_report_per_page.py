


from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
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
NOTO_SYMBOLS = os.path.join(FONT_DIR, "NotoSansSymbols2-Regular.ttf")

pdfmetrics.registerFont(TTFont("NotoSans", NOTO_REGULAR))
pdfmetrics.registerFont(TTFont("NotoSans-Bold", NOTO_BOLD))
pdfmetrics.registerFont(TTFont("NotoSansSymbols2", NOTO_SYMBOLS))

# ================== CONFIG ==================

PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT = 20
HEADER_FONT_SIZE = 13

IMAGE_BOTTOM_MARGIN = 60
IMAGE_WIDTH = 500
IMAGE_HEIGHT = 280

PRIMARY = colors.HexColor("#ED752F")
SECONDARY = colors.HexColor("#27AE60")
LIGHT_BG = colors.HexColor("#E4EAF7")
TITLE_BG = colors.HexColor("#07389B")
ANSWERS_BG = colors.HexColor("#F7EFD0")
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
    c.setFont("NotoSans", 11)

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
    c.setFont("NotoSans-Bold", HEADER_FONT_SIZE)
    c.drawString(LEFT + padding_x, y_top - padding_y - 11, "Σύσταση")

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



def draw_stats(c, title, text, y_top):
    padding_after_title = 18
    leading = 14
    max_chars = 95

    # ---- TITLE ----
    c.setFillColor(TITLE_BG)
    c.setFont("NotoSans-Bold", HEADER_FONT_SIZE)
    c.drawString(LEFT, y_top, title)

    # ---- TEXT ----
    lines = wrap(f"{text}", max_chars)

    text_y = y_top - padding_after_title

    c.setFillColor(TEXT)
    c.setFont("NotoSans", 11)

    for line in lines:
        c.drawString(LEFT, text_y, line)
        text_y -= leading

    # return new y position (space after block)
    return text_y - 15


def draw_arrow(c, x, y, size=6):
    color = colors.HexColor("#4D4A49")
    c.setStrokeColor(color)
    c.setLineWidth(1.0)
    c.line(x, y, x + size*2, y)
    c.line(x + size*2, y, x + size*1.5, y + size/2)
    c.line(x + size*2, y, x + size*1.5, y - size/2)


def draw_arrow_glyph(c, x, y):
    c.saveState()
    c.setFont("NotoSansSymbols2", 12)
    c.drawString(x, y, "➝")
    c.restoreState() 

    
def draw_answers(c, x, y, answer, exercise):
    items_per_column = 5
    base_column_offset = 110
    line_height = 14


    padding_x = 15
    padding_y = 12
    radius = 12
    title_height = 20

    for section, values in answer.items():
        if not values:
            continue

        # ---- DETERMINE COLUMN OFFSET ----
        column_offset = base_column_offset
        for v in values:
            if "⟶" in v:
                column_offset = 130
            if ")" in v:
                column_offset = 190
                break

        # ---- CALCULATE BOX SIZE ----
        total_items = len(values)
        columns = (total_items - 1) // items_per_column + 1
        rows = min(items_per_column, total_items)

        content_height = rows * line_height
        box_height = padding_y * 2 + title_height + content_height
        
        if(exercise=='Κατανόηση Προτάσεων'):
            box_width = padding_x * 2 + columns * column_offset + 130
        elif(columns>3):
            box_width = padding_x * 2 + columns * column_offset - 10
        else:
            box_width = padding_x * 2 + columns * column_offset

        # ---- DRAW BACKGROUND BOX ----
        c.setFillColor(ANSWERS_BG)
        c.roundRect(
            x,
            y - box_height,
            box_width,
            box_height,
            radius=radius,
            fill=1,
            stroke=0
        )

        # ---- DRAW SECTION TITLE ----
        c.setFillColor(TITLE_BG)
        c.setFont("NotoSans-Bold", HEADER_FONT_SIZE)
        c.drawString(x + padding_x, y - padding_y - 5, section)

        # ---- DRAW ANSWERS (YOUR EXISTING LOGIC, UNCHANGED) ----
        y -= padding_y + title_height
        start_y = y

        c.setFillColor(TEXT)
        c.setFont("NotoSans", 11)

        for i, v in enumerate(values):
            if "⟶" in v:
                column_offset = 140  # 👈 YOUR LOGIC, UNTOUCHED
            if(exercise=='Κατανόηση Προτάσεων'):
                column_offset = 220
            
            col = i // items_per_column
            row = i % items_per_column

            draw_x = x + padding_x + col * column_offset
            draw_y = start_y - row * line_height

            if "⟶" in v:
                left_part, right_part = v.split("⟶")

                # # # left part
                c.drawString(draw_x, draw_y, "• " + left_part)
                left_w = pdfmetrics.stringWidth("• " + left_part, "NotoSans", 11)

                # # # middle/arrow part
                draw_arrow_glyph(c, draw_x + left_w, draw_y)
                # draw_arrow(c, draw_x + left_w, draw_y + 3)
                
                # # # right part
                c.drawString(draw_x + left_w + 12, draw_y, right_part)
            
            else:
                c.drawString(draw_x, draw_y, f"• {v}")

        # ---- MOVE CURSOR DOWN ----
        y = y - content_height - padding_y - 20

    return y


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

# ================== MAIN DRAWING FUNCTION ==================
def beautify_pdf(c, filepath, recommendation, stats, score, answer, exercise):
    draw_title(c, exercise)

    y = PAGE_HEIGHT - 100

    # ---- RECOMMENDATION ----
    if(recommendation!=''):
        y = draw_recommendation(c, recommendation, y)
        y -= 20
        

    # ---- SCORE ----
    y = draw_stats(c, "Σκορ", score, y)
    y -= 10

    # ---- STATS ----
    y = draw_stats(c, "Στατιστικά", stats, y)
    y -= 10
    

    # ---- ANSWERS ----
    y = draw_answers(c, LEFT, y, answer, exercise)
    y -= 10

    # ---- IMAGE ----
    if filepath:
        insert_image(
            c,
            filepath,
            image_width=480,
            image_height=260,
            y= IMAGE_BOTTOM_MARGIN + IMAGE_HEIGHT - 40 # y-20
        )

    c.showPage()


# ================== MAIN  FUNCTION ==================
def beautify_pdf_main(subno, exercise, title, results_collection1, results_collection2, c, figurepath1, figurepath2, recommendation, stats, score, answer):
    if(exercise=='Memory Short Audit Verb' or exercise=='Decode Words Pseudo' or exercise=='Visual Orthographic Rec'):
        if(subno in results_collection1.keys() and subno in results_collection2.keys()):
            if(subno in results_collection1.keys()):
                beautify_pdf(c, figurepath1, recommendation[0], stats[0], score[0], answer[0], title[0])
            if(subno in results_collection2.keys()):
                beautify_pdf(c, figurepath2, recommendation[1], stats[1], score[1], answer[1], title[1])
        else:
            if(subno in results_collection1.keys()):
                beautify_pdf(c, figurepath1, recommendation[0], stats[0], score[0], answer[0], title[0])
            if(subno in results_collection2.keys()): 
                beautify_pdf(c, figurepath2, recommendation[0], stats[0], score[0], answer[0], title[0])
                
    else:
        if(subno in results_collection1.keys()):
            beautify_pdf(c, figurepath1, recommendation[0], stats[0], score[0], answer[0], title[0])
               
