

import pandas as pd
import numpy 

def get_result(exercise, df):
    last_row = [df.iloc[-1-i] for i in range(len(df)) if df.iloc[-1-i].notna().any()][0]

    # if(exercise=='Decode Words Pseudo'):
    #     last_row = df.iloc[-1]
    #     for col_name, cell in last_row.items():
    #         if(col_name==0 or col_name==1):
    #             if not ( isinstance(cell, (int, float)) or cell is None or pd.isna(cell) ):
    #                 last_row = df.iloc[-2]
    #                 break
    
    if(exercise=='Decode Words Pseudo'):
        last_row = df.iloc[-1]
        
    if(exercise=='Raven Score'):
        last_row = df.iloc[-2]
        
    
    result = []
    for col_name, cell in last_row.items():
        if( (cell is None or pd.isna(cell)) and (col_name==0 or col_name==1) and exercise=='Decode Words Pseudo'):
            result.append([-1])
            continue
        elif cell is None or pd.isna(cell):
            continue

        # Case 1: "3,3"
        if isinstance(cell, str) and "," in cell:
            parts = cell.split(",")
            if all(p.strip().isdigit() for p in parts):
                result.append([int(p) for p in parts])

        # Case 2: extra specific case only for Raven Score and more specific only for True Age cell in order to keep the float part
        elif isinstance(cell, float) and exercise=='Raven Score' and isinstance(cell, float):
            result.append([float(cell)])
            
        # Case 3: single number
        elif isinstance(cell, (int, float, numpy.int64)):
            result.append([int(cell)])
            
        # Case 4: numeric string "3"
        elif isinstance(cell, str) and cell.strip().isdigit():
            result.append([int(cell)])
        
            
    return result
