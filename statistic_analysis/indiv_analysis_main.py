

import pandas as pd
import os
import xlsxwriter

from load_population import load_class_population
from indiv_analysis import indiv_analysis
from load_population import load_class_population_exercise_data
from delete_old_individual_analysisfiles import delete_old_individual_analysisfiles
from get_subclass import get_subclass


 
def indiv_analysis_main(basepath, sub_start, sub_end):
    # Individual Path
    indiv_path = basepath + 'individual/'
    
    # Population Path & Define Population DataFrame
    popul_path = basepath + 'population/'
    db_name = "ANALYSIS_DB.xlsx"
    popul_db = popul_path + db_name
    popul_database_df = pd.read_excel(popul_db)
    
    # Define Exercise Sheet Name
    executive_sheet_name = "ExecutiveSheet"


    # # # Exercises
    # 'Memory Short Audit Verb':[7,34,10] -> 7(index=0) ερωτήματα με μέγιστο σκορ 7(index=1) για το part1 και 10(index=2) ερωτήματα για το part2
    exercises = {'Raven Score':141, 'Memory Short Audit Verb':[7, 7, 10], 'Memory Work Audit Verb':7, 'Phonological Rhymes':10, 'Phonological Syllables':10, 'Phonological Phonemes':6, 'Decode Words Pseudo':24, 'Visual Orthographic Rec':10, 'Decode Sentences':10}
    
    # # # fonts
    font_sizes_pdf = {
        'Phonological Rhymes': 12
    }
    
    # # # class mapping dictionary
    class_mapping = {
        "ae": "Α' Δημοτικού",
        "be": "Β' Δημοτικού",
        "ge": "Γ' Δημοτικού",
        "de": "Δ' Δημοτικού",
        "ee": "Ε' Δημοτικού",
        "ste": "ΣΤ' Δημοτικού",
        "ag": "Α' Γυμνασίου",
        "bg": "Β' Γυμνασίου",
        "gg": "Γ' Γυμνασίου",
        "al": "Α' Λυκείου",
        "bl": "Β' Λυκείου",
        "gl": "Γ' Λυκείου",
        "ad": "Ενήλικας"
    }

    # Read the Database Excel file
    
    # Create list for undone subjects, in case that '?' exist in their data, 
    # so no answers can be defined and thus no analysis can be done for them. 
    # This list will be printed at the end of the analysis.
    undone_subs_list = []
    undone_wb = xlsxwriter.Workbook(indiv_path + "undone_subjects.xlsx")
    undone_wsh = undone_wb.add_worksheet("Sheet1")
    
    for subno in range(sub_start, sub_end + 1):
        # # # # # # # # # # # # # # # # Individual Processing # # # # # # # # # # # # # #
        print("\n\n--- Individual Analysis for Subject %d ---" % subno)
        
        # Check if subject's folder path exist
        subjectpath = indiv_path +'subject_' + str(subno) + '/'
        if not os.path.exists(subjectpath):
            print("This subject doesn't exist in individual/ folder. \nPath = " + subjectpath + " doesn't exist.")
            continue
        
        # Check if subject's executive_sheet exist
        sub_answers_path = subjectpath + 'executive_sheet_' + str(subno) + '.xlsx'
        if not os.path.exists(sub_answers_path):
            print("This subject hasn't done any TEST.\nPath = " + sub_answers_path + " doesn't exist.")
            continue
        
        # Create plots folder, into subject's folder, if not exist
        plotspath = subjectpath + str(subno) + '_indiv_analysis_plots'  
        if not os.path.exists(plotspath):
            os.makedirs(plotspath)
        
        # Delete older analysis files, for this subject
        delete_old_individual_analysisfiles(subno, subjectpath)
        
        # Find subject's class
        search1 = get_subclass(subno, subjectpath)
        _, subclass, _ = search1[0], search1[1], int(search1[2])
        
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        
        # # # # # # # # # # # # # # # # Population Processing # # # # # # # # # # # # # # # # #
        
        # Gather class population ids from db
        class_filtered_population = load_class_population(subclass, popul_database_df)
        
        # Add subno in class population if not exist
        if subno not in class_filtered_population:
            class_filtered_population.append(subno)
            
        # Gather class population dataframes->their answers from executive_sheet
        sub_dataframes = load_class_population_exercise_data(subno, indiv_path, popul_path, class_filtered_population, executive_sheet_name)
        
        # Run indiv analysis
        undone_sub = indiv_analysis(subno, sub_dataframes, class_mapping, subclass, exercises, subjectpath, plotspath, font_sizes_pdf)
        if(undone_sub!=None):
            undone_subs_list.append(undone_sub)
    
    undone_wsh.write_column(0, 0, undone_subs_list)
    undone_wb.close()