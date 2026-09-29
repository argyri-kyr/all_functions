

import openpyxl

def auto_adjust_column_width_xlsx(filepath, sheet_name):
    # Now, open the saved workbook with openpyxl and apply auto-fit
    try:
        wb = openpyxl.load_workbook(filepath)
        ws = wb[sheet_name] # Get the specific worksheet

        for col_idx, col in enumerate(ws.columns):
            max_length = 0
            column_letter = col[0].column_letter # Get the column letter (e.g., 'A')

            for cell in col:
                try:
                    cell_value_str = str(cell.value) if cell.value is not None else ""
                    if len(cell_value_str) > max_length:
                        max_length = len(cell_value_str)
                except TypeError:
                    pass

            # Ensure a minimum width even if all cells are empty or skipped
            if max_length == 0:
                adjusted_width = 10 # Default width for empty columns, adjust as needed
            else:
                adjusted_width = (max_length + 2) * 0.87 # Add a small buffer (this is the adjustment factor for a bit extra space, it is 0.87 to fit as 1 page in the .pdf, if i make it bigger like 0.9 then the pdf export will be 2 pages)

            ws.column_dimensions[column_letter].width = adjusted_width

        wb.save(filepath)
        print(f"Workbook saved and columns auto-fitted to: {filepath}")

    except Exception as e:
        print(f"Error during auto-fitting with openpyxl: {e}")