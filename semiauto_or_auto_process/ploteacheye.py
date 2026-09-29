


from asyncio.windows_events import NULL
import pandas as pd
import numpy as np


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2, textends
from GetAndDrawROIS import getROIbounds
from calcROI import calcROI


def ploteacheye(text, file, sub1, pagenumber):

    gazesfilepath = folder1 + folder2 + 'subject_' + str(sub1) + '/' + file + '/gazes.txt' 
    gazesfile = open(gazesfilepath,"r")
    lines = gazesfile.readlines()

    for p in lines:
        size = len( p.split(None) )
        break

    if( size < 7 ):
        return NULL, NULL
    
    else:
        # # # # # # # # # # # # # # # # # # # # # #  NEW GAZES FILE  # # # # # # # # # # # # # # # # # # # # # #

        index = []
                      
        leftx = []
        lefty = []
        leftz = []
        leftvalid = []

        rightx = []
        righty = []
        rightz = []
        rightvalid = []

        timestamp = []

        leftpupilsize = []
        leftpupilvalid = []

        rightpupilsize = []
        rightpupilvalid = []

        roileft = []
        roiright = []


        finalx = []
        finaly = []
        finalroi = []
        finalvalid = []
        vergence = []
        pupilsize = []


        finalx_lefteye = []
        finaly_lefteye = []
        finalx_righteye = []
        finaly_righteye= []
        

        pageno = 0

        # Here I will load all gazes data into the lists I made before
        for p in lines:
             
            if( int(p.split(None)[0]) == 1 ):
                pageno+= 1

                roibounds = getROIbounds(text, pageno)
                roistartpath = folder1 + 'texts/' + text + textends + '/py/mytext/page(' + str(pageno) + ')/ROIstart/ROIstart.xlsx'
                roistart = pd.read_excel(roistartpath, header=None).values[0][0]


            if(pageno == pagenumber):

                index.append( int(p.split(None)[0]) )

                leftx.append( float(p.split(None)[1]) )                   
                lefty.append( float(p.split(None)[2]) )
                leftz.append( float(p.split(None)[3]) )
                leftvalid.append( int(p.split(None)[4]) )

                rightx.append( float(p.split(None)[5]) )                   
                righty.append( float(p.split(None)[6]) )
                rightz.append( float(p.split(None)[7]) )
                rightvalid.append( int(p.split(None)[8]) )            
                
                timestamp.append( float(p.split(None)[9]) )


                if( size < 13 ):
                    leftpupilsize.append(0)
                    leftpupilvalid.append(0)

                    rightpupilsize.append(0)
                    rightpupilvalid.append(0)
                
                else:                    
                    leftpupilsize.append( float(p.split(None)[10]) )
                    leftpupilvalid.append( int(p.split(None)[11]) )

                    rightpupilsize.append( float(p.split(None)[12]) )
                    rightpupilvalid.append( int(p.split(None)[13]) )


                roileft.append( calcROI(roistart, leftx[-1], lefty[-1], roibounds[0], roibounds[1], roibounds[2], roibounds[3]) )
                roiright.append( calcROI(roistart, rightx[-1], righty[-1], roibounds[0], roibounds[1], roibounds[2], roibounds[3]) )

                    
                finalx_lefteye.append(leftx[-1])
                finaly_lefteye.append(lefty[-1])
                finalx_righteye.append(rightx[-1])
                finaly_righteye.append(righty[-1])
                
                pupilsize.append( (leftpupilsize[-1]+rightpupilsize[-1])/2 )
                vergence.append( np.sqrt((leftx[-1]-rightx[-1])**2+(lefty[-1]-righty[-1])**2) )
                
        
        
        gazesfile.close()


        uncutgazesraw = [index, leftx, lefty, leftz, leftvalid, rightx, righty, rightz, rightvalid, timestamp, leftpupilsize, leftpupilvalid, rightpupilsize, rightpupilvalid, roileft, roiright]
        uncutgazes = [index, finalx, finaly, timestamp, finalroi, finalvalid, vergence, pupilsize] 
        oneeyeindexes = [finalx_lefteye, finaly_lefteye, finalx_righteye, finaly_righteye]

        
        return uncutgazesraw, uncutgazes, oneeyeindexes

              