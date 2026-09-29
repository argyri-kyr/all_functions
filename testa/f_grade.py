


from asyncio.windows_events import NULL
import pandas as pd


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass


text="testapartf"



def f_grade(sub):
    from_runcrashes = False

    search1 = getGazesFoldersandClass(sub)   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/

    gazesfolders1, sub1class, subexam = search1[0], search1[1], search1[2]   # gazesfolders1 : ta keimena pou brethikan mesa sto individual
    gazesfolders = gazesfolders1 
    gazesfolders = list(dict.fromkeys(gazesfolders))               

    file = getGazesFolderbyText(sub, subexam, text, gazesfolders, sub1class, from_runcrashes)

    if(file==NULL):
        # print("There is no data for this text")
        return -1

    # collect data per exercise
    answerspath = folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/Answers.xlsx'
    if not os.path.exists(answerspath):
        return -1
    
    data = pd.read_excel(answerspath, header=None)
    
     # # # check and convert answers into 0 if answer is Wrong and 1 if answer is Correct

    f1_data_ans = data.iloc[0,:].tolist()
    f1_data_ans = [x for x in f1_data_ans if not pd.isna(x)]
    f1_data_ans = [int(x) for x in f1_data_ans]
    correct_answers = [4, 2, 4, 1, 1, 2, 3]
    f1_data = []
    for pairnumber in range(7):
        if( f1_data_ans[pairnumber]==correct_answers[pairnumber] ):
            f1_data.append(1)
        else:
            f1_data.append(0)


    f2_data_ans = data.iloc[1,:].tolist()
    f2_data_ans = [x for x in f2_data_ans if not pd.isna(x)]
    f2_data_ans = [int(x) for x in f2_data_ans]
    correct_answers = [4, 2, 1, 1, 3, 2, 3]
    f2_data = []
    for pairnumber in range(7):
        if( f2_data_ans[pairnumber]==correct_answers[pairnumber] ):
            f2_data.append(1)
        else:
            f2_data.append(0)


    f3_data_ans = data.iloc[2,:].tolist()
    f3_data_ans = [x for x in f3_data_ans if not pd.isna(x)]
    f3_data_ans = [int(x) for x in f3_data_ans]
    correct_answers = [4, 2, 4, 1, 3, 1, 3]
    f3_data = []
    for pairnumber in range(7):
        if( f3_data_ans[pairnumber]==correct_answers[pairnumber] ):
            f3_data.append(1)
        else:
            f3_data.append(0)


    f1_final = []
    f2_final = []
    f3_final = []
    zeros1 = 0
    zeros2 = 0
    zeros3 = 0


    # # # # # # # # # # # # # # stop rule # # # # # # # # # # # # # #

    # # # for f1
    for i in range(len(f1_data)):
        if( f1_data[i]==0 and zeros1<5 ):
            f1_final.append(f1_data[i])
            zeros1 += 1
            if(zeros1==5):
                break
        else:
            f1_final.append(f1_data[i])
        

    # # # for f2
    if( zeros1 < 5 ):
        for i in range(len(f2_data)):
            if( f2_data[i]==0 and zeros2<5 ):
                f2_final.append(f2_data[i])
                zeros2 += 1
                if(zeros2==5):
                    break
            else:
                f2_final.append(f2_data[i])


    # # # for f3
    if( zeros2 < 5 ):
        for i in range(len(f3_data)):
            if( f3_data[i]==0 and zeros3<5 ):
                f3_final.append(f3_data[i])
                zeros3 += 1
                if(zeros3==5):
                    break
            else:
                f3_final.append(f3_data[i])
    

    # print(f1_final)
    # print(f2_final)
    # print(f3_final)


    g1 = f1_final.count(1)
    g2 = f2_final.count(1)
    g3 = f3_final.count(1)
    grades = open(folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/scores.txt',"w")
    grades.write(str(g1) + "\n")
    grades.write(str(g2) + "\n")
    grades.write(str(g3))
    grades.close()  

    return g1+g2+g3


# sub=13041
# f_grade(sub)