


from asyncio.windows_events import NULL
import pandas as pd

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass


text="testaparte"


def e_grade(sub):
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
    
    e1_data = data.iloc[0,:].tolist()
    e1_data = [x for x in e1_data if not pd.isna(x)]
    e1_data = [int(x) for x in e1_data]

    # # # check and convert answers into 0 if answer is Wrong and 1 if answer is Correct
    e2_data_ans = data.iloc[1,:].tolist()
    e2_data_ans = [x for x in e2_data_ans if not pd.isna(x)]
    e2_data_ans = [int(x) for x in e2_data_ans]
    correct_answers = [3, 5, 2, 5, 2, 4, 2, 5]
    e2_data = []
    for pairnumber in range(0, 8, 2):
        if( e2_data_ans[pairnumber]==correct_answers[pairnumber] and e2_data_ans[pairnumber+1]==correct_answers[pairnumber+1] ):
            e2_data.append(1)
        else:
            e2_data.append(0)

    
    e1_final = []
    e2_final = []

    # # # # # # # # # # # # # # stop rule # # # # # # # # # # # # # #

    # # # for e1
    for i in range(len(e1_data)):
        if( i >= 2 ):
            if(e1_data[i-2]==0 and e1_data[i-1]==0 and e1_data[i]==0):
                e1_final.append(e1_data[i])
                break
            else:
                e1_final.append(e1_data[i])
        else:
            e1_final.append(e1_data[i])
    

    # # # for e2
    for i in range(len(e2_data)):
        if( i >= 2 ):
            if(e2_data[i-2]==0 and e2_data[i-1]==0 and e2_data[i]==0):
                e2_final.append(e2_data[i])
                break
            else:
                e2_final.append(e2_data[i])
        else:
            e2_final.append(e2_data[i])
        
    
    # print(e1_final)
    # print(e2_final)


    g1 = e1_final.count(1)
    g2 = e2_final.count(1)
    grades = open(folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/scores.txt',"w")
    grades.write(str(g1) + "\n")
    grades.write(str(g2))
    grades.close()  

    return g1, g2


# sub=13041
# e_grade(sub)