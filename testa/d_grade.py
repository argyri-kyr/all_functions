


from asyncio.windows_events import NULL
import pandas as pd

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass


text="testapartd"


def d_grade(sub):
    from_runcrashes = False

    search1 = getGazesFoldersandClass(sub)   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/
   
    gazesfolders1, sub1class, subexam = search1[0], search1[1], search1[2]   # gazesfolders1 : ta keimena pou brethikan mesa sto individual
    gazesfolders = gazesfolders1 
    gazesfolders = list(dict.fromkeys(gazesfolders))               

    file = getGazesFolderbyText(sub, subexam, text, gazesfolders, sub1class, from_runcrashes)

    if(file==NULL):
        # print("There is no data for this text")
        return -1, -1

    # collect data per exercise
    answerspath = folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/Answers.xlsx'
    if not os.path.exists(answerspath):
        return -1, -1
    
    data = pd.read_excel(answerspath, header=None)
    
    d1_data = data.iloc[0,:].tolist()
    d1_data = [x for x in d1_data if not pd.isna(x)]
    d1_data = [int(x) for x in d1_data]

    d2_data = data.iloc[1,:].tolist()
    d2_data = [x for x in d2_data if not pd.isna(x)]
    d2_data = [int(x) for x in d2_data]

    
    d1_final = []
    d2_final = []

    # # # # # # # # # # # # # # stop rule # # # # # # # # # # # # # #

    # # # for d1
    for i in range(len(d1_data)):
        if( i >= 2 ):
            if(d1_data[i-2]==0 and d1_data[i-1]==0 and d1_data[i]==0):
                d1_final.append(d1_data[i])
                break
            else:
                d1_final.append(d1_data[i])
        else:
            d1_final.append(d1_data[i])
    

    # # # for d2
    for i in range(len(d2_data)):
        if( i >= 2 ):
            if(d2_data[i-2]==0 and d2_data[i-1]==0 and d2_data[i]==0):
                d2_final.append(d2_data[i])
                break
            else:
                d2_final.append(d2_data[i])
        else:
            d2_final.append(d2_data[i])
        
    
    # print(d1_final)
    # print(d2_final)


    g1 = d1_final.count(1)
    g2 = d2_final.count(1)
    grades = open(folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/scores.txt',"w")
    grades.write(str(g1) + "\n")
    grades.write(str(g2))
    grades.close()  

    return g1, g2


# sub=13041
# d_grade(sub)