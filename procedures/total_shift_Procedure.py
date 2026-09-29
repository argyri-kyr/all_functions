
from asyncio.windows_events import NULL
import os
import time
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
from matplotlib.patches import Rectangle


from globalVars import folder1, folder2, textends, pyimagepath, dispersion, dispersion2, guiflag
from basic_function_gui import basic_function_gui
from GetSomeInitialData import createextra, getGazesFolderbyText, getGazesFoldersandClass

from MakeFixationsFile import MakeFixationsTxt
from MakeGazesFile import MakeGazesTxt
from GetAndDrawROIS import getROIbounds, drawROIbounds
from creategazedata import CreateGazeData
from drawFixations import drawFixations
from semiauto_or_auto_process.concatdata import concatdata
from movefigure import movefigure
from loaduncutdata_hardcases import loaduncutdata_hardcases
from fixationfungap import fixationfungap
from drawEyeMovements import drawEyeMovements
from MakeDispersionTxt import MakeDispersionTxt
from loadcutgazesdata import loadcutgazesdata
from MakePageFixationsGap import MakePageFixationsGap
from load_subs_initial_data import load_subs_initial_data
from make_textfolder_struct import make_textfolder_struct



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                 #
#                                                                                 #
#                                                                                 #
#           AFTH H SINARTHSH KANEI KATHOLIKO SHIFT SE OLO TO KEIMENO              #
#                                                                                 #
#                                                                                 #
#                                                                                 #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #




def total_shift_Procedure(subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye):

    global from_runcrashes
    from_runcrashes = False


    # Replace no valid gazes with valid
    global nonvalid2valid
    nonvalid2valid = 0   # 0 for do nothing, 1 for replace
    ###################################
    
    global hardcases_glob
    hardcases_glob = hardcases
    
    
    global loadgazes
    loadgazes = int(input("Load from rawgazes( press 1 ) or cutgazes( press 2 ): "))
    if(loadgazes==1):
        loadgazes = True
    else:
        loadgazes = False
    
    

    # Orizw se poia exam einai to kathe subject
    exam = 1
    


    # Kuria while loop gia na trexoun ola ta subject pou thelw ( trexw 1h loop gia ta subject kai 2h eswterikh loop gia ta texts tou subject )
    for i in range(len(subs)): 
        
        # load subjects data, i.e if subject exist and which texts has this subject
        gazesfolders, analysis_texts, textanalysisfiles = load_subs_initial_data(subs[i], exam, texts, from_runcrashes)      
        if( gazesfolders == NULL ):
            continue         
        
        for j in range (len(analysis_texts)):
            text = analysis_texts[j]
            file = textanalysisfiles[j]
            
            # Make the folders (if not exist) that i will use to store graphs and data for my texts
            make_textfolder_struct(subs[i], exam, text)
            

            if os.path.exists( folder1 + folder2 + 'subject_' + str(subs[i]) + "/" + file + "/gazes-orignal-1920.txt" ):
                print("\nFound SD gazes file on subject " + str(subs[i]))
                print("Considering changing analysis version or fix the file.")
                print("Do not forget that you also need the SD texts.\n")
                time.sleep(5)
                break
    

            Start_Text_Procedure(file, subs[i], exam, text, onlylefteye, onlyrighteye)  # Main procedure of the programme for each text
            
        
        
        if( analysis_texts==[] ):
            print("\nΝo texts were found for Subject = %d " % subs[i])
            time.sleep(3)

              
    # Delete unneeded .txts 
    for file in os.listdir():
        if( file.endswith(".txt") ):
            if( os.stat(file).st_size==0 ):
                os.remove(file)
    




