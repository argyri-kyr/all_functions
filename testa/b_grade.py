


from asyncio.windows_events import NULL
import pandas as pd

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass


text="testapartb"


def b_grade(sub):
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

    b1_data = data.iloc[0,:].tolist()
    b1_data = [x for x in b1_data if not pd.isna(x)]
    b1_data = [int(x) for x in b1_data]

    b2_data = data.iloc[1,:].tolist()
    b2_data = [x for x in b2_data if not pd.isna(x)]
    b2_data = [int(x) for x in b2_data]

    
    b1_final = []
    b2_final = []

    # # # # # # # # # # # # # # stop rule # # # # # # # # # # # # # #

    # # # for b1
    checkindexes = [ [2], [4], [6,8], [9,11,12], [14,15], [17,20], [22,24,25], [26,28,30], [31,33,34] ]
    stopped_indexes = [-1, -1, 8, 12, 16, 20, 25, 30, 35]
    stopindex = len(b1_data)

    correctfound = 0

    for ino in range(len(checkindexes)):
        if(ino>=2):     
            correctfound = 0  

            for jno in range(len(checkindexes[ino])):
                if(checkindexes[ino][jno]<len(b1_data)):
                    if(b1_data[checkindexes[ino][jno]]==1):
                        correctfound = 1

            for jno in range(len(checkindexes[ino-1])):
                if(checkindexes[ino-1][jno]<len(b1_data)):
                    if(b1_data[checkindexes[ino-1][jno]]==1):
                        correctfound = 1

            for jno in range(len(checkindexes[ino-2])):
                if(checkindexes[ino-2][jno]<len(b1_data)):
                    if(b1_data[checkindexes[ino-2][jno]]==1):
                        correctfound = 1
            
            if(correctfound == 0):
                stopindex = stopped_indexes[ino]
                break

            #         if( b1_data[checkindexes[ino]]==0 and b1_data[checkindexes[ino-1]]==0 and b1_data[checkindexes[ino-2]]==0 ):
            #             stopindex = checkindexes[ino]
    
    
    for j in range(stopindex):
        b1_final.append(b1_data[j])
    

    # # # for b2
    for i in range(len(b2_data)):
        if( i >= 2 ):
            if(b2_data[i-2]==0 and b2_data[i-1]==0 and b2_data[i]==0):
                b2_final.append(b2_data[i])
                break
            else:
                b2_final.append(b2_data[i])
        else:
            b2_final.append(b2_data[i])
        
    
    # print(b1_final)
    # print(b2_final)


    g1 = b1_final.count(1)
    g2 = b2_final.count(1)
    grades = open(folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/scores.txt',"w")
    grades.write(str(g1) + "\n")
    grades.write(str(g2))
    grades.close()  

    return g1, g2

# sub=13170
# b_grade(sub)