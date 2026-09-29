

import pandas as pd


def get_exercise_block(ws, exercise):
    # 1. Find the title cell
    title_row = None
    title_col = None

    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, str) and exercise in cell.value:
                title_row = cell.row
                title_col = cell.column
                break
        if title_row:
            break

    if title_row is None:
        raise ValueError(f"Exercise '{exercise}' not found")

    data = []

    for r in range(title_row + 1, ws.max_row + 1):
        first_cell = ws.cell(row=r, column=title_col).value

        # STOP at the NEXT title (any exercise)
        if isinstance(first_cell, str) and "(" in first_cell:
            break

        row_values = [
            ws.cell(row=r, column=c).value
            for c in range(title_col, ws.max_column + 1)
        ]

        # trim trailing empty columns
        while row_values and row_values[-1] is None:
            row_values.pop()

        # keep only meaningful rows
        if any(v is not None for v in row_values):
            data.append(row_values)

    return pd.DataFrame(data)