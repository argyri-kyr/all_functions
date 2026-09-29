import numpy as np
import math as m
from globalVars import *

def cmshiftfun2(gazedata, windowgazes, gazestart, gazeend):

    arraywindowgazes = np.array(windowgazes)
    windowx = np.mean(arraywindowgazes[:,1], axis=0)
    windowy = np.mean(arraywindowgazes[:,2], axis=0)
    newwindowgazes = []
    flag = 0
    newgazeno = gazestart 

    while( newgazeno<len(gazedata) ):
        gazedist = m.sqrt( (gazedata[newgazeno][1]-windowx)**2 + (gazedata[newgazeno][2]-windowy)**2 )
    
        if( gazedist<=dispersion2 and flag==1 ):
            newwindowgazes.append( [gazedata[newgazeno][0], gazedata[newgazeno][1], gazedata[newgazeno][2], gazedata[newgazeno][3]] )
        
        if( gazedist<=dispersion2 and flag==0 ):
            newgazestart = newgazeno
            newwindowgazes.append( [gazedata[newgazeno][0], gazedata[newgazeno][1], gazedata[newgazeno][2], gazedata[newgazeno][3]] )
            flag=1
        
        if( gazedist>dispersion2 and flag==1 ):
            newgazeend = newgazeno-1
            break
        
        if( newgazeno==(len(gazedata)-1) and flag==1 ):
            newgazeend = newgazeno
            break

        newgazeno +=1


    return newwindowgazes, newgazestart, newgazeend