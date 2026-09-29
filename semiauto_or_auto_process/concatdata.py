
from asyncio.windows_events import NULL
import os
from os.path import exists
import shutil

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2, textends


#Edw ginetai sinenwsh twn arxeiwn cutgazes1.txt, cutgazes2.txt,.... se ena arxeio me onoma cutgazes.txt kai omoiws gia ta fixations.txt
def concatdata(sub1, exam, text, filename1, filename2):
    pagesfile = open(folder1 + "texts/" + text + textends + "/py/pages/pages.txt", "r")
    pages = pagesfile.read()

    #Create cutgazes.txt file
    cutgazestxt = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/' + filename1 + '.txt'
    cutgazesfile = open(cutgazestxt,"w")
    cutgazesfile.close()

    #Create fixations.txt file
    fixationstxt = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/' + filename2 + '.txt' #Αυτο το αρχειο ειναι το αντιστοιχο του fixationsFF που δημιουργει το matlab με προσθετη στηλη στο τελος τη στηλη του timestampend
    fixationsfile = open(fixationstxt,'w')
    fixationsfile.close()
    

    for pageno in range(1, int(pages)+1):  
        cutgazespagetxt = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/' + filename1 + str(pageno) + '.txt'
        fixationspagetxt = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/' + filename2 + str(pageno) + '.txt'

        if( not exists( cutgazespagetxt ) ):
            print("File  C:%s not found" % (cutgazespagetxt))
            return  NULL
        if( not exists( fixationspagetxt ) ):
            print("File  C:%s not found" % (fixationspagetxt))
            return  NULL        

        # # append page number into cutgazes.txt
        cutgazeslist = [l for l in open(cutgazespagetxt).readlines()]
        for cl in range(len(cutgazeslist)):
            cgrow = cutgazeslist[cl].split('\t')
            cgrow.insert(5, str(pageno))
            cgrow = "\t".join(cgrow)
            cutgazeslist[cl] = cgrow
        # # end of append page number

        open(cutgazestxt, 'a').writelines(cutgazeslist)

        open(fixationstxt, 'a').writelines([l for l in open(fixationspagetxt).readlines()])

        cutgazespagetxt_final = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/' + filename1 + 'py' + str(pageno) + '.txt'
        shutil.copyfile(cutgazespagetxt, cutgazespagetxt_final)
        
        fixationspagetxt_final = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/' + filename2 + 'py' + str(pageno) + '.txt'
        shutil.copyfile(fixationspagetxt, fixationspagetxt_final)

        os.remove(cutgazespagetxt)
        os.remove(fixationspagetxt)
