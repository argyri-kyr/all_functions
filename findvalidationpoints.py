
from asyncio.windows_events import NULL
import cv2
import numpy as np


from globalVars import folder1, folder2


def findvalidationpoints(sub, text, file):

    imagepath = folder1 + folder2 + '/subject_' + str(sub) + "/" + file + "/validation.png"
    img = cv2.imread(imagepath,0)
    global numpydata
    numpydata = np.asarray(img)

    points = []
    almostwhite = [ i for i in range(245,256) ]


    #Find up and down limits in each line
    print("Start Validation process for subject=%d, text=%s " %(sub, text))
    times = 0
    for y in range(2,len(numpydata)):
        for x in range(len(numpydata[y])):
            times += 1

            print("\rProgress: {0}%".format( int( times/((len(numpydata)-2)*len(numpydata[0])-1)*100 ) ), end="\r")   #  progress message

            if( numpydata[y][x] in almostwhite ):
                    points.append( [x,y] )
        

    # store data
    validationdatatxt = folder1 + folder2 + '/subject_' + str(sub) + "/" + file + '/' + text + '_validation.txt'
    validationdatafile = open(validationdatatxt, 'w')
    for i in range(len(points)):
        validationdatafile.write( str(points[i][0]) + '\t' + str(points[i][1]) + '\n' )
    validationdatafile.close()

    return imagepath
     