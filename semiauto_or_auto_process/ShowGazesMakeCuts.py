from matplotlib import pyplot as plt
from PIL import Image
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.artist import Artist

import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2, pyimagepath
from findPages import findPages
from movefigure import movefigure



#Sinarthsh opou mou epistrefei to frame sto opoio kanw ta kopsimata kai apothikeuei afth thn eikona(linesteps.png)
def ShowGazesMakeCuts(sub1, exam, text, pageno, lines, tempx, tempy, xo, yo, average, flag, secondRun, from_runcrashes):
    global tsub1, texam, ttext, tpageno, ttempx, ttempy, lengthx
    tsub1 = sub1
    texam = exam
    ttext = text
    tpageno = pageno
    ttempx = tempx
    ttempy = tempy
    lengthx = len(tempx)  # this var defines how big the area will be for the remove click. len(tempx) is the number of gazes per page. We choose to use 0.007 (0.7%) on them on remove click 

    
    global plines      #i made this global in order to use them some code below { (indexes : list with Index coords that have occur from my cut), (plines : page lines) }
    plines = lines

    #Draw gazes
    global f, ax
    f, (ax, ax1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [5, 1]})
    f.set_figwidth(14)
    f.set_figheight(9)     # f.set_figheight(8)
    plt.subplots_adjust(hspace = 0.2)   # plt.subplots_adjust(hspace = 0.5)
    
    ax.margins(x=0)
    ax.plot(tempx,'yellow')
    ax.plot(tempy,'blue')


    pages = findPages(text)


    ax.set_title( "Subject: "+ str(sub1) + ", Text: " + text + ", Page: " + str(pageno) + " out of " + str(pages) + ", Lines: " + str(lines) + ',  Second_Run: ' + str(secondRun) )

    
    #Draw Cuts(red circles) and Average(red line)
    global x
    global y
    global line
    
    ax.plot(average,'red')
    
    x = xo
    y = yo
    
    line, = ax.plot(xo, yo, ls="None", linewidth=0, marker="o", color=(0, 230/255, 0), markersize=10, markerfacecolor='none', markeredgewidth=2)
    
    
    #Make pointsleftframe
    global pointsleftframe
    pointsleft = lines+1 - len(x)
    y0, ymax = ax.set_ylim()
    myheight = ymax - ( ymax - max(max(tempx), max(tempy), max(average)) )/3
    mywidth = max(len(tempx),len(tempy)) - 0.12*max(len(tempx),len(tempy))
    pointsleftframe = ax.text(mywidth, myheight, "points left = " + str(pointsleft), size=12, color = 'black', weight = 'bold', ha="left", va="top")
    Artist.set_visible(pointsleftframe, True)

    
    if(flag == 0):
        ax1.axis('off')

        if(secondRun):
            extent = ax.get_window_extent().transformed(f.dpi_scale_trans.inverted())
            f.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/linesteps' + str(pageno) + '.png', bbox_inches=extent.expanded(1.3, 1.55))
            # change_Image_dim(folder1 + folder2 + 'subject_' + str(tsub1) + '/all_graphs/' + ttext + str(texam) + pyimagepath + '/linesteps' + str(tpageno) + '.png', 1366, 768)
        
        if(from_runcrashes==True):
            f.canvas.mpl_connect('button_press_event' , remove_point)
            f.canvas.mpl_connect('key_press_event' , close_figure_enter)

            ax1.text(0.35, -0.4,"Add a point with Left Click\n\nRemove a point with Right Click\n\nPress 'Enter' when done", fontsize = 15, color='red', style='italic')
            movefigure(f, 3, 10)

            plt.show()
        
        
        return x, y
    
    
    if(flag == 1):
        ax1.axis('off')
        extent = ax.get_window_extent().transformed(f.dpi_scale_trans.inverted())
        f.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath +'/linesteps' + str(pageno) + '.png', bbox_inches=extent.expanded(1.3, 1.55))
        # change_Image_dim(folder1 + folder2 + 'subject_' + str(tsub1) + '/all_graphs/' + ttext + str(texam) + pyimagepath + '/linesteps' + str(tpageno) + '.png', 1366, 768)
        # plt.show()
        return x



#Sinarthsh(mouse event) gia afairesh h prosthiki kapoiou cut(kiklaki)
def remove_point(event):
    removed = False
    
    for i in range(len(x)):
        if( abs(event.xdata-x[i]) <= 0.007*lengthx and event.button == 3 ):
            removed = True

            del x[i]
            xvals = x[:]
            line.set_xdata(xvals)

                
            del y[i]
            yvals = y[:]
            line.set_ydata(yvals)

            line.set_data(xvals,yvals)
        
            f.canvas.draw_idle()
            break

    if( removed == False and event.button == 1 ):
        if( len(x) < plines+1 ):            
            x.append(int(event.xdata))
            xvals = x[:]
            line.set_xdata(xvals)

            y.append(int(event.ydata))
            yvals = y[:]
            line.set_xdata(yvals)

            line.set_data(xvals,yvals)

            f.canvas.draw_idle()
        else:
            print("You have already (lines+1) = %d points" %(plines+1))

    
    
    pointsleft = plines+1 - len(x)
    pointsleftframe.set_text("points left = " + str(pointsleft))

    extent = ax.get_window_extent().transformed(f.dpi_scale_trans.inverted())
    f.savefig(folder1 + folder2 + 'subject_' + str(tsub1) + '/all_graphs/' + ttext + str(texam) + pyimagepath + '/linesteps' + str(tpageno) + '.png', bbox_inches=extent.expanded(1.3, 1.55))
    # change_Image_dim(folder1 + folder2 + 'subject_' + str(tsub1) + '/all_graphs/' + ttext + str(texam) + pyimagepath + '/linesteps' + str(tpageno) + '.png', 1366, 768)
    


def close_figure_enter(event):
    if( event.key == 'enter' ):
        plt.close(event.canvas.figure)
        plt.close('all')


def on_close(event):
    plt.close('all')
    


def change_Image_dim(path, dimX, dimY):
    image = Image.open(path)
    image = image.resize((dimX,dimY),Image.ANTIALIAS)
    image.save(fp=path)