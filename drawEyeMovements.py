from asyncio.windows_events import NULL
from matplotlib.patches import Circle
from matplotlib import pyplot as plt
import numpy as np


from globalVars import folder1, folder2, textends, dim, pyimagepath

#Συναρτηση οπου παιρνει ως ορισμα το fixationdata που ειναι μια λιστα με ολες τις πληροφοριες των fixation και απο αυτες αποθηκευει σε λιστες το Χ, το Υ και το duration αυτων
def takeCoordData(fixationdata):
    fixX = []        #fixation's x coordinate
    fixY = []        #fixation's y coordinate
    duration = []    #fixation's duration
        
    for i in range(len(fixationdata)):
        fixX.append( fixationdata[i][0] )
        fixY.append( fixationdata[i][1] )
        duration.append( fixationdata[i][6] )
    
    return fixX, fixY, duration


#Συναρτηση που φτιαχνει τις fixations(page_nymber).png
#Το drawradius παιρνει τιμες={"yes","no"} 
#Eαν drawradius=="yes" τοτε θελω να φτιαξω τις fixations.png images
#Eαν drawradius=="no" τοτε θελω να φτιαξω τις cutgazes.png images
def drawEyeMovements(sub1, exam, text, fixationdata, pageno, plot):
    x = takeCoordData(fixationdata)[0]
    y = takeCoordData(fixationdata)[1]
    duration = takeCoordData(fixationdata)[2]

    # Create a figure. Equal aspect so circles look circular
    if(plot==NULL):
        f = plt.figure(dpi=100) 
        f.set_size_inches(dim[0]/100, dim[1]/100)
        plot=plt

    
    image = folder1 + 'texts/'+ text + textends + '/Slide' + str(pageno) + '.PNG'
    img = plt.imread(image)
    ax = plt.subplot(1,1,1) 
    ax.imshow(img)
        
    plot.axis('off')

    # Now, loop through coord arrays, and create a circle at each x,y pair
    i=0
    points = []
    for xx,yy in zip(x,y):
        points.append( [xx,yy] )
        circ = Circle( (xx,yy), radius=5, color=(165/255, 219/255, 229/255), fill=True)   # facecolor=(0/255, 255/255, 0/255), edgecolor='black'
        ax.add_patch(circ)       
        i+=1

        
  
    for i in range(1, len(points)):
        if( points[i-1][0] < points[i][0] ):
            draw_curve(points[i-1], points[i], plot, 1)
        elif( abs(points[i][0]-points[i-1][0])>=600 and  abs(points[i][1]-points[i-1][1])>=70 ):
            draw_curve(points[i-1], points[i], plot, 3)
        else:
            draw_curve(points[i-1], points[i], plot, 2)
           
    # plot.plot(x, y, color=(250/255,121/255,12/255) , linewidth=1) 
    left, width = .25, .8
    bottom, height = .0, 0.9
    right = left + width 
    top = bottom + height

    ax.text(right, top, str(sub1),
    color = '#cfcfd1',
    fontsize=12,
    horizontalalignment='right',
    verticalalignment='top',
    transform=ax.transAxes)

    plt.xlim([0, dim[0]])
    plt.ylim([dim[1], 0])
        
    plot.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/eye_movements' + str(pageno) + '.png', dpi=100)
    
    plot.close()

    #plt.show()


def draw_curve(p1, p2, plot, flag):
    startx = min(p1[0], p2[0])
    endx = max(p1[0], p2[0])
    starty = min(p1[1], p2[1])
    endy = max(p1[1], p2[1])

    if( flag == 1 ):
        p3 = [ startx+((endx-startx)/2), starty+((endy-starty)/2) - (0.20*(endx-startx)) ]

    elif( flag == 2 ):
        if( endx-startx >= 500 ):
            p3 = [ startx+((endx-startx)/2), starty+((endy-starty)/2) + (0.08*(endx-startx)) ]
        else:
            p3 = [ startx+((endx-startx)/2), starty+((endy-starty)/2) + (0.30*(endx-startx)) ]
    
    elif( flag == 3 ):
        p3 = [ startx+((endx-startx)/2), starty+((endy-starty)/2) + (0.02*(endx-startx)) ]
    
    f = np.poly1d(np.polyfit((p1[0], p2[0], p3[0]), (p1[1], p2[1], p3[1]), 2))
    x = np.linspace(p1[0], p2[0], 100)
    y = f(x)

    if( flag == 1 ):
        plot.plot(x, y, color=(250/255, 121/255, 12/255) , linewidth=2.5)

    elif( flag == 2 ):
        plot.plot(x, y, color=(101/255, 170/255, 215/255), linewidth=2.5)       # green line

    elif( flag == 3 ):
        plot.plot(x, y, color=(245/255, 69/255, 42/255), linewidth=2.5)         # blue line

