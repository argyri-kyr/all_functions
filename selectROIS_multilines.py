

from asyncio.windows_events import NULL
import copy
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.widgets import RadioButtons


from globalVars import folder1, folder2, textends
from GetAndDrawROIS import getROIbounds
from findroisposition import findroisposition
from movefigure import movefigure



def selectROIS(sub1, exam, text, pageno, file, roibounds, tempx, tempy, cgx, cgy):
    global gtext
    gtext = text

    plt.close("all")

    # if(text in ['visitloud','midfredloud'] ):
    #     # # i.e # loud = 'C:/_Iro_analysis_tobii7_HD/individual/subject_13110/de_13110_1_visitloud_wa_4_4_2023-03-28-09.58.11/AudioRecording.wav'
    #     loud = folder1 + folder2 + 'subject_' + str(sub1) + "/" + file + "/AudioRecording.wav"
    #     os.system(loud)
    

    global lengthx, lengthy, x, y, xo, yo, f, ax, tsub1, texam, ttext, tpageno, troibounds, tcgx, tcgy, line, ax_check, labels, activated, plot_button
    lengthx = len(cgx)
    lengthy = len(cgy)
    tsub1 = sub1
    texam = exam
    ttext = text
    tpageno = pageno
    troibounds = roibounds
    tcgx = cgx
    tcgy = cgy
    x = []
    y = []
    xo = []
    yo = []

    global prois, xroi, yroi, widthroi, heightroi     #i made this global in order to use them some code below { (indexes : list with Index coords that have occur from my cut), (plines : page lines) }
    xroi, yroi, widthroi, heightroi = getROIbounds(text, pageno)
    prois = len(xroi)

    f=plt.figure()
    ax = plt.subplot(1,1,1)
    f.set_size_inches(9, 6)

    movefigure(f, 500, 80)   

    plt.title("Diselect the ROIS that are almost empty\nPress X when done")
    plt.plot(tempx, tempy, 'x', color='#6685E9', markeredgewidth=0.5)
    plt.plot(cgx, cgy, 'x', color='#E96F66', markeredgewidth=0.5)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis('off')
    

    image = folder1 + 'texts/' + text + textends + '/Slide' + str(pageno) + '.PNG'
    img = plt.imread(image)
    ax.imshow(img)
    
    plt.axis('off')

    x, y, xo, yo, line = drawSelectedROIS(sub1, exam, text, pageno, roibounds, tempx, tempy, cgx, cgy)

    
    ax_check = plt.axes([0.8, 0.05, 0.15, 0.15])
    labels = ['Check All', 'Uncheck All']
    activated = [0, 0]
    plot_button = RadioButtons(ax_check, labels, activated)
    plot_button.on_clicked(select_diselect_allrois)

    plt.gcf().canvas.mpl_connect('key_press_event', close_figure_enter)

    plt.show()


    position = findroisposition(text, pageno)

    finalROIS = []
    for j in range(len(x)):
        position = findroisposition(text, pageno)
        for k in range(len(xroi)):
            if( (xroi[k]<= x[j] <xroi[k]+widthroi[k]) and  (yroi[k]<= y[j] <yroi[k]+heightroi[k])):
                finalROIS.append(position+1)
                break
            else:
                position += 1

    finalROIS.sort()

    # delete double selected ROIS
    finalROIS = list(dict.fromkeys(finalROIS))

    print("ROIS_selected = ", finalROIS)

    return finalROIS



def zoomimage(text, pageno):
    global lines, data
    data = pd.read_excel(folder1 + 'texts/' + text + textends + '/py/ROIbounds/mytext.page_' + str(pageno) + '.ROIbounds.xlsx')

    first_y = data.iloc[0, 1] - 5
    last_y = data.iloc[-1, 1] + data.iloc[-1, 3] + 5
    plt.ylim(last_y, first_y)


def drawSelectedROIS(sub1, exam, text, pageno, roibounds, tempx, tempy, cgx, cgy):

    #I WILL MAKE/DRAW THE ROI BOUNDS
    x = roibounds[0]
    y = roibounds[1]
    width = roibounds[2]
    height = roibounds[3]


    for i in range(len(x)):
        rect = matplotlib.patches.Rectangle((x[i],y[i]),
                                        width[i], height[i],
                                        color ='#79D0EB',
                                        fill=False)


        ax.add_patch(rect)

        xo.append( x[i]+ width[i]/2 )
        yo.append( y[i]+ height[i]/2 )


    x = copy.deepcopy(xo)
    y = copy.deepcopy(yo)
    

    line, = ax.plot(xo, yo, ls="None", linewidth=0, marker="o", color='lime', markersize=12, markerfacecolor='none', markeredgewidth=3)

    f.canvas.mpl_connect('button_press_event' , remove_point)

    zoomimage(text, pageno)

    return x, y, xo, yo, line



# function for displaying/hiding the plots
def select_diselect_allrois(label):
    
    # get the index that correspon]ds to the word "label"
    index = labels.index(label)
    if( index == 1 ):
        global x, y
        sizex = len(x)
        while( sizex > 0 ):
            del x[-1]
            xvals = x[:]
            line.set_xdata(xvals)

                
            del y[-1]
            yvals = y[:]
            line.set_ydata(yvals)

            line.set_data(xvals,yvals)
        
            f.canvas.draw_idle()

            sizex = len(x)

    if( index == 0 ):
        line.set_xdata(xo)
        line.set_ydata(yo)

        x = copy.deepcopy(xo)
        y = copy.deepcopy(yo)
 

        f.canvas.draw_idle()

    
    # f.canvas.draw()



def remove_point(event):
    global plot_button, x, y


    if(plot_button.value_selected=="Check All" or plot_button.value_selected=="Uncheck All"):
        if(plot_button.value_selected=="Uncheck All"):
            x = []
            y = []

        if(plot_button.value_selected=="Check All"):
            x = copy.deepcopy(xo)
            y = copy.deepcopy(yo)


        plot_button = RadioButtons(ax_check, labels, activated)
        plot_button.on_clicked(select_diselect_allrois)

    removed = False
    
    for i in range(len(x)):
        if( abs(event.xdata-x[i]) <= 0.009*lengthx and abs(event.ydata-y[i]) <= 0.009*lengthy and event.button == 3 ):  # REMOVE ROIS
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
        if( len(x) < prois and int(event.xdata)>1 ):    # ADD ROIS
            x.append(int(event.xdata))
            xvals = x[:]
            line.set_xdata(xvals)

            y.append(int(event.ydata))
            yvals = y[:]
            line.set_xdata(yvals)

            line.set_data(xvals,yvals)

            f.canvas.draw_idle()

        elif( len(x) >= prois and int(event.xdata)>=1 ):
            print("You have already len(rois) = %d points" %(prois))


    extent = ax.get_window_extent().transformed(f.dpi_scale_trans.inverted())



def close_figure_enter(event):
    if( event.key == 'enter' ):
        # plt.close(event.canvas.figure)

        plt.close('all')

        # if( gtext == "visitloud" ):
        #     os.system('TASKKILL /F /IM Microsoft.Media.Player.exe')



        # # os.system('TASKKILL /F /IM wmplayer.exe')

        # # os.system('TASKKILL /F /IM setup_wm.exe')
        
        # # os.system('TASKKILL /F /IM wmlaunch.exe')

        # # os.system('TASKKILL /F /IM wmpconfig.exe')

        # # os.system('TASKKILL /F /IM wmpnetwk.exe')

        # # os.system('TASKKILL /F /IM wmpnscfg.exe')

        # # os.system('TASKKILL /F /IM wmpshare.exe')