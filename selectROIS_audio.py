

import matplotlib
import copy
import pandas as pd
import matplotlib.pyplot as plt
from GetAndDrawROIS import getROIbounds
from movefigure import movefigure
from matplotlib.widgets import RadioButtons

from globalVars import folder1, textends
from findroisposition import findroisposition


globParams = {}

def selectROIS_audio(sub1, exam, text, pageno, roibounds, tempx, tempy, cgx, cgy, flag_seegazes, flag_roischecked, finalselectedrois, setglobParams_ref):
    plt.close("all")

    global globParams, setglobParams
    
    setglobParams = setglobParams_ref

    globParams["lengthx"] = len(cgx)
    globParams["lengthy"] = len(cgy)
    
    globParams["Xevent"] = finalselectedrois[pageno-1][0]
    globParams["Yevent"] = finalselectedrois[pageno-1][1]
    globParams["xo"] = []
    globParams["yo"] = []


    xroi, yroi, widthroi, heightroi = getROIbounds(text, pageno)
    globParams["prois"] = len(xroi)


    f=plt.figure()
    ax = plt.subplot(1,1,1)
    f.set_size_inches(8.2, 5.2)
    globParams["f"] = f
    globParams["ax"] = ax
    
    movefigure(f, 550, 10)   
    
    if(flag_seegazes):
        plt.plot(tempx, tempy, 'x', color='#6685E9', markeredgewidth=0.5)
        plt.plot(cgx, cgy, 'x', color='#E96F66', markeredgewidth=0.5)
    
    plt.title("Sub = " + str(sub1))
    ax.set_xticks([])
    ax.set_yticks([])
    plt.setp(ax.spines.values(), color=None)
    plt.xlabel("1:Παραποίηση, 2:Παράλειψη, \n3:Προσθήκη μετά από, 4:Παρατονισμός, 5:Αυτοδιόρθωση, \n6:Επανάληψη, 7:Γενική κατηγορία ")

    image = folder1 + 'texts/' + text + textends + '/Slide' + str(pageno) + '_no.PNG'
    img = plt.imread(image)
    ax.imshow(img)
    

    drawSelectedROIS(text, pageno, roibounds, flag_roischecked, finalselectedrois)
    
    ax_check = plt.axes([0.8, 0.05, 0.15, 0.15])
    labels = ['Check All', 'Uncheck All']
    activated = [0, 0]
    plot_button = RadioButtons(ax_check, labels, activated)
    plot_button.on_clicked(select_diselect_allrois)
    globParams["ax_check"] = ax_check
    globParams["labels"] = labels
    globParams["activated"] = activated
    globParams["plot_button"] = plot_button
    
    setglobParams("Xevent", globParams["Xevent"])
    setglobParams("Yevent", globParams["Yevent"])
    
    return 



def get_selectedROIS(text, pageno, finalx, finaly):
    xroi, yroi, widthroi, heightroi = getROIbounds(text, pageno)
    position = findroisposition(text, pageno)

    finalselectedrois = []
    for j in range(len(finalx)):
        position = findroisposition(text, pageno)
        for k in range(len(xroi)):
            if( (xroi[k]<= finalx[j] <xroi[k]+widthroi[k]) and  (yroi[k]<= finaly[j] <yroi[k]+heightroi[k])):
                finalselectedrois.append(position+1)
                break
            else:
                position += 1

    finalselectedrois.sort()

    # delete double selected ROIS
    finalselectedrois = list(dict.fromkeys(finalselectedrois))

    # print("ROIS_selected = ", finalselectedrois)
    
    return finalselectedrois



def zoomimage(text, pageno):
    data = pd.read_excel(folder1 + 'texts/' + text + textends + '/py/ROIbounds/mytext.page_' + str(pageno) + '.ROIbounds.xlsx')

    first_y = data.iloc[0, 1] - 5
    last_y = data.iloc[-1, 1] + data.iloc[-1, 3] + 5
    plt.ylim(last_y, first_y)
    
    return



