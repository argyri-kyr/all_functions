

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COVER_DEPENDENCIES_DIR = os.path.join(BASE_DIR, "cover_deps")

COVER = os.path.join(COVER_DEPENDENCIES_DIR, "cover.png")
                            
def draw_cover_page(c, subno):
    page_width, page_height = A4

    # ---- DRAW COVER IMAGE (FULL PAGE) ----
    cover = ImageReader(COVER)
    c.drawImage(
        cover,
        x=0,
        y=0,
        width=page_width,
        height=page_height,
        preserveAspectRatio=True,
        mask='auto'
    )

    # ---- OVERLAY SUBJECT NUMBER (BOTTOM-LEFT) ----
    c.setFont("Helvetica-Bold", 30)
    c.setFillColorRGB(0, 0, 0)  # black

    c.drawString(
        4 * cm + 10,          # left margin
        2 * cm,          # bottom margin
        f"{subno}"
    )

    # ---- FINISH COVER PAGE ----
    c.showPage()
