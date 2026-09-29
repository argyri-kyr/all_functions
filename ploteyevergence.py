

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
import math 
import cv2


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2, pyimagepath, dim


def ploteyevergence(sub1, text, textends, pageno, exam, vergence):
    global gtext, gtextends, gpageno
    gtext , gtextends, gpageno = text, textends, pageno

    # # # # # # # # # # # # # # # # # # # # # #  PLOT NUMBER 1  # # # # # # # # # # # # # # # # # # # # # # 

    # # Calculate vergence distance
    # count_verg = -1
    # vergence_dist = []
    # for i in range(90, 100):
    #     count_verg = count_verg + 1
    #     vergence_dist.append( math.sqrt( (abs(vergence[i][3]-vergence[i][1]))^2 + (abs(vergence[i][4]-vergence[i][2]))^2 ) )
       
    # # # # Plot vergence
    # # keep y constant, and plot leftx with leftx + distance (left-right eye)
    # global pointsleft, pointsright
    # pointsleft = []
    # pointsright = []
    # fixed_y = 500
    # eyeeye = -1
    # for i in range(90, 100):
    #     eyeeye = eyeeye + 1
    #     pointsleft.append( (vergence[i][1], fixed_y) )
    #     pointsright.append( (vergence[i][1]+vergence_dist[eyeeye], fixed_y) )

    # # # # # # # # # # # # # # # # # # # # # #  PLOT NUMBER 2  # # # # # # # # # # # # # # # # # # # # # # 

    global pointsleft, pointsright
    pointsleft = []
    pointsright = []
    for i in range(90, 100):
        pointsleft.append( (vergence[i][1], vergence[i][2]) )
        pointsright.append( (vergence[i][3], vergence[i][4]) )
    

    # # # # # # # # # # # # # # # # # # # # # #  ANIME  # # # # # # # # # # # # # # # # # # # # # #

    global fig, ax
    fig = plt.figure(dpi=100)
    fig, ax = plt.subplots()

    ani = FuncAnimation(fig, animate, frames=len(pointsleft), interval=20)

   
    f = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/eyesvergence.mp4'
    writervideo = FFMpegWriter() 
    ani.save(f, writer=writervideo)
    




def animate(i):
    ax.clear()
    
    image = folder1 + 'texts/'+ gtext + gtextends + '/Slide' + str(gpageno) + '.PNG'
    img = plt.imread(image)

    ax.imshow(img)

    # Get the point from the points list at index i
    pointleft = pointsleft[i]
    pointright = pointsright[i]

    # Plot left point using the x and y coordinates
    ax.plot(pointleft[0], pointleft[1], color=(69/255, 105/255, 193/255), marker='o', markersize=3)

    # Plot right point using the x and y coordinates
    ax.plot(pointright[0], pointright[1], color=(250/255, 121/255, 12/255), marker='o', markersize=3)

    # Set the x and y axis to display a fixed range
    ax.set_xlim([0, dim[0]])
    ax.set_ylim([0, dim[1]])

    ax.invert_yaxis()
    
    return [ax]