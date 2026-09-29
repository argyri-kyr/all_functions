


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2


def loadshifteddata(text, exam, pageno, sub1):

    cutgazesfilepath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/cutgazespy' + str(pageno) + '.txt' 
    cutgazesfile = open(cutgazesfilepath,"r")
    lines = cutgazesfile.readlines()
           
    shiftedx = []
    shiftedy = []

    for p in lines:
        shiftedx.append( float(p.split(None)[1]) )
        shiftedy.append( float(p.split(None)[2]) )  
    
    return shiftedx, shiftedy