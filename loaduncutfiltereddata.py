

import pandas as pd


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2, textends
from GetAndDrawROIS import getROIbounds
from calcROI import calcROI


def loaduncutfiltereddata(text, exam, file, sub1):

    gazesfilepath = folder1 + folder2 + 'subject_' + str(sub1) + '/' + file + '/gazes_filtered.txt' 
    gazesfile = open(gazesfilepath,"r")
    lines = gazesfile.readlines()
    tabcount = lines[0].count('\t')
    lesscolumn = False

    if( tabcount < 5 ):
        lesscolumn = True

    # # # # # # # # # # # # # # # # # # # # # #  NEW GAZES FILTERED FILE  # # # # # # # # # # # # # # # # # # # # # #

    index = []           
    filtered_x = []
    filtered_y = []
    timestamp = []
    validity = []
    validity2 = []
    roi = []


    pageno = 0
    prev_len = 0

    # Here I will load all gazes data into the lists I made before
    for p in lines:
            
        if( int(p.split(None)[0]) == 1 ):
            pageno+= 1

            roibounds = getROIbounds(text, pageno)
            roistartpath = folder1 + 'texts/' + text + textends + '/py/mytext/page(' + str(pageno) + ')/ROIstart/ROIstart.xlsx'
            roistart = pd.read_excel(roistartpath, header=None).values[0][0]


        # Collect data for uncutgazesraw.xlsx
        index.append( int(p.split(None)[0]) )
        filtered_x.append( float(p.split(None)[1]) )                   
        filtered_y.append( float(p.split(None)[2]) )

        if( lesscolumn==False ):
            timestamp.append( float(p.split(None)[3]) )
            validity.append( int(p.split(None)[4]) )
            validity2.append( int(p.split(None)[5]) )  
        else:
            timestamp.append( float(p.split(None)[4]) )
            validity.append( int(p.split(None)[3]) )
            validity2.append( int(p.split(None)[3]) )                          
        
        roi.append( calcROI(roistart, filtered_x[-1], filtered_y[-1], roibounds[0], roibounds[1], roibounds[2], roibounds[3]) )
 
    

    gazesfile.close()

    gazesfiltered = [index, filtered_x, filtered_y, timestamp, validity, validity2, roi]


    # Write gazes_filtered_enhanced.txt if it's existed
    if( lesscolumn ):
        gazesfilteredenhanced = folder1 + folder2 + 'subject_' + str(sub1) + '/' + file + '/gazes_filtered_enhanced.txt' 
        file = open(gazesfilteredenhanced, 'w')

        for i in range(len(index)):
            file.write( str(index[i]) + "\t" + str(filtered_x[i]) + "\t" + str(filtered_y[i]) + "\t" + str(timestamp[i]) + "\t" + str(validity[i]) + "\t" + str(validity2[i]) + "\n" )
        
        file.close()
    
    
    
    return gazesfiltered