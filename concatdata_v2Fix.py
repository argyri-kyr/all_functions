from asyncio.windows_events import NULL
import os
from os.path import exists


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2, textends


#Edw ginetai sinenwsh twn arxeiwn cutgazes1.txt, cutgazes2.txt,.... se ena arxeio me onoma cutgazes.txt kai omoiws gia ta fixations.txt
def concatdata_v2Fix(sub1, exam, text, filename):
    pagesfile = open(folder1 + "texts/" + text + textends + "/py/pages/pages.txt", "r")
    pages = pagesfile.read(1)

    #Create fixations.txt file
    fixationstxt = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/' + filename + '.txt' #Αυτο το αρχειο ειναι το αντιστοιχο του fixationsFF που δημιουργει το matlab με προσθετη στηλη στο τελος τη στηλη του timestampend
    fixationsfile = open(fixationstxt,'w')
    fixationsfile.close()
    

    for pageno in range(1, int(pages)+1):  
        fixationspagetxt = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/' + filename + str(pageno) + '.txt'

        if( not exists( fixationspagetxt ) ):
            print("File  C:%s not found" % (fixationspagetxt))
            return  NULL        


        open(fixationstxt, 'a').writelines([l for l in open(fixationspagetxt).readlines()])


        # delete old fixationspy files and create new one with the same name, OR, if old fixationspy doesnt exist just create a new one fixationspy
        fixationspypagetxt = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/' + filename + 'py' + str(pageno) + '.txt'

        if(os.path.exists(fixationspypagetxt)):
            os.remove(fixationspypagetxt)

        # rename new fixations into fixationspy
        os.rename(fixationspagetxt, fixationspypagetxt)

