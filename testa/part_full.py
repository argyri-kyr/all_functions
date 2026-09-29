

from asyncio.windows_events import NULL
import xlsxwriter

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass



def part_full(sub, search1):
    texts = ["testaparta", "testapartb", "testapartc", "testapartd", "testaparte", "testapartf"]
    exam = 1

    exist = []
    
    from_runcrashes = False
    gazesfolders1, sub1class, subexam = search1[0], search1[1], search1[2]   # gazesfolders1 : ta keimena pou brethikan mesa sto individual
    gazesfolders = gazesfolders1 
    gazesfolders = list(dict.fromkeys(gazesfolders))               
    
    for text in texts:
        file = getGazesFolderbyText(sub, exam, text, gazesfolders, sub1class, from_runcrashes)

        if(file!=NULL):
            exist.append(file)
    

    if(exist==[]):
        return -1   # there is nothing, this sub doesn't have testa at all

    elif(len(exist)<6):
        return 0     # part testa, there is something

    elif(len(exist)==6):
        return 1
        




def main():
    partpath = folder1 + 'PART_TESTA.xlsx'
    partworkbook = xlsxwriter.Workbook(partpath)
    partworksheet = partworkbook.add_worksheet() 
    partcount = 0

    fullpath = folder1 + 'FULL_TESTA.xlsx'
    fullworkbook = xlsxwriter.Workbook(fullpath)
    fullworksheet = fullworkbook.add_worksheet() 
    fullcount = 0
    

    subs = [x for x in range(13001, 13276)]
     
    for sub in subs:
        search1 = getGazesFoldersandClass(sub)   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/

        if( search1 == NULL ):
            print("Subject = ", sub, " doesn't exist")
            continue

        result = int(part_full(sub, search1))

        if(result==0):
            partworksheet.write(partcount, 0, sub)
            partcount += 1
        
        elif(result==1):
            fullworksheet.write(fullcount, 0, sub)
            fullcount+=1

    partworkbook.close()
    fullworkbook.close()


main()