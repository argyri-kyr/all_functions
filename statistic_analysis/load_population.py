

import os
import pandas as pd
from openpyxl import load_workbook
import sys


def load_class_population(subclass, df):
    # Parameters
    id_column = "ID"
    class_column = "RADAR CLASS"

    # Make sure ID column is numeric
    df[id_column] = pd.to_numeric(df[id_column], errors="coerce")

    # Filter all rows with the same CLASS
    same_class = df[df[class_column] == subclass][id_column].tolist()
    same_class = [int(id) for id in same_class]
    
    return same_class


def load_class_population_exercise_data(indiv_subno, indiv_path, popul_path, sublist, sheet_name):
    # Read and store the dataframes for each individual into a dict 
    # in order to access them each time not read the excels again and again
    sub_dataframes = {}
    for subno in sublist:
        # Load executive_sheet for the individual one and the population ones
        if(subno==indiv_subno):
            sub_folder = indiv_path + 'subject_' + str(subno) + '/'
            filepath = indiv_path + 'subject_' + str(subno) + '/'+ 'executive_sheet_' + str(subno) + '.xlsx'
        else:
            sub_folder = popul_path + 'subject_' + str(subno) + '/'
            filepath = popul_path + 'subject_' + str(subno) + '/'+ 'executive_sheet_' + str(subno) + '.xlsx'
        
        # This is for skipping non existing subjects in population (i.e. they exist in db but not in population folder)
        if not os.path.exists(sub_folder):
            continue
        
        if not os.path.exists(filepath):
            print("File %s not found" % (filepath) )
            print("Score him first with one_page_sheet_indiv_v7.py")
            sys.exit()
        
        wb = load_workbook(filepath, data_only=True)
        ws = wb[sheet_name]
        sub_dataframes[subno] = ws
    
    return sub_dataframes