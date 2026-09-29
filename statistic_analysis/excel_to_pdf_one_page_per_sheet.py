


import win32com.client as win32
import os
   
   
def excel_to_pdf_one_page_per_sheet(excel_path, pdf_path, font_size_map):
    excel = win32.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False

    wb = excel.Workbooks.Open(os.path.abspath(excel_path))

    default_font_size = 12
    
    for sheet in wb.Worksheets:
        sheet_name = sheet.Name

        # ❌ No centering
        ps = sheet.PageSetup
        ps.CenterHorizontally = False
        ps.CenterVertically = False

        # ✅ Apply font size ONLY to specific sheets
        if sheet_name in font_size_map:
            sheet.UsedRange.Font.Size = font_size_map[sheet_name]
        elif default_font_size is not None:
            sheet.UsedRange.Font.Size = default_font_size

        # ✅ Force one page per sheet
        ps.Zoom = False
        ps.FitToPagesWide = 1
        ps.FitToPagesTall = 1

        # Optional orientation
        ps.Orientation = 2  # 2 = landscape

    wb.ExportAsFixedFormat(
        Type=0,  # PDF
        Filename=os.path.abspath(pdf_path),
        Quality=0,  # Standard
        IncludeDocProperties=True,
        IgnorePrintAreas=False,
        OpenAfterPublish=False
    )

    wb.Close(False)
    excel.Quit()
    