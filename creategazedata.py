
from operator import itemgetter

#Now I will create gazedata list that I will use to find and draw fixations
#args ={ (rindex : cut gazes index), (rx : cut gazes x), (ry : cut gazes y), (rtimestamp : cut gazes timestamp) }
def CreateGazeData(cgdata):
    gazedata = []

    for i in range(len(cgdata[0])):
        sublist = []
        for j in range(len(cgdata)):
            sublist.append(cgdata[j][i])
        gazedata.append( sublist )
    
    get_n = itemgetter(0)
    gazedata.sort(key=get_n)
    
    return gazedata