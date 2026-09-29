

from globalVars import folder1, folder2


def loadcutgazesdata(sub1, exam, text):
    cutgazesfilepath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/cutgazes.txt'
    cutgazesfile = open(cutgazesfilepath,"r")
    lines = cutgazesfile.readlines()

    index = [] 
    x = []
    y = []
    timestamp = []
    roi = []  
    pagenumber = []
    validity = []
    vergence = []
    pupilsize = []

    for p in lines:
        index.append( int(p.split(None)[0]) )
        x.append( float(p.split(None)[1]) )                   
        y.append( float(p.split(None)[2]) )
        timestamp.append( float(p.split(None)[3]) )
        roi.append( int(p.split(None)[4]) )
        pagenumber.append( int(p.split(None)[5]) )
        validity.append( float(p.split(None)[6]) )                   
        vergence.append( float(p.split(None)[7]) )
        pupilsize.append( float(p.split(None)[8]) )

    return index, x, y, timestamp, roi, pagenumber, validity, vergence, pupilsize