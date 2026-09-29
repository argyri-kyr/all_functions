

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
import matplotlib.patches as patches


from globalVars import folder1, folder2, textends, pyimagepath


def ploteyecutgazes_window(sub, text, pageno, exam, cutgazesx, cutgazesy):

    global gsub, gtext, gpageno
    gsub = sub
    gtext = text
    gpageno = pageno
    

    global fig, ax, plot
    plot = plt
    fig,ax = plt.subplots()
    fig.set_figwidth(12)
    fig.set_figheight(7)


    # Now, loop through coord arrays, and create a circle at each x,y pair
    global points
    points = []
    for xx,yy in zip(cutgazesx,cutgazesy):
        points.append( [xx,yy] )      

    # # # # # # # # # # # # # # # # # # # # # #  ANIME  # # # # # # # # # # # # # # # # # # # # # #
    print("\n\nCreating window cutgazes video for sub=%d, text=%s, pageno=%d. Grab some coffee..."  %(sub, text, pageno))
    
   
    global img
    image = folder1 + 'texts/'+ gtext + textends + '/Slide' + str(gpageno) + '.PNG'
    img = plt.imread(image)
    ax = plt.subplot(1,1,1) 
    ax.imshow(img)
    plot.axis('off')

    ani = FuncAnimation(fig, animate, frames=len(points), interval=1)
    
    fig.set_figwidth(12)
    fig.set_figheight(7)
    
    f = folder1 + folder2 + 'subject_' + str(sub) + '/all_graphs/' + text + str(exam) + pyimagepath + '/ploteyecutgazes_window' + str(pageno) + '.mp4'
    writervideo = FFMpegWriter(fps=90) 
    ani.save(f, writer=writervideo)
    
    #plt.show()




def animate(i):
    print("\rProgress: {0}%".format(int(i/(len(points))*100)),end="\r")   #  progress message
    
    ax.clear()
    ax.imshow(img)
    ax.axis('off')
    
    # if( i == 0 ):
    #     return

    center_xo = points[i][0]
    center_yo = points[i][1]
    
    if( center_xo==None and center_yo==None ):
        ax.plot([center_xo])
        return
    
    width =  160  # gcutgazesduration[i-1]/2 
    height = 70
    
    # Calculate the lower-left corner
    x_lower_left = center_xo - width / 2
    y_lower_left = center_yo - height / 2

    # Create a rectangle
    rectangle = patches.Rectangle((x_lower_left, y_lower_left), width, height, linewidth=1, edgecolor='darkorange', facecolor='none')
    ax.add_patch(rectangle)
        
    # ax.text(points[i-1][0], points[i-1][1], str(i), fontsize=8)
    
    
