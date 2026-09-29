

from fixationfun import fixationfun
from calcROI import calcROI
import numpy as np

def fixationfungap(gazedata_gap, roistart, roibounds):

    indexcolumn = 0
    validitycolumn = 5

    gap_data = []


    # find validgazestart, validgazeend
    validgazestart = []
    validgazeend = []
    index_validgazestart = []
    index_validgazeend = []

    for i in range( len(gazedata_gap) ):

        if( i==0 and gazedata_gap[i][validitycolumn]!=0 ):
            validgazestart.append( i )
            index_validgazestart.append( gazedata_gap[i][indexcolumn] )

        if( i>0 and gazedata_gap[i-1][validitycolumn]==0 and gazedata_gap[i][validitycolumn]!=0 ):
            validgazestart.append( i )
            index_validgazestart.append( gazedata_gap[i][indexcolumn] )

        if( i>0 and gazedata_gap[i-1][validitycolumn]!=0 and gazedata_gap[i][validitycolumn]==0 ):
            validgazeend.append( i-1 ) 
            index_validgazeend.append( gazedata_gap[i-1][indexcolumn] )
        
        if( i==len(gazedata_gap)-1 and gazedata_gap[i][validitycolumn]!=0 ):
            validgazeend.append( i ) 
            index_validgazeend.append( gazedata_gap[i][indexcolumn] ) 

        # if( i==0 and gazedata_gap[i][validitycolumn]!=0 and gazedata_gap[i+1][validitycolumn]==0):
        #     validgazeend.append( i ) 
        #     index_validgazeend.append( gazedata_gap[i][indexcolumn] )             
        
        # if( i==len(gazedata_gap)-1 and gazedata_gap[i][validitycolumn]!=0 ):
        #     validgazeend.append( i ) 
        #     index_validgazeend.append( gazedata_gap[i][indexcolumn] ) 
        
        # if( i>0 and i<len(gazedata_gap)-1 and gazedata_gap[i][validitycolumn]==0 and gazedata_gap[i+1][validitycolumn]!=0 ):
        #     validgazestart.append( i+1 )
        #     index_validgazestart.append( gazedata_gap[i+1][indexcolumn] )
        
        # if( i>0 and i<len(gazedata_gap)-1 and gazedata_gap[i][validitycolumn]!=0 and gazedata_gap[i+1][validitycolumn]==0 ):
        #     validgazeend.append( i )  
        #     index_validgazeend.append( gazedata_gap[i][indexcolumn] ) 



    # find firstfixation, lastfixation, values of fixations in spaces
    firstfixation = []
    lastfixation = []
    fixationdata = []

    for j in range(len(validgazestart)):
        cutgazes_gap = gazedata_gap[validgazestart[j]:validgazeend[j]+1]

        newfixation = fixationfun( cutgazes_gap )
        fixationdata += newfixation

        if(  newfixation != [] ):
            if( firstfixation==[] ):
                firstfixation.append(1)
                lastfixation.append( len(newfixation) )
            else:
                if(all(lf == 0 for lf in lastfixation)):
                    lastnozeroindex = 0
                else:
                    lastnozeroindex = np.max(np.nonzero(lastfixation))
                firstfixation.append( lastfixation[lastnozeroindex] + 1 )
                lastfixation.append( lastfixation[lastnozeroindex] + len(newfixation) )
        
        else:
            firstfixation.append(0)
            lastfixation.append(0)


    # omit-merge spaces with no fixations
    nonvalid_indexes = []
    for i in range(len(firstfixation)):
        if( firstfixation[i] == 0 ):
            nonvalid_indexes.append(i)
    
    validgazestart  = [ validgazestart[i] for i in range(len(validgazestart))  if i not in nonvalid_indexes]
    validgazeend  = [ validgazeend[i] for i in range(len(validgazeend))  if i not in nonvalid_indexes]
    firstfixation  = [ firstfixation[i] for i in range(len(firstfixation))  if i not in nonvalid_indexes]
    lastfixation  = [ lastfixation[i] for i in range(len(lastfixation))  if i not in nonvalid_indexes]
    index_validgazestart = [ index_validgazestart[i] for i in range(len(index_validgazestart))  if i not in nonvalid_indexes]
    index_validgazeend = [ index_validgazeend[i] for i in range(len(index_validgazeend))  if i not in nonvalid_indexes]


    # gap struct
    if( len(firstfixation) >= 2 ):
        for j in range(len(validgazestart)-1):
            if( newfixation != [] ):
                gap_start = lastfixation[j]
                gap_end = firstfixation[j+1]

                roi_first_fixation = calcROI(roistart, fixationdata[gap_start-1][0], fixationdata[gap_start-1][1], roibounds[0], roibounds[1], roibounds[2], roibounds[3])  #Υπολογιζω σε ποιο ROI ανηκει το πρωτο fixation
                roi_last_fixation = calcROI(roistart, fixationdata[gap_end-1][0], fixationdata[gap_end-1][1], roibounds[0], roibounds[1], roibounds[2], roibounds[3])  #Υπολογιζω σε ποιο ROI ανηκει το τελευταιο fixation
                
                gaptime = gazedata_gap[validgazestart[j+1]][3] - gazedata_gap[validgazeend[j]+1][3]

                my_gap = [ gap_start, gap_end, roi_first_fixation, roi_last_fixation, fixationdata[gap_start-1][0], fixationdata[gap_start-1][1], fixationdata[gap_end-1][0], fixationdata[gap_end-1][1], gaptime ] 
            

                gap_data += [my_gap]
    

        # check for last fixation
        invalidgazefound = False
        index_invalidgaze = -1
        index_start = fixationdata[-1][3] - gazedata_gap[0][0]
        for k in range(index_start, len(gazedata_gap)):
            if( gazedata_gap[k][validitycolumn] == 0 ):
                invalidgazefound = True
                index_invalidgaze = k
                break
        if(invalidgazefound == True):
            extra_gap_start = lastfixation[-1]

            extra_roi = calcROI(roistart, fixationdata[extra_gap_start-1][0], fixationdata[extra_gap_start-1][1], roibounds[0], roibounds[1], roibounds[2], roibounds[3])  #Υπολογιζω σε ποιο ROI ανηκει το πρωτο fixation
            
            extrarow_duration = gazedata_gap[-1][3] - gazedata_gap[index_invalidgaze][3]
        
            my_gap = [ lastfixation[-1], 0, extra_roi, 0, fixationdata[extra_gap_start-1][0], fixationdata[extra_gap_start-1][1], 1920, fixationdata[extra_gap_start-1][1], extrarow_duration ]

            gap_data += [my_gap]
       


    return fixationdata, index_validgazestart, index_validgazeend, firstfixation, lastfixation, gap_data
        
