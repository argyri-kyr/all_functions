from asyncio.windows_events import NULL
from matplotlib.patches import Circle
from matplotlib import pyplot as plt

from globalVars import folder1, folder2, textends, dim, pyimagepath
from fixationsCropped import fixationsCropped

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
def drawFixations(sub1, exam, text, fixationdata, pageno, drawradius, plot):
    x = takeCoordData(fixationdata)[0]
    y = takeCoordData(fixationdata)[1]
    duration = takeCoordData(fixationdata)[2]

    # Create a figure. Equal aspect so circles look circular
    if(plot==NULL):
        f = plt.figure(dpi=100) 
        f.set_size_inches(dim[0]/100, dim[1]/100)
        plot=plt


    ax = plt.subplot(1,1,1) 
    plot.axis('off')
    
    image = folder1 + 'texts/'+ text + textends + '/Slide' + str(pageno) + '.PNG'
    img = plt.imread(image)
    ax.imshow(img)
    

    radius= []
    for i in range(len(duration)):
        radius.append( duration[i]/15 )

    # Now, loop through coord arrays, and create a circle at each x,y pair
    i=0
    for xx,yy in zip(x,y):
        if(duration[i]<=1000 and drawradius=="yes"):
            circ = Circle((xx,yy),radius[i])
            ax.add_patch(circ)  
        elif(duration[i]>1000 and drawradius=="yes"):
            circ = Circle( (xx,yy), radius[i], color=(31/255,119/255,180/255), fill=False)
            ax.add_patch(circ)      
        elif(drawradius=="no"):
            circ = Circle((xx,yy),radius=15,color='red',fill=False)
            ax.add_patch(circ)     
        
            
        i+=1

        
    if(drawradius=="yes"):
        plot.plot(x, y, color=(250/255,121/255,12/255), linewidth=2.5)
        
        # subject's id signature (top right corner)
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
        
        plot.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/fixations' + str(pageno) + '.png', dpi=100)
        fixationsCropped(sub1, exam, text, pageno)
        
    elif(drawradius=="no"):
        plot.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/cutgazes' + str(pageno) + '.png', dpi=100)

  
    
    plot.close()

    #plt.show()
