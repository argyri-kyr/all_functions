import numpy as np
import math as m
from cmshiftfun2 import cmshiftfun2
from globalVars import *

def fixationfun(gazedata):
    #initialize data
    windowtime = 0
    gazeno = 0
    j = 0
    k=int(0)
    
    #fix data 
    newfixdata = []
    x0= gazedata[0][1]
    y0= gazedata[0][2]
    t0= gazedata[0][3]

    # 20.3.2023 add-on
    timestamplist = []
    for gdt in range(len(gazedata)):
        timestamplist.append(gazedata[gdt][3])

    mediangazetime = np.median(np.diff(timestamplist))
    # end of add-on
    
    while(gazeno < len(gazedata)-2):
        k=0
        windowgazes=[]

        if(gazedata[j][0]==2406 or gazedata[j][0]==2971):
            print()

        while ( ( j<len(gazedata)-1 ) and ( m.sqrt( (gazedata[j][1]-x0)**2 + (gazedata[j][2]-y0)**2 ) < dispersion ) ):
            windowgazes.append( [ gazedata[j][0], gazedata[j][1], gazedata[j][2], gazedata[j][3] ] )
            j+=1
            # if(  windowgazes!=[] and gazedata[j-1][0]+1==gazedata[j][0] ):
            #     windowgazes.append( [ gazedata[j][0], gazedata[j][1], gazedata[j][2], gazedata[j][3] ] )
            #     j+=1
            # elif(windowgazes==[]):
            #     windowgazes.append( [ gazedata[j][0], gazedata[j][1], gazedata[j][2], gazedata[j][3] ] )
            #     j+=1
            # else:
            #     break

        
        gazestart = gazeno
        gazeend = j-1
        windowtime = windowgazes[-1][3] - windowgazes[0][3] + mediangazetime
        estimatewindowtime = len(windowgazes)*15
        # for t in range(len(windowgazes)):
        #     if(windowgazes[t][0]==534 or windowgazes[t][0]==576):
        #         print("yes")
        # if(estimatewindowtime<windowtime):
        #     print("mpika")
        arraywindowgazes = np.array(windowgazes)
        windowx = np.mean(arraywindowgazes[:,1])
        windowy = np.mean(arraywindowgazes[:,2])
        radvect=[]

        while(k<len(windowgazes)):
            radvect.append( m.sqrt( (windowgazes[k][1]-windowx)**2 + (windowgazes[k][2]-windowy)**2 ) )
            k+=1
        if(len(radvect)!=0):
            minrad = min(radvect)

        if( (windowtime>cutoff) and (minrad<dispersion2) ):
            newwindowgazes=windowgazes
            newgazestart=gazestart
            newgazeend=gazeend

            [newwindowgazes, newgazestart, newgazeend] = cmshiftfun2(gazedata, newwindowgazes, newgazestart, gazeend)

            [newwindowgazes, newgazestart, newgazeend] = cmshiftfun2(gazedata, newwindowgazes, newgazestart, gazeend)
       
            newwindowtime = newwindowgazes[-1][3] - newwindowgazes[0][3] + mediangazetime
    

            if( newwindowtime > cutoff2 ):
                arraywindowgazes = np.array(newwindowgazes)
                newwindowx = np.mean(arraywindowgazes[:,1])
                newwindowy = np.mean(arraywindowgazes[:,2])
                newfixdata.append( [newwindowx, newwindowy, gazedata[newgazestart][0], gazedata[newgazeend][0], newwindowgazes[0][3], newwindowgazes[-1][3], newwindowtime] )


                gazeno = newgazeend+1
                j = gazeno
            else:
                gazeno += 1
                j = gazeno

            if ( gazeno<len(gazedata) ):
                x0 = gazedata[j][1]
                y0 = gazedata[j][2]

        else:
            gazeno+=1
            j=gazeno
        
        if(gazeno<len(gazedata)):
            x0 = gazedata[j][1]
            y0 = gazedata[j][2]


    return newfixdata




