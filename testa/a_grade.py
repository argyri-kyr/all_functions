

from asyncio.windows_events import NULL
import pandas as pd

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass


text="testaparta"


def a_grade(sub):
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

    a1_data = data.iloc[0,:].tolist()
    a1_data = [x for x in a1_data if not pd.isna(x)]
    a1_data = [int(x) for x in a1_data]

    a2_data = data.iloc[1,:].tolist()
    a2_data = [x for x in a2_data if not pd.isna(x)]
    a2_data = [int(x) for x in a2_data]

    
    a1_final = []
    a2_final = []


    # # # # # # # # # # # # # # stop rule # # # # # # # # # # # # # #

    # # # for a1
    for i in range(len(a1_data)):
        if( i >= 4 ):
            if(a1_data[i-4]==0 and a1_data[i-3]==0 and a1_data[i-2]==0 and a1_data[i-1]==0 and a1_data[i]==0):
                a1_final.append(a1_data[i])
                break
            else:
                a1_final.append(a1_data[i])
        else:
            a1_final.append(a1_data[i])
    
    # # # for a2
    for i in range(len(a2_data)):
        if( i >= 4 ):
            if(a2_data[i-4]==0 and a2_data[i-3]==0 and a2_data[i-2]==0 and a2_data[i-1]==0 and a2_data[i]==0):
                a2_final.append(a2_data[i])
                break
            else:
                a2_final.append(a2_data[i])
        else:
            a2_final.append(a2_data[i])
    
    # print(a1_final)
    # print(a2_final)


    g1 = a1_final.count(1)
    g2 = a2_final.count(1)
    grades = open(folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/scores.txt',"w")
    grades.write(str(g1) + "\n")
    grades.write(str(g2))
    grades.close()  

    return g1, g2

# sub=13041
# a_grade(sub)