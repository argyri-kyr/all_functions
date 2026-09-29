


from asyncio.windows_events import NULL
import xlsxwriter
import os
import pandas as pd

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass


def cbm_scoring():
    from_runcrashes = False 

    subs = [14022]
    countsubs = 0
    # subs = [13020]

    parta_cor = [2, 1, 1, 3, 2, 3, 3, 2, 3, 1, 3, 3, 1, 3, 2, 2, 1, 1]
    partb_cor = [1, 3, 1, 1, 3, 2, 1, 3, 3, 1, 2, 2, 1, 3, 2, 1, 3, 1, 3, 1, 3, 1, 1, 2]
    partc_cor = [2, 1, 2, 2, 1, 3, 1, 1, 2, 2, 2, 1, 3, 2, 1, 1, 3, 1, 2, 1, 3, 1, 1, 3]


    for sub1 in subs:
        # Define correct answers path
        cbmscoringpath = folder1 + folder2 + 'subject_' + str(sub1) + '/' + 'CBM_scoring.xlsx'
        workbook = xlsxwriter.Workbook(cbmscoringpath)
        worksheet = workbook.add_worksheet()
        
        subjectno_col = 0
        parta_cor_col = 1
        parta_error_col = 2
        partb_cor_col = 3
        partb_error_col = 4
        partc_cor_col = 5
        partc_error_col = 6
        average_subtr = 7

        worksheet.write(0, subjectno_col, "ID")
        worksheet.write(0, parta_cor_col, "PART A CORRECTS")
        worksheet.write(0, parta_error_col, "PART A ERRORS")
        worksheet.write(0, partb_cor_col, "PART B CORRECTS")
        worksheet.write(0, partb_error_col, "PART B ERRORS")
        worksheet.write(0, partc_cor_col, "PART C CORRECTS")
        worksheet.write(0, partc_error_col, "PART C ERRORS")
        worksheet.write(0, average_subtr, "DIFF")  

    
        print("\nSub = ", sub1)

        
        # # # # # # # # # # # # # #  Check if cbma, cbmb, cbmc exists, in order to start main process  # # # # # # # # # # # # # #

        search1 = getGazesFoldersandClass(sub1)
        cbmfilepath = folder1 + folder2 + 'subject_' + str(sub1) + '/' + 'CBM.xlsx'
        
        if( search1 != NULL and os.path.exists(cbmfilepath) ): # # if subject exists 
            
            search1 = getGazesFoldersandClass(sub1)
            gazesfolders, sub1class, subexam = search1[0], search1[1], search1[2]

            
            
            df = pd.read_excel(cbmfilepath, usecols=[0, 1, 2], engine='openpyxl', header=None)
            clean_columns = {}

            for col in df.columns:
                clean_columns[col] = df[col].dropna().tolist()
                
            # Actual answers
            colA = clean_columns[0]
            colB = clean_columns[1]
            colC = clean_columns[2]
            
            # Define if it's correct or not
            ans1 = [1 if colA[i] == parta_cor[i] else 0 for i in range(len(colA))]
            ans2 = [1 if colB[i] == partb_cor[i] else 0 for i in range(len(colB))]
            ans3 = [1 if colC[i] == partc_cor[i] else 0 for i in range(len(colC))]

            # Calculate how many is correct
            correct_ansA = ans1.count(1)
            correct_ansB = ans2.count(1)
            correct_ansC = ans3.count(1)
            
            # Calculate how many is wrong
            error_ansA = ans1.count(0)
            error_ansB = ans2.count(0)
            error_ansC = ans3.count(0)
            
            # Calculate average difference between correct ones and wrong ones
            correct_average = (correct_ansA + correct_ansB + correct_ansC) / 3
            error_average = (error_ansA + error_ansB + error_ansC) / 3

            overall_final_score = correct_average - error_average
                 
            worksheet.write(1, subjectno_col, sub1)
            worksheet.write(1, parta_cor_col, correct_ansA)
            worksheet.write(1, parta_error_col, error_ansA)
            worksheet.write(1, partb_cor_col, correct_ansB)
            worksheet.write(1, partb_error_col, error_ansB)
            worksheet.write(1, partc_cor_col, correct_ansC)
            worksheet.write(1, partc_error_col, error_ansC)
            worksheet.write(1, average_subtr, overall_final_score) 

            # # # # # # End of first-statistics # # # # #


    workbook.close()

cbm_scoring()