#Procedure's args ={ (text : text i will analyze), (folder : main folder), (sub1 : subject's id), (sub1class : subject's class) }
def Start_Text_Procedure(file, sub1,  exam, text, onlylefteye, onlyrighteye):
    global mypagecollection
    

    # Load Gazes Data
    if( loadgazes==True ):
        uncutgazes_raw, uncutgazes, negativecheck, oneeyeindexes = loaduncutdata_hardcases(text, exam, file, sub1, onlylefteye, onlyrighteye)

        # # # # #  Collect gazes data per column  # # # # #
        index, x, y, timestamp, roi, validity, vergence, pupilsize = uncutgazes[0], uncutgazes[1], uncutgazes[2], uncutgazes[3], uncutgazes[4], uncutgazes[5], uncutgazes[6], uncutgazes[7]
    
    
    # Load cutgazes data
    elif ( loadgazes==False ):
        index, x, y, timestamp, roi, pagenumber, validity, vergence, pupilsize = loadcutgazesdata(sub1, exam, text)
    
    
    ##############################  START PROCESS  ##############################
    
    #Temporary lists that will save the cutgazes data per page
    pageno = -1             #page number, assumption pageno=-1

    tempindex = []          
    tempx = []              #temporary x list
    tempy = []              #temporary y list
    temptimestamp = []      #temporary timestamp list
    temproi = []
    tempvalidity = []
    tempvergence = []
    temppupilsize = []


    i=-1
    
    #Μεχρι να φτασω στο τελος του αρχειου cutgazes.txt θα μπαινω να κανω την αναλυση
    #δηλαδη γεμιζω προσωρινες λιστες με τα data ανα σελιδα(index, x, y, timestamp)
    #και δημιουργω τα αρχεια fixations.txt , cutgazes.txt ,
    #κανω τα plot που χρειαζομαι και βρισκω fixations και rois οπου χρειαζεται
    while( i<len(index) ):
        i+=1
        if(   (loadgazes and i<len(index) and index[i] == 1)  or (not loadgazes and i>0 and i<len(index) and index[i]<index[i-1])  or  (i == len(index))  or  (i==0)   ):
            pageno+=1

            if(pageno>0) :
                roibounds = getROIbounds(text, pageno)             # Βρισκω τα ROIbounds του κειμενου

                roistartpath = folder1 + 'texts/' + text + textends + '/py/mytext/page(' + str(pageno) + ')/ROIstart/ROIstart.xlsx'
                roistart = pd.read_excel(roistartpath, header=None).values[0][0]
                
                print("\nsubject %d, text %s, page %d " %(sub1, text, pageno))          #Βρισκω τα ROIbounds του κειμενου

            if( len(tempindex) != 0 ):                  #Οταν φτασω στο τελος της 1ης σελιδας και εχω συλλεξει τα δεδομενα μου                                                               
                mypagecollection = [tempindex, tempx, tempy, temptimestamp, temproi, tempvalidity, tempvergence, temppupilsize]

                MainProcedure(sub1, exam, text, pageno, roibounds, mypagecollection)
                
                cgdata = [tempindex, tempx, tempy, temptimestamp, temproi, tempvalidity, tempvergence, temppupilsize]

                gazedata = CreateGazeData(cgdata)

                #Make cutgazes.txt file
                MakeGazesTxt(sub1, exam, text, pageno, gazedata)


                # # # # # # # # # # # # # # # # # # # # # # #  Gap Process -- NEW FIXATION  # # # # # # # # # # # # # # # # # # # # # # 

                #Find Fixations and Make fixations.txt file
                fixationdatagap, gazestart, gazeend, fixationstart, fixationend, gap_data = fixationfungap(gazedata, roistart, roibounds)
                MakeFixationsTxt(sub1, exam, text, pageno, roistart, fixationdatagap, roibounds)
                MakeDispersionTxt(sub1, exam, text)
                MakePageFixationsGap(sub1, exam, text, pageno, gazestart, gazeend, fixationstart, fixationend, gap_data)
                
                # # # # # # # # # # # # # # # # # # # # # # End Gap Process # # # # # # # # # # # # # # # # # # # # # # 
                
             
                #Draw fixations(pane_number).png images
                print("Creating fixation images with dispersion ", dispersion, "-", dispersion2)
                drawFixations(sub1, exam, text, fixationdatagap, pageno, "yes", NULL)

                # Draw fixations(pane_number).png colored arrows
                drawEyeMovements(sub1, exam, text, fixationdatagap, pageno, NULL)
         
                #Draw cutgazes(pane_number).png images
                drawROIbounds(sub1, exam, text, pageno, roibounds, cgdata[1], cgdata[2], "cutgazes", fixationdatagap, NULL, "close") 

           

            #Αδειαζω τις λιστες που περιεχουν τα δεδομενα της σελιδας που επεξεργαστηκα, ωστε να αποθηκευσω τα νεα δεδομενα της επομενης σελιδας
            tempindex = []
            tempx = []
            tempy = []
            temptimestamp = []
            temproi = []
            tempvalidity = []
            tempvergence = []
            temppupilsize = []
            
            plt.close('all')
        

        #Εδω δημιουργω τις λιστες των δεδομενων ανα σελιδα   
        if( i != len(index) ):
            tempindex.append( index[i] )
            tempx.append( x[i] )
            tempy.append( y[i] )
            temptimestamp.append( timestamp[i] )
            temproi.append( roi[i] )
            tempvalidity.append( validity[i] )
            tempvergence.append( vergence[i] )
            temppupilsize.append( pupilsize[i] )


    concatdata(sub1, exam, text, 'cutgazes', 'fixations')
    
    return
    

    

