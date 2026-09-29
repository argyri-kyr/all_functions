

from asyncio.windows_events import NULL
import os
import xlsxwriter


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass


def convert(sub, exam, text):
    from_runcrashes = False

    proceduredone = True

    search1 = getGazesFoldersandClass(sub)   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/

    if( search1 == NULL ):
        print("Subject doesn't exist")
        return
    
    else:
        gazesfolders1, sub1class, subexam = search1[0], search1[1], search1[2]   # gazesfolders1 : ta keimena pou brethikan mesa sto individual
        gazesfolders = gazesfolders1 
        gazesfolders = list(dict.fromkeys(gazesfolders))               

    file = getGazesFolderbyText(sub, exam, text, gazesfolders, sub1class, from_runcrashes)

    if(file!=NULL):
        if(text=="testaparta"):
            txtpath = folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/testa.txt'

        if(text=="testaparte" or text=="testapartf"):
            txtpath = folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/Answers.txt'


        xlsxpath = folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/Answers.xlsx'

    if( file!=NULL and os.path.exists(txtpath) and not os.path.exists(xlsxpath)):
        workbook = xlsxwriter.Workbook(xlsxpath)
        worksheet = workbook.add_worksheet()

        txtfile = open(txtpath , 'r')
        answers = txtfile.readlines()
        countrows = 0

        for line in answers:
            if(line.strip()):
                s = [ int(x) for x in line.strip().split(" ") ]
                worksheet.write_row(countrows, 0, s)
                countrows += 1

        workbook.close()
            
    else:
        print("\nPossible Exit Reasons for subject = ", sub,":\n1.Check if all files exist in their location - Something is missing\n2.Subject has already .xlsx files for this text")
        return



def main():
    subs = [13274]
    exam = 1
    texts = ["testaparta", "testaparte", "testapartf"]   

    for sub in subs:
        for text in texts:
            convert(sub, exam, text)


main()