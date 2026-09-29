

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
import time

from semiauto_or_auto_process.commonfunctions import CalculateYline


import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2, pyimagepath, textends, dim
from brighterimages import brighterimages
from Median import Median



def plotpupilsizebypage(sub, text, pageno, subexam, vergenceindex, vergenceleftx, vergencelefty, vergencerightx, vergencerighty, meanpupilsize, startgaze, endgaze, finalindexes):
    global gvergenceleftx, gvergencelefty, gvergencerightx, gvergencerighty, gmeanpupilsize
    gvergenceleftx, gvergencelefty, gvergencerightx, gvergencerighty, gmeanpupilsize = vergenceleftx, vergencelefty, vergencerightx, vergencerighty, meanpupilsize

    global pointsleft, pointsright, radius
    pointsleft = []
    pointsright = []
    radius = []

    # # # # # # If I want shifted y coords  # # # # # #
    yline = CalculateYline(text, pageno)
    for i in range(len(finalindexes)-1):
        start = int( finalindexes[i] )-1
        stop = int( finalindexes[i+1] ) 
        
        tempverglefty = []
        tempvergrighty = []
        for j in range(start,stop):
            tempverglefty.append(vergencelefty[j])
            tempvergrighty.append(vergencerighty[j])

        ymedianleft = Median(tempverglefty, 0)
        ymedianright = Median(tempvergrighty, 0)

        for j in range(start,stop):
            vergencelefty[j] = vergencelefty[j] + (yline[i]-ymedianleft) 
            vergencerighty[j] = vergencerighty[j] + (yline[i]-ymedianright) 

    # # # # # # end of shift y  # # # # # # 

    
    if( len(vergenceleftx) < endgaze ):
            print("\nText %s does not have so many gazes in page %d. Try different range." % (text, pageno))
            time.sleep(3)
            return
    

    # # # # # # keep specific points # # # # # #  
    for i in range(startgaze, endgaze):
        if( vergenceleftx[i]>0 and vergencelefty[i]>0 and vergencerightx[i]>0 and vergencerighty[i]>0 ):
            pointsleft.append( (vergenceleftx[i], vergencelefty[i]) )
            pointsright.append( (vergencerightx[i], vergencerighty[i]) )
            radius.append( meanpupilsize[i] )

    
    # create video
    print("\nCreating pupil size video for sub=%d, text=%s, pageno=%d. Grab some coffee..."  %(sub, text, pageno))

    global img
    path1 = folder1 + 'texts/'+ text + textends + '/Slide' + str(pageno) + '.PNG'
    img = brighterimages(text, pageno, path1)

    global  ax
    fig, ax = plt.subplots()


    ani = FuncAnimation(fig, animate, frames=len(radius), interval=20, repeat=False, blit=False)
    # bar.update(len(radius))
    fig.set_figwidth(12)
    fig.set_figheight(7)

    f = folder1 + folder2 + 'subject_' + str(sub) + '/all_graphs/' + text + str(subexam) + pyimagepath + '/plotpupilsize' + str(pageno) + '.mp4'
    writervideo = FFMpegWriter(fps=30) 
    ani.save(f, writer=writervideo)

    # animepath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/pupilsize' + str(pageno) + '.gif'
    # ani.save(animepath, dpi=300, writer=PillowWriter(fps=20))
    
   



def animate(i):
    print("\rProgress: {0}%".format(int(i/(len(radius)-1)*100)),end="\r")   #  progress message

    ax.clear()

    # image = folder1 + 'texts/'+ gtext + gtextends + '/Slide' + str(gpageno) + '.PNG'
    # img = plt.imread(image)
    ax.imshow(img)
    
    # Get the point from the points list at index i
    pointleft = pointsleft[i]
    pointright = pointsright[i]

    # Plot left point using the x and y coordinates
    ax.plot(pointleft[0], pointleft[1], color=(255/255, 0/255, 127/255), marker='o', markersize=radius[i])   # explanation: pointleft[0]==pointleftx, pointleft[1]==pointlefty

    # Plot right point using the x and y coordinates
    ax.plot(pointright[0], pointright[1], color=(0/255, 0/255, 255/255), marker='o', markersize=radius[i])   # explanation: pointright[0]==pointrightx, pointright[1]==pointrighty

    # Set the x and y axis to display a fixed range
    ax.set_xlim([0, dim[0]])
    ax.set_ylim([0, dim[1]])
    
    # # Turn off tick labels
    # ax.set_yticklabels([])
    # ax.set_xticklabels([])

    plt.axis("off")

    ax.invert_yaxis()
    
    return [ax]