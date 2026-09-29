

from asyncio.windows_events import NULL
import pandas as pd
import xlsxwriter
from asyncio.windows_events import NULL
import calendar
import time


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass



def score_Atest(sub, text):
    from_runcrashes = False

    search1 = getGazesFoldersandClass(sub)   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/

    gazesfolders1, sub1class, subexam = search1[0], search1[1], search1[2]   # gazesfolders1 : ta keimena pou brethikan mesa sto individual
    gazesfolders = gazesfolders1 
    gazesfolders = list(dict.fromkeys(gazesfolders))               

    file = getGazesFolderbyText(sub, subexam, text, gazesfolders, sub1class, from_runcrashes)

    if(file==NULL):
        # print("There is no data for this text")
        return 

    # collect data per exercise
    answerspath = folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/Answers.xlsx'
    if not os.path.exists(answerspath):
        return
    
    data = pd.read_excel(answerspath, header=None)

    a1_data = data.iloc[0,:].tolist()
    a1_data = [x for x in a1_data if not pd.isna(x)]
    a1_data = [int(x) for x in a1_data]

    a2_data = data.iloc[1,:].tolist()
    a2_data = [x for x in a2_data if not pd.isna(x)]
    a2_data = [int(x) for x in a2_data]

    a3_data = data.iloc[2,:].tolist()
    a3_data = [x for x in a3_data if not pd.isna(x)]
    a3_data = [int(x) for x in a3_data]
    
    
    # count ones in data
    score = 0
    
    for i in range(len(a1_data)):
        if( a1_data[i] == 1 ):
            score += 1
    
    for i in range(len(a2_data)):
        if( a2_data[i] == 1 ):
            score += 1
    
    for i in range(len(a3_data)):
        if( a3_data[i] == 1 ):
            score += 1
            
    scorefile = open(folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/scores.txt',"w")
    scorefile.write(str(score))
    scorefile.close()
    
    return 




def main():
    subs = [13373]
    # subs = [subno for subno in range(13370, 13380)]
    
    # texts = ['testlekseona1']
    texts = ['testlekseona1', 'testlekseona2', 'testlekseonb1', 'testlekseonb2', 'raven']
    

    for sub in subs:
        time.sleep(15)
        search1 = getGazesFoldersandClass(sub)   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/

        if( search1 == NULL ):
            print("\nSubject= ", sub, "doesn't exist")
            continue
        print("\nSub = ", sub)
        
        
        for text in texts:
            # print(text)
            score_Atest(sub, text)


main()