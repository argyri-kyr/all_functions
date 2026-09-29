from asyncio.windows_events import NULL
import pandas as pd

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass


text="testapartc"


def c_grade(sub):
    from_runcrashes = False

    search1 = getGazesFoldersandClass(sub)   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/

    gazesfolders1, subclass, subexam = search1[0], search1[1], search1[2]   # gazesfolders1 : ta keimena pou brethikan mesa sto individual
    gazesfolders = gazesfolders1 
    gazesfolders = list(dict.fromkeys(gazesfolders))               

    file = getGazesFolderbyText(sub, subexam, text, gazesfolders, subclass, from_runcrashes)

    if(file==NULL):
        # print("There is no data for this text")
        return -1

    # collect data per exercise
    answerspath = folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/Answers.xlsx'
    if not os.path.exists(answerspath):
        return -1
    
    data = pd.read_excel(answerspath, header=None)
   
    c_data = []
    for row in range(16):
        row_data = data.iloc[row,:].tolist()

        # for x in range(len(row_data)):
        #     if(pd.isna(row_data[x]) and row!=15):
        #         print("sub has nan")
        #         break

        row_data = [x for x in row_data if not pd.isna(x)]
        row_data = [int(x) for x in row_data]
        c_data += row_data


    c_final = []

    # # # # # # # # # # # # # # stop rule # # # # # # # # # # # # # #

    stoprulefile = open(folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/stoprule.txt','r')
    stopindex = int(stoprulefile.readline())

    c_final = c_data[:stopindex]

    g = c_final.count(1)
    grades = open(folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/scores.txt',"w")
    grades.write(str(g))
    grades.close()  

    return g



# subs = [i for i in range(13006, 13040)]
# for sub in subs:    
#     c_grade(sub)