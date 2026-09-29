

from matplotlib.patches import Circle
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter


from globalVars import folder1, folder2, textends, dim, pyimagepath


def ploteyefixations(sub, text, pageno, exam, fixationx, fixationy, fixationduration):

    global gsub, gtext, gpageno, gfixationduration
    gsub = sub
    gtext = text
    gpageno = pageno
    gfixationduration = fixationduration

    global fig, ax, plot
    plot = plt
    fig,ax = plt.subplots()
    fig.set_size_inches(dim[0]/100, dim[1]/100)


    # Now, loop through coord arrays, and create a circle at each x,y pair
    global points
    points = []
    for xx,yy in zip(fixationx,fixationy):
        points.append( [xx,yy] )      

    # # # # # # # # # # # # # # # # # # # # # #  ANIME  # # # # # # # # # # # # # # # # # # # # # #
    print("\n\nCreating fixations video for sub=%d, text=%s, pageno=%d. Grab some coffee..."  %(sub, text, pageno))
   

    image = folder1 + 'texts/'+ gtext + textends + '/Slide' + str(gpageno) + '.PNG'
    img = plt.imread(image)
    ax = plt.subplot(1,1,1) 
    ax.imshow(img)
    plot.axis('off')
    plot.xlim([0, dim[0]])
    plot.ylim([dim[1], 0])
    
    ani = FuncAnimation(fig, animate, frames=len(points), interval=1)
    
    
    f = folder1 + folder2 + 'subject_' + str(sub) + '/all_graphs/' + text + str(exam) + pyimagepath + '/ploteyefixations_' + str(pageno) + '.mp4'
    writervideo = FFMpegWriter(fps=30) 
    ani.save(f, writer=writervideo)
    
    #plt.show()





def animate(i):
    print("\rProgress: {0}%".format(int(i/(len(points)-1)*100)),end="\r")   #  progress message
    # ax.clear()
  
    
    # if( i == 0 ):
    #     return


    if( gfixationduration[i] <= 1000 ):
        circ = Circle((points[i][0],points[i][1]), gfixationduration[i]/15)
        ax.add_patch(circ)
        # ax.text(points[i][0], points[i][1], str(i), fontsize=8)
        

    elif( gfixationduration[i] > 1000 ):
        circ = Circle((points[i][0],points[i][1]), gfixationduration[i]/15, color=(31/255,119/255,180/255), fill=False)
        ax.add_patch(circ)
        # ax.text(points[i][0], points[i][1], str(i), fontsize=8)
       

    # else:
    #     circ = Circle((points[i][0],points[i][1]), 15)
    #     ax.add_patch(circ)
        # ax.text(points[i][0], points[i][1], str(i), fontsize=8)
        

    if( i>0 ):
        tempx = [ points[i-1][0], points[i][0] ]
        tempy = [ points[i-1][1], points[i][1] ]
        plot.plot(tempx, tempy, color=(250/255,121/255,12/255), linewidth=1.5)
    
    # if( i<1 ):
    #     tempx = [ points[i+1][0], points[i][0] ]
    #     tempy = [ points[i+1][1], points[i][1] ]
    #     plot.plot(tempx, tempy, color=(250/255, 121/255, 12/255), linewidth=1.5)

    


