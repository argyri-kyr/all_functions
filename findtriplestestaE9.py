

import pandas as pd
import os
import xlsxwriter


def findIds():
    main_folder = 'U:/'
    
    start = 14001
    end = 14258
    
    sheet_name  ='partΕ exerc9'
    workbook = xlsxwriter.Workbook(main_folder + 'testatripleansE9.xlsx')
    worksheet = workbook.add_worksheet()
    
    i=0 
    for subno in range(start, end+1):
        file_path = main_folder + 'subject_' + str(subno) + '/testa.xlsx'
        
        if os.path.exists(file_path):
            partE9_df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[0, 1, 2], header=None)
            
            condition = partE9_df[2].notna()

            partE9_df.loc[condition, 1] = (partE9_df.loc[condition, 1].fillna(0).astype(int).astype(str) +
                            partE9_df.loc[condition, 2].fillna(0).astype(int).astype(str)).astype(float)
            
            clean_columns = {
                0: partE9_df[0].tolist(),
                1: partE9_df[1].tolist(), # This column now contains the concatenated values or original values
                2: partE9_df[2].tolist()  # This column remains unchanged
            }
            
            clean_columns[0] = [x for x in clean_columns[0] if not pd.isna(x)]
            clean_columns[1] = [x if not pd.isna(x) else None for x in clean_columns[1]]
            clean_columns[2] = [x if not pd.isna(x) else None for x in clean_columns[2]]
            
            found_extra_ans = [True for x in clean_columns[2] if x is not None]
            if found_extra_ans!=[]:
                print(subno)
                worksheet.write(i+1, 0, subno)
                i+=1
            
            
    workbook.close()        


findIds()