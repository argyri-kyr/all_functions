

import numpy as np


from globalVars import folder1, folder2

#Συναρτηση που γραφει το αρχειο cutgazes.txt
#args = { (cutgazesfile : cutgazes.txt file path), (cgi : cutgazes index list), (cgx : cutgazes X list), (cgy : cytgazes Y list), (cgtimestamp : cutgazes timestamp list), (cgroi : cutgazes ROI list) }
#columns of cutgazes.txt:
#1: index
#2: x 
#3: y
#4: timestamp
#5: ROI
def MakeGazesTxt(sub, exam, text, pageno, gazedata):   
    cutgazespagetxt = folder1 + folder2 + 'subject_' + str(sub) + '/all_data/' + text + str(exam) + '/cutgazes' + str(pageno) + '.txt'
    cutgazespagefile = open(cutgazespagetxt,"w")
    cutgazespagefile.close()

    for i in range( len(gazedata) ):
        f = open(cutgazespagetxt,"a")

        for j in range( len(gazedata[0]) ):
            if( isinstance(gazedata[i][j], float) ):
                f.write( str(np.round(gazedata[i][j],2)) + "\t")
            else:
                f.write( str(gazedata[i][j]) + "\t" )
        
        f.write("\n")
    
        f.close()