def MainProcedure(sub, exam, text, pageno, roibounds, mypagecollection):
    global fig, ax
    
    # SaveLinesteps(sub, exam, text, pageno,  mypagecollection[1], mypagecollection[2])  
    
    fig, ax = Shift_Procedure(sub, exam, text, pageno, roibounds, mypagecollection) 
    plt.show()
    
    return 




def Shift_Procedure(sub, exam, text, pageno, roibounds, mypagecollection):
    global fig, ax, indicator, mouse_pressed

    # # create the figure & the axes
    fig, ax = plt.subplots(1,1,constrained_layout=True)
    fig.set_size_inches(9, 7)
    ax.margins(x=0)
    plt.title("Test Attention - Gazes Preview\n")
    movefigure(fig, 500, 100)
    # plt.xlabel("X")
    # plt.ylabel("Y")
    # plt.axis('off')
    
    
    # # plot the points
    tempx = mypagecollection[1]
    tempy = mypagecollection[2]
    plt.scatter(tempx,tempy, marker='x')   # # # # # if i want to set a color like red, add this:    c='red'

    
    # # draw the text image
    image = folder1 + 'texts/'+ text + textends + '/Slide' + str(pageno) + '.PNG'
    img = plt.imread(image)
    ax.imshow(img)
    
    
    # # load/draw the black frame in plot
    a = plt.gca()
    xax = a.axes.get_xaxis()
    xax = xax.set_visible(False)
    yax = a.axes.get_yaxis()
    yax = yax.set_visible(False)
    # end of show frame in plot


    # # Bind the callback functions to the mouse events 
    mouse_pressed = False
    indicator = 0
    ax.figure.canvas.mpl_connect('button_press_event', on_mouse_press)
    ax.figure.canvas.mpl_connect('motion_notify_event', lambda event: on_mouse_move(event, text, pageno))
    fig.canvas.mpl_connect('button_release_event', on_mouse_release)
    fig.canvas.mpl_connect('key_press_event', lambda event: on_key_press(event, sub, exam, text, pageno, roibounds))
    
    # fig.canvas.mpl_connect('motion_notify_event', on_mouse_motion)
        
    return fig, ax

  



