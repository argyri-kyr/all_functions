

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import win32com.client
from pypdf import PdfWriter

subno = 14303
basepath = 'Q:/' 
subject_path = basepath + 'subject_' + str(subno) + '/'

for fname in os.listdir(subject_path):
    if fname.startswith(str(subno)) and fname.endswith(".xlsx"):
        excel_path = os.path.join(subject_path, fname)
        print(excel_path)
        break  # remove if you want all matches
    
main_filename = fname.split('.')
output_pdf = subject_path + main_filename[0] + "_output.pdf"

# # Read all sheets
# xls = pd.ExcelFile(excel_path)

# with PdfPages(output_pdf) as pdf:
#     for sheet_name in xls.sheet_names:
#         df = pd.read_excel(xls, sheet_name=sheet_name)

#         fig, ax = plt.subplots(figsize=(11.69, 8.27))  # A4 landscape
#         ax.axis('off')

#         table = ax.table(
#             cellText=df.values,
#             colLabels=df.columns,
#             loc='center',
#             cellLoc='center'
#         )

#         table.auto_set_font_size(False)
#         table.set_fontsize(8)
#         table.scale(1, 1.5)

#         plt.title(sheet_name, fontsize=12, pad=20)
#         pdf.savefig(fig, bbox_inches='tight')
#         plt.close(fig)

# print("PDF created successfully!")



# Second
output_pdf = os.path.join(subject_path, main_filename[0] + "_output2.pdf")

# ======================================================
# SHEET -> PLOT CONFIGURATION
# ======================================================
sheet_plots = {
    "phonolrhymes": os.path.join(
        subject_path,
        "14303_indiv_analysis_plots",
        "Phonological Rhymes  pt1.png"
    )
}

# ======================================================
# EXCEL SETUP
# ======================================================
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False

wb = excel.Workbooks.Open(os.path.abspath(excel_path))

# ======================================================
# PREPARE SHEETS
# ======================================================
for ws in wb.Worksheets:

    sheet_name = ws.Name
    print(f"Processing sheet: {sheet_name}")

    # --------------------------------------------------
    # Insert plot ONLY if sheet is configured
    # --------------------------------------------------
    if sheet_name in sheet_plots:

        image_path = os.path.abspath(sheet_plots[sheet_name])

        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"Plot not found: {image_path}")

        # Remove old pictures (prevents duplicates)
        for shp in ws.Shapes:
            if shp.Type == 13:  # msoPicture
                shp.Delete()

        ws.Shapes.AddPicture(
            Filename=image_path,
            LinkToFile=False,
            SaveWithDocument=True,
            Left=ws.Range("H2").Left,
            Top=ws.Range("H2").Top,
            Width=-1,
            Height=-1
        )

        # Adjust font only where plots exist
        ws.UsedRange.Font.Size = 12

    # --------------------------------------------------
    # Page setup (do NOT force fit-to-page)
    # --------------------------------------------------
    ws.PageSetup.Zoom = 100
    ws.PageSetup.FitToPagesWide = False
    ws.PageSetup.FitToPagesTall = False

    ws.Calculate()

# ======================================================
# EXPORT EACH SHEET SAFELY
# ======================================================
os.makedirs(os.path.dirname(output_pdf), exist_ok=True)

temp_pdfs = []

for ws in wb.Worksheets:

    temp_pdf = os.path.join(
        subject_path,
        f"_temp_{ws.Name}.pdf"
    )

    ws.Calculate()
    ws.ExportAsFixedFormat(
        Type=0,                 # PDF
        Filename=temp_pdf,
        Quality=0,
        IncludeDocProperties=True,
        IgnorePrintAreas=False,
        OpenAfterPublish=False
    )

    temp_pdfs.append(temp_pdf)

# ======================================================
# MERGE PDFs
# ======================================================
writer = PdfWriter()

for pdf in temp_pdfs:
    writer.append(pdf)

with open(output_pdf, "wb") as f:
    writer.write(f)

# ======================================================
# CLEANUP
# ======================================================
for pdf in temp_pdfs:
    os.remove(pdf)

wb.Close(SaveChanges=True)
excel.Quit()

print("PDF created successfully:", output_pdf)