def findlastline(ygazesfil,startsearch,ylastline,ylinestep):
    # find last line end through comparison with the last line median
    # find last line end
    # lastlineend=startsearch-1
    # if startsearch >= len(ygazesfil):
    #     lastlineend = startsearch-1
        
    for i in range(startsearch, len(ygazesfil)):
        if(abs(ygazesfil[i]-ylastline) > ylinestep):
            lastlineend = i-1
            break
        else:
            lastlineend=len(ygazesfil)-1
    return lastlineend