

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
import time




import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2, pyimagepath, dim, textends
from brighterimages import brighterimages
from Median import Median
from semiauto_or_auto_process.commonfunctions import CalculateYline


def ploteyevergencebypage_ofth(sub1, text, pageno, exam, vergenceindex, vergenceleftx, vergencelefty, vergenceleftvalid, vergencerightx, vergencerighty, vergencerightvalid, vergencetimestamp, startgaze, endgaze, finalindexes):
    global gtext, gtextends, gpageno
    gtext , gtextends, gpageno = text, textends, pageno

    global pointsleft, pointsright, pointsleft_loss, pointsright_loss, pointsvalidity
    pointsleft = []
    pointsright = []
    pointsleft_loss = []
    pointsright_loss = []
    pointsvalidity = []

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
    

    # # # # # # # delete non valid vergence gazes # # # # # # # # # # # #
    # for i in range(startgaze, endgaze):    # an to pame apo "startgaze" ews "endgaze" tote petaw gazes stin arxi kai sto telos (apo kopsimo sta skalopatia)
    #     if( vergenceleftx[i]>0 and vergencelefty[i]>0 and vergencerightx[i]>0 and vergencerighty[i]>0 ):
    #         pointsleft.append( (vergenceleftx[i], vergencelefty[i]) )
    #         pointsright.append( (vergencerightx[i], vergencerighty[i]) )
    #     else:
    #         pointsleft.append( (-30, -30) )       # afto to kaname wste na iparxei o xronos tou gaze alla na mh fenete pouthena sto video
    #         pointsright.append( (-30, -30) )      # afto to kaname wste na iparxei o xronos tou gaze alla na mh fenete pouthena sto video
    # # # # # # # end of shift delete  # # # # # # # # # # # # # # # #


    for i in range(len(vergenceleftx)):  # an to pame se olh th lista twn gazes tote den petaw kanena gaze(tha exw pio megala video, me skoupidia)
        if( vergenceleftvalid[i]==1 and vergencerightvalid[i]==1 ):
            pointsleft.append( (vergenceleftx[i], vergencelefty[i]) )
            pointsright.append( (vergencerightx[i], vergencerighty[i]) )
            pointsvalidity.append( (vergenceleftvalid[i], vergencerightvalid[i]) )
            
        elif( (vergenceleftvalid[i]==1 and vergencerightvalid[i]==0) or (vergenceleftvalid[i]==0 and vergencerightvalid[i]==1) ):
            if(  (i-1>=0 and (vergenceleftvalid[i-1]!=0 or vergencerightvalid[i-1]!=0)) and (i+1<len(vergenceleftx) and (vergenceleftvalid[i+1]!=0 or vergencerightvalid[i+1]!=0)) ):
                pointsleft.append( (vergenceleftx[i], vergencelefty[i]) )
                pointsright.append( (vergencerightx[i], vergencerighty[i]) )
                pointsleft_loss.append( (vergenceleftx[i], vergencelefty[i]) )
                pointsright_loss.append( (vergencerightx[i], vergencerighty[i]) )
                pointsvalidity.append( (vergenceleftvalid[i], vergencerightvalid[i]) )
            
        else:
            pointsleft.append( (-30, -30) )       # afto to kaname wste na iparxei o xronos tou gaze alla na mh fenete pouthena sto video
            pointsright.append( (-30, -30) )      # afto to kaname wste na iparxei o xronos tou gaze alla na mh fenete pouthena sto video
            pointsvalidity.append( (0, 0) )


    # # # # # # # # # # # # # # # # # # # # # #  ANIME  # # # # # # # # # # # # # # # # # # # # # #
    print("\nCreating eye vergence video for sub=%d, text=%s, pageno=%d. Grab some coffee..."  %(sub1, text, pageno))

    global img
    path1 = folder1 + 'texts/'+ gtext + gtextends + '/Slide' + str(gpageno) + '.PNG'
    img = brighterimages(text, pageno, path1)

    global  ax
    fig, ax = plt.subplots()

    ani = FuncAnimation(fig, animate, frames=len(pointsleft), interval=20, repeat=False, blit=False)
    fig.set_figwidth(12)
    fig.set_figheight(7)

    f = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/eyesvergence' + str(pageno) + '.mp4'
    writervideo = FFMpegWriter(fps=89) 
    ani.save(f, writer=writervideo)

    # animepath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/eyesvergence' + str(pageno) + '.gif'
    # ani.save(animepath, dpi=300, writer=PillowWriter(fps=20))
    
   



def animate(i):
    print("\rProgress: {0}%".format(int(i/(len(pointsleft)-1)*100)),end="\r")   #  progressbar message

    ax.clear()
    ax.imshow(img)
    
    # Get the point from the points list at index i
    pointleft = pointsleft[i]
    pointright = pointsright[i]

    if( (pointleft in pointsleft_loss) and (pointright in pointsright_loss) ):
        if( pointsvalidity[i][0]==1 and pointsvalidity[i][1]==0 ):
            ax.plot(pointleft[0], pointleft[1], color='darkorange', marker='s', markersize=8)   
            # ax.plot(pointright[0], pointright[1], color='green', marker='s', markersize=9)   
            # plt.annotate('Track Loss Detected in index i =  '+ str(i), xy = (2.4, 8), fontsize = 14, xytext = ( dim[0]/3, 40 ), arrowprops = dict(facecolor = 'red'), color = 'g')
            plt.annotate('Track Loss Detected in index i =  '+ str(i), xy = (2.4, 8), fontsize = 14, xytext = ( dim[0]/3, 40 ), color = 'g')
            print( 'Track Loss Detected' )
            
        if( pointsvalidity[i][0]==0 and pointsvalidity[i][1]==1 ):
            ax.plot(pointright[0], pointright[1], color='darkorange', marker='^', markersize=8)   
            # ax.plot(pointleft[0], pointleft[1], color='darkorange', marker='^', markersize=9)   
            # plt.annotate('Track Loss Detected in index i =  '+ str(i), xy = (1, 7), fontsize = 14, xytext = ( dim[0]/3, 40 ), arrowprops = dict(facecolor='red',shrink=0.05), color = 'g')
            plt.annotate('Track Loss Detected in index i =  '+ str(i), xy = (2.4, 8), fontsize = 14, xytext = ( dim[0]/3, 40 ), color = 'g')
            print( 'Track Loss Detected' )
    
    else:
        ax.plot(pointleft[0], pointleft[1], color=(255/255, 0/255, 127/255), marker='o', markersize=5)
        ax.plot(pointright[0], pointright[1], color=(0/255, 0/255, 255/255), marker='o', markersize=5)


    ax.set_xlim([0, dim[0]])
    ax.set_ylim([0, dim[1]])
    
    plt.title("Gazeno = " + str(i), y=-0.001)
    plt.axis("off")

    ax.invert_yaxis()
    
    return [ax]
   