def drawSelectedROIS(text, pageno, roibounds, flag_roischecked, finalselectedrois):

    #I WILL MAKE/DRAW THE ROI BOUNDS
    xroibounds = roibounds[0]
    yroibounds = roibounds[1]
    width = roibounds[2]
    height = roibounds[3]

    xo_temp = []
    yo_temp = []

    for i in range(len(xroibounds)):
        rect = matplotlib.patches.Rectangle((xroibounds[i],yroibounds[i]),
                                        width[i], height[i],
                                        color ='#79D0EB',
                                        fill=False)


        globParams["ax"].add_patch(rect)

        xo_temp.append( xroibounds[i]+ width[i]/2 )
        yo_temp.append( yroibounds[i]+ height[i]/2 )

    globParams["xo"] = xo_temp
    globParams["yo"] = yo_temp


    # If I want to be all checked at first
    if flag_roischecked:
        xdraw = copy.deepcopy(xo_temp)
        ydraw = copy.deepcopy(yo_temp)
        line, = globParams["ax"].plot(xdraw, ydraw, ls="None", linewidth=0, marker="o", color='lime', markersize=12, markerfacecolor='none', markeredgewidth=3)
    
    # If I want to be all unchecked at first
    if not flag_roischecked:
        xdraw = []
        ydraw = []
        line, = globParams["ax"].plot(xdraw, ydraw, ls="None", linewidth=0, marker="o", color='lime', markersize=12, markerfacecolor='none', markeredgewidth=3)

    # Draw previous selected
    if( finalselectedrois[pageno-1] != [[],[]] ):
        xdraw = finalselectedrois[pageno-1][0]
        ydraw = finalselectedrois[pageno-1][1]
        line, = globParams["ax"].plot(xdraw, ydraw, ls="None", linewidth=0, marker="o", color='lime', markersize=12, markerfacecolor='none', markeredgewidth=3)       
        globParams["f"].canvas.draw_idle()

    globParams["line"] = line
    globParams["Xevent"] = xdraw
    globParams["Yevent"] = ydraw
    
    globParams["f"].canvas.mpl_connect('button_press_event' , remove_point)

    zoomimage(text, pageno)

    return 




# function for displaying/hiding the plots
def select_diselect_allrois(label):
    
    # get the index that corresponds to the word "label"
    index = globParams["labels"].index(label)

    sizex = len(globParams["Xevent"])
    while( sizex > 0 ):
        del globParams["Xevent"][-1]
        xvals = globParams["Xevent"][:]
        globParams["line"].set_xdata(xvals)

            
        del globParams["Yevent"][-1]
        yvals = globParams["Yevent"][:]
        globParams["line"].set_ydata(yvals)

        globParams["line"].set_data(xvals,yvals)

        sizex = len(globParams["Xevent"])
        
    if( index == 1 ):
        globParams["f"].canvas.draw_idle()
        
    
    elif( index == 0 ):
        for i in range(len(globParams["xo"])):
            globParams["Xevent"].append(globParams["xo"][i])
            globParams["Yevent"].append(globParams["yo"][i])
            globParams["line"].set_data(globParams["Xevent"], globParams["Yevent"])

            globParams["f"].canvas.draw_idle()

    
    setglobParams("Xevent", globParams["Xevent"])
    setglobParams("Yevent", globParams["Yevent"])  
    
    extent = globParams["ax"].get_window_extent().transformed(globParams["f"].dpi_scale_trans.inverted())
    
    return




def remove_point(event):
    
    if( globParams["plot_button"].value_selected=="Check All"  or  globParams["plot_button"].value_selected=="Uncheck All"):
        if( globParams["plot_button"].value_selected=="Uncheck All"):
            globParams["Xevent"] = []
            globParams["Yevent"] = []

        if( globParams["plot_button"].value_selected=="Check All"):
            globParams["Xevent"] = copy.deepcopy(globParams["xo"])
            globParams["Yevent"] = copy.deepcopy(globParams["yo"])


        globParams["plot_button"] = RadioButtons(globParams["ax_check"], globParams["labels"], globParams["activated"])
        globParams["plot_button"].on_clicked(select_diselect_allrois)

    removed = False
    
    for i in range(len(globParams["Xevent"])):
        if( abs(event.xdata-globParams["Xevent"][i]) <= 0.009*globParams["lengthx"] and abs(event.ydata-globParams["Yevent"][i]) <= 0.009*globParams["lengthy"] and event.button == 3 ):  # REMOVE ROIS
            removed = True

            del globParams["Xevent"][i]
            xvals = globParams["Xevent"][:]
            globParams["line"].set_xdata(xvals)

                
            del globParams["Yevent"][i]
            yvals = globParams["Yevent"][:]
            globParams["line"].set_ydata(yvals)

            globParams["line"].set_data(xvals,yvals)
        
            globParams["f"].canvas.draw_idle()

            break

    if( removed == False and event.button == 1 ):
        if( len(globParams["Xevent"]) < globParams["prois"] and int(event.xdata)>1 ):    # ADD ROIS
            globParams["Xevent"].append(int(event.xdata))
            xvals = globParams["Xevent"][:]
            globParams["line"].set_xdata(xvals)

            globParams["Yevent"].append(int(event.ydata))
            yvals = globParams["Yevent"][:]
            globParams["line"].set_ydata(yvals)

            globParams["line"].set_data(xvals,yvals)

            globParams["f"].canvas.draw_idle()

        elif( len(globParams["Xevent"]) >= globParams["prois"] and int(event.xdata)>=1 ):
            print("You have already len(rois) = %d points" %(globParams["prois"]))

    setglobParams("Xevent", globParams["Xevent"])
    setglobParams("Yevent", globParams["Yevent"])
    
    extent = globParams["ax"].get_window_extent().transformed(globParams["f"].dpi_scale_trans.inverted())
    
    return



# def setglobalParams(paramname, param):
#     global globParams
#     globParams[paramname] = param
#     return 
    
    
# def getEvents(paramname):
#     return globParams[paramname]
    

#############################################################################################