def on_mouse_press(event):
    global start_x, start_y, x, y, rectangle, indicator, mouse_pressed
    
    if( event.xdata == None ):
        return
    
    if event.button==1:
        # #Remove previous rectangle, before draw an other one, procedure from one left click to another left click
        indicator += 1
        if( indicator>1 ):
            rectangle.set_xy((0, 0))
            rectangle.set_width(0)
            rectangle.set_height(0)
            rectangle.set_visible(False)
            fig.canvas.draw_idle()
        # # end of remove previous rectangle
            
        # # Start draw a new rectangle, when left click pressed
        start_x = event.xdata
        start_y = event.ydata

        rectangle = Rectangle((start_x, start_y), 0, 0, color='#ff8080', alpha=0.4)

        
        ax.add_patch(rectangle)
    
    # # when right click pressed i want to keep watching the rectangle i have already draw, so I refactor it from its previous coords 
    if event.button==3:
        mouse_pressed = True
        
        # xprev = rectangle.get_x()
        # yprev = rectangle.get_y()
        # w = rectangle.get_width()
        # h = rectangle.get_height()
        
        # rectangle.set_visible(True)
        # rectangle.set_width(w)
        # rectangle.set_height(h)
        # rectangle.set_xy((xprev, yprev))
        # fig.canvas.draw_idle()
                



def on_mouse_move(event, text, pageno):
    global x, y, rectangle, mouse_pressed
    
    if( event.xdata == None ):
        return
    
    # # Create the rectangle while left cursor in pressed
    if event.button == 1:
        x = event.xdata
        y = event.ydata

        
        rectangle.set_width(x - start_x)
        rectangle.set_height(y - start_y)
        rectangle.set_xy((start_x, start_y))

        fig.canvas.draw_idle()
    # # end of create the rectangle while left cursor in pressed
    
    # # move the rectangle , but first save its previous position in order to know how much was x-shifted and y-shifted after i moved it
    if event.button == 3:
        if mouse_pressed:
            xprev = rectangle.get_x()
            yprev = rectangle.get_y()
            
            rectangle.set_xy((event.xdata, event.ydata))

            
            xshift = event.xdata - xprev
            yshift = event.ydata - yprev
            
            # move also the points that are included into the rectangle
            moveIncludedGazes2(text, pageno, includedgazes_index, xshift, yshift)
            
            fig.canvas.draw_idle()
    # # end of move rectangle and its points   
    
    return 
        


def on_mouse_release(event):
    global includedgazes_index, mouse_pressed
    
    if( event.xdata == None ):
        return
    
    if event.button==1:
        includedgazes_index = findIncludedGazes()
    
    if event.button == 3:
        mouse_pressed = False
    



def on_key_press(event, sub, exam, text, pageno, roibounds):
    global rectangle, includedgazes_index
    
    if event.key == 'up':
        myshift = -10
        moveIncludedGazes(event.key, myshift, text, pageno, includedgazes_index)

        
    elif event.key == 'down':
        myshift = +10
        moveIncludedGazes(event.key, myshift, text, pageno, includedgazes_index)
        

    elif event.key == 'left':
        myshift = -10
        moveIncludedGazes(event.key, myshift, text, pageno, includedgazes_index)


    elif event.key == 'right':
        myshift = +10
        moveIncludedGazes(event.key, myshift, text, pageno, includedgazes_index)
    
    
    elif event.key =='enter':
        if( 'rectangle' in globals() ):
            rectangle.set_visible(False)
        drawROIbounds(sub, exam, text, pageno, roibounds, mypagecollection[1], mypagecollection[2], "rawgazes", [], plt, "close")   # In order to draw and save the rawgazes(pageno).png images
        plt.close('all')

    # Redraw the plot
    fig.canvas.draw()




def findIncludedGazes():
    xstart = rectangle.get_x()
    ystart = rectangle.get_y()
    xend = xstart + rectangle.get_width()
    yend = ystart + rectangle.get_height()
        
    includedgazes_index = []
    for i in range(len(mypagecollection[1])):
        if( xstart <= mypagecollection[1][i] <= xend and ystart <= mypagecollection[2][i] <= yend ):
            includedgazes_index.append(i)
    
    return includedgazes_index
    
    
    

