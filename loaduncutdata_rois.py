


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2


def loaduncutdata_rois(file, sub1):
    # check if subject has old or new data, if old data found then work with gazes.txt, else work with gazespy.txt
    gazesfilepath = folder1 + folder2 + 'subject_' + str(sub1) + '/' + file + '/gazes.txt' 
    gazesfile = open(gazesfilepath,"r")
    lines = gazesfile.readlines()
    for p in lines:
        size = len( p.split(None) )
        break

    if( size > 5 ):
        gazesfilepath = folder1 + folder2 + 'subject_' + str(sub1) + '/' + file + '/gazespy.txt' 
        gazesfile = open(gazesfilepath,"r")
        lines = gazesfile.readlines()


    index = []
    finalx = []
    finaly = []
    timestamp = []
    roi = []


    # Here I will load all gazes data into the lists I made before
    for p in lines:
        # Collect data for uncutgazesraw.xlsx
        index.append( int(p.split(None)[0]) )
        finalx.append(float(p.split(None)[1]) )
        finaly.append(float(p.split(None)[2]) )
        timestamp.append( float(p.split(None)[3]) )
        roi.append( int(p.split(None)[4]) )
            

        
        return index, finalx, finaly, timestamp, roi