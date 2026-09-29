




from openpyxl import load_workbook
from openpyxl.styles import Alignment


def auto_adjust_column_width_xlsx_v2(filepath, padding=2, shrink_B=5):
    wb = load_workbook(filepath)

    for ws in wb.worksheets:  # loop over ALL sheets
        for col_cells in ws.columns:
            max_length = 0
            col_letter = col_cells[0].column_letter

            for cell in col_cells:
                if cell.value is not None:
                    # ✅ FIX: handle multiline text correctly
                    lines = str(cell.value).splitlines()
                    longest_line = max(len(line) for line in lines)
                    max_length = max(max_length, longest_line)

                    # optional but recommended for multiline cells
                    cell.alignment = Alignment(wrap_text=True)

            if max_length > 0:
                width = max_length + padding

                # 🔹 HARD-CODED SHRINK FOR COLUMN B
                if col_letter == "B":
                    width = max(5, width - shrink_B)  # safety minimum

                ws.column_dimensions[col_letter].width = width

    wb.save(filepath)