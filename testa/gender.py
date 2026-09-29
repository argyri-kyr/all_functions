

import pandas as pd
from asyncio.windows_events import NULL


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2
from GetSomeInitialData import getGazesFoldersandClass

def gender():
    data = pd.read_excel(folder1 + folder2 + 'gender_list2.xlsx')

    female = data.iloc[:,0].tolist()
    female = [x for x in female if not pd.isna(x)]
    female = [int(x) for x in female]

    male = data.iloc[:,1].tolist()
    male = [x for x in male if not pd.isna(x)]
    male = [int(x) for x in male]

    for fno in female:
        search1 = getGazesFoldersandClass(fno)   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/

        if( search1 == NULL ):
            continue
        
        else:
            gender_indicator = open(folder1 + folder2 + 'subject_' + str(fno) + '/female.txt',"w")
            gender_indicator.close()


    for mno in male:
        search1 = getGazesFoldersandClass(mno)   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/

        if( search1 == NULL ):
            continue
        
        else:
            gender_indicator = open(folder1 + folder2 + 'subject_' + str(mno) + '/male.txt',"w")
            gender_indicator.close()
    
   
    return

gender()