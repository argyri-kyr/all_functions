

import os, sys


from matplotlib.patches import Circle
from matplotlib.patches import RegularPolygon
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter



def plottestattention_fun(fixationx, fixationy, fixationduration):

    global gfixationduration

    gfixationduration = fixationduration

    global fig, ax, plot
    plot = plt
    fig,ax = plt.subplots()
    fig.set_figwidth(19.5)
    fig.set_figheight(15)
    ax.set_xlim(80, 2700)
    figheight = 18
    hy = figheight * 72 / ax.get_ylim()[1]


    # Now, loop through coord arrays, and create a circle at each x,y pair
    global points
    points = []
    for xx,yy in zip(fixationx,fixationy):
        points.append( [xx,yy] )      

    # # # # # # # # # # # # # # # # # # # # # #  ANIME  # # # # # # # # # # # # # # # # # # # # # #
    print("\n\nCreating test attention video")

    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    image = script_directory + '\\mybackground.png'
    img = plt.imread(image)
    ax = plt.subplot(1,1,1) 
    ax.imshow(img)
    plot.axis('off')

    ani = FuncAnimation(fig, animate, frames=len(points)+1, interval=1)
    fig.set_figwidth(19.5)
    fig.set_figheight(15)
    ax.set_xlim(80, 2700)

    
    f = script_directory + '\\attention2.mp4'
    writervideo = FFMpegWriter(fps=3) 
    ani.save(f, writer=writervideo)
    
    #plt.show()





def animate(i):
    print("\rProgress: {0}%".format(int(i/(len(points))*100)),end="\r")   #  progress message
    # ax.clear()
  
    
    if( i == 0 ):
        return

    # ### Colorful choices
    # if( i%8 == 0 ):
    #     colorpicker = "red"
    # if( i%8 == 1 ):
    #     colorpicker = "green"
    # if( i%8 == 2 ):
    #     colorpicker = "blue"
    # if( i%8 == 3 ):
    #     colorpicker = "magenta"
    # if( i%8 == 4 ):
    #     colorpicker = "yellow"
    # if( i%8 == 5 ):
    #     colorpicker = "black"
    # if( i%8 == 6 ):
    #     colorpicker = "orange"
    # if( i%8 == 7 ):
    #     colorpicker = "purple"
        
    ### Colorful choices with spaces
    if( i%8 == 0 ):
        colorpicker = "red"
    if( i%8 == 1 ):
        colorpicker = (160/255,160/255,160/255)
    if( i%8 == 2 ):
        colorpicker = "blue"
    if( i%8 == 3 ):
        colorpicker = (160/255,160/255,160/255)
    if( i%8 == 4 ):
        colorpicker = "yellow"
    if( i%8 == 5 ):
        colorpicker = (160/255,160/255,160/255)
    if( i%8 == 6 ):
        colorpicker = "orange"
    if( i%8 == 7 ):
        colorpicker = (160/255,160/255,160/255) 
        


    # #### Blue choices (normal)
    # if( i%8 == 1 ):
    #     colorpicker = (31/255,119/255,180/255)
    # if( i%8 == 2 ):
    #     colorpicker = (160/255,160/255,160/255)
    # if( i%8 == 3 ):
    #     colorpicker = (31/255,119/255,180/255)
    # if( i%8 == 4 ):
    #     colorpicker = (160/255,160/255,160/255)
    # if( i%8 == 5 ):
    #     colorpicker = (31/255,119/255,180/255)
    # if( i%8 == 6 ):
    #     colorpicker = (160/255,160/255,160/255)
    # if( i%8 == 7 ):
    #     colorpicker = (31/255,119/255,180/255)
    # if( i%8 == 0 ):
    #     colorpicker = (160/255,160/255,160/255)
        
        
    
    # Select geometrical shapes
    if( i%3==0 ):
        circ = RegularPolygon((points[i-1][0],points[i-1][1]), numVertices=6, radius=gfixationduration[i-1]/15, color=colorpicker)
        ax.add_patch(circ)

    
    if( i%3==1 ):
        circ = Circle((points[i-1][0],points[i-1][1]), gfixationduration[i-1]/15, color=colorpicker)
        ax.add_patch(circ)

        
    if( i%3==2 ):
        circ = RegularPolygon((points[i-1][0],points[i-1][1]), numVertices=4, radius=gfixationduration[i-1]/15, color=colorpicker)
        ax.add_patch(circ)
    
        

    # if( i>1 ):
    #     tempx = [ points[i-2][0], points[i-1][0] ]
    #     tempy = [ points[i-2][1], points[i-1][1] ]
    #     plot.plot(tempx, tempy, color=(250/255,121/255,12/255), linewidth=1.5)
    
    # if( i<1 ):
    #     tempx = [ points[i+1][0], points[i][0] ]
    #     tempy = [ points[i+1][1], points[i][1] ]
    #     plot.plot(tempx, tempy, color=(250/255, 121/255, 12/255), linewidth=1.5)

    


