


from gui_for_profiles import gui_for_profiles
from indiv_analysis_main import indiv_analysis_main
from one_page_sheet_indiv_v7 import create_executive_sheet_main
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import guiflag
from create_birth_txt_from_db import create_birth_txt_from_db


def run_analysis_main():
    # Define Variables
    if guiflag == 1:
        basepath, sub_start, sub_end, dob = gui_for_profiles()
        if sub_end=='': 
            sub_end=sub_start
        sub_start = int(sub_start)
        sub_end = int(sub_end)
        
    else:
        basepath = 'H:/' 
        sub_start = 1970
        sub_end = 1971


    # Slash in basepath
    if not basepath.endswith('/'):
        basepath += '/'
        
    # # # # # # # # # # # # # # # # # # Individual Answer Analysis # # # # # # # # # # # # # # # # # #
        
    indiv_folder = basepath + 'individual/'


    # Create individual's DOB txt for ONLY ONE subject
    if dob!='YYYY-MM-DD' and dob!='':
        if(sub_start != sub_end):
            print("DOB variable can be used only for one subject at a time.")
            print("Please re-run & define only one subject number and his DOB to proceed.")
            sys.exit()
        else:
            id_birth_dataframe = None
            create_birth_txt_from_db(sub_start, sub_end, indiv_folder, dob, id_birth_dataframe)
    
    # Create executive sheets for subject's answers
    create_executive_sheet_main(indiv_folder, sub_start, sub_end)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    # # # # # # # # # # # # # # Population & Individual Statistical Analysis # # # # # # # # # # # # # #
    indiv_analysis_main(basepath, sub_start, sub_end)
    
    # Save defined path in a txt file
    pathfile = os.path.join(os.path.dirname(__file__), 'last_used_path.txt')
    with open(pathfile, 'w') as f:
        f.write(basepath)
        

run_analysis_main()