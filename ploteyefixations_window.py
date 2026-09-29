

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
import matplotlib.patches as patches


from globalVars import folder1, folder2, textends, pyimagepath


def ploteyefixations_window(sub, text, pageno, exam, fixationx, fixationy, fixationduration):

    global gsub, gtext, gpageno, gfixationduration
    gsub = sub
    gtext = text
    gpageno = pageno
    gfixationduration = fixationduration

    global fig, ax, plot
    plot = plt
    fig,ax = plt.subplots()
    fig.set_figwidth(12)
    fig.set_figheight(7)


    # Now, loop through coord arrays, and create a circle at each x,y pair
    global points
    points = []
    for xx,yy in zip(fixationx,fixationy):
        points.append( [xx,yy] )      

    # # # # # # # # # # # # # # # # # # # # # #  ANIME  # # # # # # # # # # # # # # # # # # # # # #
    print("\n\nCreating window fixations video for sub=%d, text=%s, pageno=%d. Grab some coffee..."  %(sub, text, pageno))
    
   
    global img
    image = folder1 + 'texts/'+ gtext + textends + '/Slide' + str(gpageno) + '.PNG'
    img = plt.imread(image)
    ax = plt.subplot(1,1,1) 
    ax.imshow(img)
    plot.axis('off')

    ani = FuncAnimation(fig, animate, frames=len(points), interval=1)
    
    fig.set_figwidth(12)
    fig.set_figheight(7)
    
    f = folder1 + folder2 + 'subject_' + str(sub) + '/all_graphs/' + text + str(exam) + pyimagepath + '/ploteyefixations_window' + str(pageno) + '.mp4'
    writervideo = FFMpegWriter(fps=30) 
    ani.save(f, writer=writervideo)
    
    #plt.show()




def animate(i):
    print("\rProgress: {0}%".format(int(i/(len(points)-1)*100)),end="\r")   #  progress message
    
    ax.clear()
    ax.imshow(img)
    ax.axis('off')
    
    # if( i == 0 ):
    #     return

    center_xo = points[i][0]
    center_yo = points[i][1]
    
    width =  160  # gfixationduration[i]/2 
    height = 70
    
    # Calculate the lower-left corner
    x_lower_left = center_xo - width / 2
    y_lower_left = center_yo - height / 2

    # Create a rectangle
    rectangle = patches.Rectangle((x_lower_left, y_lower_left), width, height, linewidth=3, edgecolor='darkorange', facecolor='none')
    ax.add_patch(rectangle)
        
    # ax.text(points[i][0], points[i][1], str(i), fontsize=8)
    
    