def moveIncludedGazes(event_key, myshift, text, pageno, includedgazes_index):
    global rectangle

    # # clear all the plot
    ax.clear()
    
    # # draw again the rectangle
    if( event_key=='up' or event_key=='down' ):
        rectangle.set_y(rectangle.get_y() + myshift)
        moved_index = 2
    elif( event_key=='left' or event_key=='right' ):
        rectangle.set_x(rectangle.get_x() + myshift)
        moved_index = 1
    
    ax.add_patch(rectangle)

    # # move the points included into the rectangle
    j=0
    for i in range(len(mypagecollection[1])):
        if( j<len(includedgazes_index) and (i==includedgazes_index[j]) ):
            mypagecollection[moved_index][i] = mypagecollection[moved_index][i] + myshift
            j+=1    
    
    ax.scatter(mypagecollection[1], mypagecollection[2], marker='x')
    
    # # load again the text
    image = folder1 + 'texts/'+ text + textends + '/Slide' + str(pageno) + '.PNG'
    img = plt.imread(image)
    ax.margins(x=0)
    plt.title("Test Attention - Gazes Preview\n")
    
    ax.imshow(img)
    
    # # load/draw the black frame in plot
    a = plt.gca()
    xax = a.axes.get_xaxis()
    xax = xax.set_visible(False)
    yax = a.axes.get_yaxis()
    yax = yax.set_visible(False)
    # # end of draw frame in plot
    
    # # redraw the whole plot
    fig.canvas.draw()
    



def moveIncludedGazes2(text, pageno, includedgazes_index, xshift, yshift):
    global rectangle

    # # clear all the plot
    ax.clear()

    # # add the rectangle again into plot
    ax.add_patch(rectangle)

    
    # # move the points included into the rectangle
    j=0
    for i in range(len(mypagecollection[1])):
        if( j<len(includedgazes_index) and (i==includedgazes_index[j]) ):
            mypagecollection[1][i] = mypagecollection[1][i] + xshift
            mypagecollection[2][i] = mypagecollection[2][i] + yshift
            j+=1    
    
    ax.scatter(mypagecollection[1], mypagecollection[2], marker='x')
    # #
    
    # # load again the text
    image = folder1 + 'texts/'+ text + textends + '/Slide' + str(pageno) + '.PNG'
    img = plt.imread(image)
    ax.margins(x=0)
    plt.title("Test Attention - Gazes Preview\n")
    
    ax.imshow(img)
    # #
    
    # # load/draw the black frame in plot
    a = plt.gca()
    xax = a.axes.get_xaxis()
    xax = xax.set_visible(False)
    yax = a.axes.get_yaxis()
    yax = yax.set_visible(False)
    # # end of show frame in plot
    
    # # redraw the whole plot
    fig.canvas.draw()
    



    
"""

def on_mouse_motion(event):
    global rectangle, mouse_pressed

    if event.button==3:
        if mouse_pressed:
            rectangle.set_xy((event.xdata, event.ydata))
            fig.canvas.draw_idle()
        



def SaveLinesteps(sub, exam, text, pageno, tempx, tempy):
    
    f = plt.figure()
    f.set_figwidth(14)
    f.set_figheight(9)
    ax = plt.subplot(1,1,1)
    ax.margins(x=0)
    # plt.subplots_adjust(left = 0.15)
    
    plt.plot(tempx,'yellow')
    if( hardcases_glob ):
        plt.plot(tempy,'bo', markersize=1)
    else:
        plt.plot(tempy,'b')

    pagesfile = open(folder1 + "texts/" + text + textends + "/py/pages/pages.txt", "r")
    pages = pagesfile.read(1)


    plt.title( "Subject: " + str(sub) + ", Text: " + text + ", Page: " + str(pageno) + " out of " + str(pages) )

    plt.savefig(folder1 + folder2 + 'subject_' + str(sub) + '/all_graphs/' + text + str(exam) + pyimagepath + '/linesteps' + str(pageno) + '.png')
    
    movefigure(f, 3, 10)
    
    plt.close('all')

    return 
    
"""



