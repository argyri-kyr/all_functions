


import numpy as np


def calcMedian(xgazes, ygazes):
    #set parameter filterwindow
    filterwindow = 100     #half median filter window

    # # # #  filter X, Y gazes # # # #
    # filter gazes with a median filter for Y
    ygazes = [0 if i < 0 else i for i in ygazes]
    ygazesfil = ygazes.copy()

    for i in range (filterwindow, len(ygazes)-filterwindow):
        start = int(i-filterwindow)
        end = int(i+filterwindow)+1

        ygazesfil[i] = Median( ygazes, start, end )
        
    
    return ygazesfil
        
        
        
def Median(x, a, b):
    if( a < 0 ):
        a=0
    
    med = np.median( x[a : b] )
    
    if(a==b):
        med = x[a]
    
    return med