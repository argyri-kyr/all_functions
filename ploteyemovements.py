


from asyncio.windows_events import NULL
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter


from globalVars import folder1, folder2, textends, dim, pyimagepath



#Συναρτηση που φτιαχνει τις fixations(page_nymber).png
#Το drawradius παιρνει τιμες={"yes","no"} 
#Eαν drawradius=="yes" τοτε θελω να φτιαξω τις fixations.png images
#Eαν drawradius=="no" τοτε θελω να φτιαξω τις cutgazes.png images
def plotEyeMovements(sub1, exam, text, pageno, fixationx, fixationy):
    global x, y, gtext, gpageno
    x = fixationx
    y = fixationy
    gtext = text
    gpageno = pageno
   

    # Now, loop through coord arrays, and create a circle at each x,y pair
    global points
    points = []
    for xx,yy in zip(x,y):
        points.append( [xx,yy] )  
        
    print("\n\nCreating eyemovements video for sub=%d, text=%s, pageno=%d. Grab some coffee..."  %(sub1, text, pageno))

    global f, ax, plot
    plot = plt
    f = plt.figure(dpi=100) 
    f.set_size_inches(dim[0]/100, dim[1]/100)
    
    
    image = folder1 + 'texts/'+ text + textends + '/Slide' + str(pageno) + '.PNG'
    img = plt.imread(image)
    ax = plt.subplot(1,1,1) 
    ax.imshow(img) 
    plot.axis('off')
    plot.xlim([0, dim[0]])
    plot.ylim([dim[1], 0])
    
    
    ani = FuncAnimation(f, animate, frames=len(points), interval=1)

    file = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/ploteyemovements_' + str(pageno) + '.mp4'
    writervideo = FFMpegWriter(fps=30) 
    ani.save(file, writer=writervideo)
    
    
    
def animate(i):
    print("\rProgress: {0}%".format(int(i/(len(points)-1)*100)),end="\r")   #  progress message
    
    # #############################
    # if( i%6 == 0 and i!=0 ):
    #     ax.clear()
        
    #     image = folder1 + 'texts/'+ gtext + textends + '/Slide' + str(gpageno) + '.PNG'
    #     img = plt.imread(image)
    #     plt.subplot(1,1,1) 
    #     ax.imshow(img)
        
    #     plot.xlim([0, dim[0]])
    #     plot.ylim([dim[1], 0])        
            
    #     plot.axis('off')
    # ############################
    
    if( i == 0 ):
        return

        
    if( points[i-1][0] < points[i][0] ):
        draw_curve(points[i-1], points[i], plot, 1)
        
    elif( abs(points[i][0]-points[i-1][0])>=600 and  abs(points[i][1]-points[i-1][1])>=70 ):
        draw_curve(points[i-1], points[i], plot, 3)
    
    else:
        draw_curve(points[i-1], points[i], plot, 2)
           
           
    # plot.plot(x, y, color=(250/255,121/255,12/255) , linewidth=1) 



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
    
    func = np.poly1d(np.polyfit((p1[0], p2[0], p3[0]), (p1[1], p2[1], p3[1]), 2))
    x = np.linspace(p1[0], p2[0], 100)
    y = func(x)

    if( flag == 1 ):
        plot.plot(x, y, color=(250/255, 121/255, 12/255) , linewidth=2.5)

    elif( flag == 2 ):
        plot.plot(x, y, color=(101/255, 170/255, 215/255), linewidth=2.5)       # green line

    elif( flag == 3 ):
        plot.plot(x, y, color=(245/255, 69/255, 42/255), linewidth=2.5)         # blue line

