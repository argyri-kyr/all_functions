


from asyncio.windows_events import NULL
import pandas as pd
import numpy as np
import xlsxwriter


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2, textends
from GetAndDrawROIS import getROIbounds
from calcROI import calcROI


def loaduncutdata_hardcases(text, exam, file, sub1, onlylefteye_check, onlyrighteye_check):

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
        
        negativecheck = []
        finalx_lefteye = []
        finaly_lefteye = []
        finalx_righteye = []
        finaly_righteye= []

        pageno = 0
        prev_len = 0

        # Here I will load all gazes data into the lists I made before
        for p in lines:
             
            if( int(p.split(None)[0]) == 1 ):
                if( 'uncutgazesrawtxt' in locals() ):
                    prev_len = len(index)
                    uncutgazesrawbook.close()
                if( 'uncutgazestxt' in locals() ):
                    uncutgazesbook.close()
                
                pageno+= 1
                
                if( text=='decodedecision' and pageno>6 ):
                    break

                roibounds = getROIbounds(text, pageno)
                roistartpath = folder1 + 'texts/' + text + textends + '/py/mytext/page(' + str(pageno) + ')/ROIstart/ROIstart.xlsx'
                roistart = pd.read_excel(roistartpath, header=None).values[0][0]

                uncutgazesrawtxt = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/uncutgazesraw' + str(pageno) + '.xlsx' #Αυτο το αρχειο ειναι το αντιστοιχο του fixationsFF που δημιουργει το matlab με προσθετη στηλη στο τελος τη στηλη του timestampend
                uncutgazesrawbook  = xlsxwriter.Workbook(uncutgazesrawtxt)
                uncutgazesrawsheet = uncutgazesrawbook.add_worksheet()

                uncutgazestxt = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/uncutgazes' + str(pageno) + '.xlsx' #Αυτο το αρχειο ειναι το αντιστοιχο του fixationsFF που δημιουργει το matlab με προσθετη στηλη στο τελος τη στηλη του timestampend
                uncutgazesbook  = xlsxwriter.Workbook(uncutgazestxt)
                uncutgazessheet = uncutgazesbook.add_worksheet()


            # Collect data for uncutgazesraw.xlsx
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

            leftpupilsize.append( float(p.split(None)[10]) )
            leftpupilvalid.append( int(p.split(None)[11]) )

            rightpupilsize.append( float(p.split(None)[12]) )
            rightpupilvalid.append( int(p.split(None)[13]) )

            roileft.append( calcROI(roistart, leftx[-1], lefty[-1], roibounds[0], roibounds[1], roibounds[2], roibounds[3]) )
            roiright.append( calcROI(roistart, rightx[-1], righty[-1], roibounds[0], roibounds[1], roibounds[2], roibounds[3]) )
        

            uncutgazesrawsheet.write(len(index)-1-prev_len, 0, index[-1])
            uncutgazesrawsheet.write(len(leftx)-1-prev_len, 1, leftx[-1])
            uncutgazesrawsheet.write(len(lefty)-1-prev_len, 2, lefty[-1])
            uncutgazesrawsheet.write(len(leftz)-1-prev_len, 3, leftz[-1])
            uncutgazesrawsheet.write(len(leftvalid)-1-prev_len, 4, leftvalid[-1])
            uncutgazesrawsheet.write(len(rightx)-1-prev_len, 5, rightx[-1])
            uncutgazesrawsheet.write(len(righty)-1-prev_len, 6, righty[-1])
            uncutgazesrawsheet.write(len(rightz)-1-prev_len, 7, rightz[-1])
            uncutgazesrawsheet.write(len(rightvalid)-1-prev_len, 8, rightvalid[-1])
            uncutgazesrawsheet.write(len(timestamp)-1-prev_len, 9, timestamp[-1])
            uncutgazesrawsheet.write(len(leftpupilsize)-1-prev_len, 10, leftpupilsize[-1])
            uncutgazesrawsheet.write(len(leftpupilvalid)-1-prev_len, 11, leftpupilvalid[-1])
            uncutgazesrawsheet.write(len(rightpupilsize)-1-prev_len, 12, rightpupilsize[-1])
            uncutgazesrawsheet.write(len(rightpupilvalid)-1-prev_len, 13, rightpupilvalid[-1])
            uncutgazesrawsheet.write(len(roileft)-1-prev_len, 14, roileft[-1])
            uncutgazesrawsheet.write(len(roiright)-1-prev_len, 15, roiright[-1])


            # Collect data for uncutgazes.xlsx
            if( onlylefteye_check==1 and onlyrighteye_check!=1 ):
                finalx.append( leftx[-1] )
                finaly.append( lefty[-1] )
                finalroi.append( calcROI(roistart, finalx[-1], finaly[-1], roibounds[0], roibounds[1], roibounds[2], roibounds[3]) )
                if( leftvalid[-1]==1 and leftx[-1]>0 and lefty[-1]>0 ):
                    finalvalid.append(1)
                else:
                    finalvalid.append(0)
    
                
                    
            elif( onlyrighteye_check==1 and onlylefteye_check!=1 ):
                finalx.append( rightx[-1] )
                finaly.append( righty[-1] )
                finalroi.append( calcROI(roistart, finalx[-1], finaly[-1], roibounds[0], roibounds[1], roibounds[2], roibounds[3]) )
                if( rightvalid[-1]==1 and rightx[-1]>0 and righty[-1]>0 ):
                    finalvalid.append(1)
                else:
                    finalvalid.append(0)
            
            
            else:
                if( leftvalid[-1]==1 and rightvalid[-1]==1): # and leftx[-1]>0 and lefty[-1]>0 and rightx[-1]>0 and righty[-1]>0 ):
                    finalx.append( (leftx[-1]+rightx[-1])/2 )
                    finaly.append( (lefty[-1]+righty[-1])/2 )
                    finalvalid.append(1)
                # elif( leftvalid[-1]==0 and rightvalid[-1]==1):
                #     finalx.append( rightx[-1] )
                #     finaly.append( righty[-1] )
                #     finalvalid.append(0)
                # elif( leftvalid[-1]==1 and rightvalid[-1]==0):
                #     finalx.append( leftx[-1] )
                #     finaly.append( lefty[-1] )
                #     finalvalid.append(0)
                # else:
                #     finalx.append( (leftx[-1]+rightx[-1])/2 )
                #     finaly.append( (lefty[-1]+righty[-1])/2 )
                #     finalvalid.append(0)
                else:
                    finalx.append(0)
                    finaly.append(0)
                    finalvalid.append(0)
                
                finalroi.append( calcROI(roistart, finalx[-1], finaly[-1], roibounds[0], roibounds[1], roibounds[2], roibounds[3]) )
                
                # finalx.append( (leftx[-1]+rightx[-1])/2 )
                # finaly.append( (lefty[-1]+righty[-1])/2 )
                # finalroi.append( calcROI(roistart, finalx[-1], finaly[-1], roibounds[0], roibounds[1], roibounds[2], roibounds[3]) )
                # if( leftvalid[-1]==1 and rightvalid[-1]==1 ):   # and leftx[-1]>0 and lefty[-1]>0 and rightx[-1]>0 and righty[-1]>0 
                #     finalvalid.append(1)
                # else:
                #     finalvalid.append(0)
            
            
                
            if( (lefty[-1]<0 or righty[-1]<0) and ((lefty[-1]+righty[-1])/2)>0 and leftvalid[-1]==1 and rightvalid[-1]==1 ):
                negativecheck.append(1)
            elif( (leftx[-1]<0 or rightx[-1]<0) and ((leftx[-1]+rightx[-1])/2)>0 and leftvalid[-1]==1 and rightvalid[-1]==1 ):
                negativecheck.append(1)
            else:
                negativecheck.append(0)
            
            
            finalx_lefteye.append(leftx[-1])
            finaly_lefteye.append(lefty[-1])
            finalx_righteye.append(rightx[-1])
            finaly_righteye.append(righty[-1])
                
            pupilsize.append( (leftpupilsize[-1]+rightpupilsize[-1])/2 )
            vergence.append( np.sqrt((leftx[-1]-rightx[-1])**2+(lefty[-1]-righty[-1])**2) )

            uncutgazessheet.write(len(index)-1-prev_len, 0, index[-1])
            uncutgazessheet.write(len(finalx)-1-prev_len, 1, finalx[-1])
            uncutgazessheet.write(len(finaly)-1-prev_len, 2, finaly[-1])
            uncutgazessheet.write(len(timestamp)-1-prev_len, 3, timestamp[-1])
            uncutgazessheet.write(len(finalroi)-1-prev_len, 4, finalroi[-1])
            uncutgazessheet.write(len(finalvalid)-1-prev_len, 5, finalvalid[-1])
            uncutgazessheet.write(len(vergence)-1-prev_len, 6, vergence[-1])
            uncutgazessheet.write(len(pupilsize)-1-prev_len, 7, pupilsize[-1])
                
        
        
        gazesfile.close()
        uncutgazesrawbook.close()
        uncutgazesbook.close()


        uncutgazesraw = [index, leftx, lefty, leftz, leftvalid, rightx, righty, rightz, rightvalid, timestamp, leftpupilsize, leftpupilvalid, rightpupilsize, rightpupilvalid, roileft, roiright]
        uncutgazes = [index, finalx, finaly, timestamp, finalroi, finalvalid, vergence, pupilsize] 
        oneeyeindexes = [finalx_lefteye, finaly_lefteye, finalx_righteye, finaly_righteye]

        
        return uncutgazesraw, uncutgazes, negativecheck, oneeyeindexes