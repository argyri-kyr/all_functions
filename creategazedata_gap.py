
from operator import itemgetter

#Now I will create gazedata list that I will use to find and draw fixations
#args ={ (rindex : cut gazes index), (rx : cut gazes x), (ry : cut gazes y), (rtimestamp : cut gazes timestamp) }
def creategazedata_gap(rindex, rx, ry, rtimestamp, rvalidity, rroi):
    gazedata = []
    for i in range(len(rindex)):
        gazedata.append( [rindex[i], rx[i], ry[i], rtimestamp[i], rvalidity[i], rroi[i]] )
    
    get_n = itemgetter(0)
    gazedata.sort(key=get_n)
    
    return gazedata