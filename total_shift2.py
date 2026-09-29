
from asyncio.windows_events import NULL
import os
import time
import shutil
import statistics
from os.path import exists
from matplotlib.patches import Rectangle
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import tkinter as tk




from globalVars import folder1, folder2, textends, pyimagepath, dispersion, dispersion2, guiflag
from basic_function_gui import basic_function_gui
from GetSomeInitialData import createextra, getGazesFolderbyText, getGazesFoldersandClass
from createSubfile import createSubfile
from gazeshandling import gazeshandling

from semiauto_or_auto_process.storerawdata import storegazedata, storevergencedata, store_pupil_z_data
from semiauto_or_auto_process.commonfunctions import getpagelines
from MakeFixationsFile import MakeFixationsTxt
from MakeGazesFile import MakeGazesTxt
from creategazedata import CreateGazeData
from semiauto_or_auto_process.concatdata import concatdata
from storefinalindexes import storefinalindexes
from movefigure import movefigure
from loaduncutdata_hardcases import loaduncutdata_hardcases
from fixationfungap import fixationfungap
from drawEyeMovements import drawEyeMovements
from MakeDispersionTxt import MakeDispersionTxt
from totalshift_askbox import totalshift_askbox
from loadcutgazesdata import loadcutgazesdata   
from MakePageFixationsGap import MakePageFixationsGap
from GetAndDrawROIS import getROIbounds


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


globParams = {}


def main1():

    global from_runcrashes
    from_runcrashes = False


    # Replace no valid gazes with valid
    global nonvalid2valid
    nonvalid2valid = 0   # 0 for do nothing, 1 for replace
    ###################################
    
    global loadgazes
    loadgazes = False
    
    global hardcases

    if( guiflag ):
        textcheckedflag = 1
        subs = NULL
        while( subs==NULL ):
            subs, texts, firstchoices = basic_function_gui(textcheckedflag)
        bypass, hardcases, onlylefteye, onlyrighteye = firstchoices[0], firstchoices[1], firstchoices[2], firstchoices[3]

    else:
        # texts = [ 'visit', 'zoo', 'visitloud', 'psaras', 'morning', 'island', 'efeyreseis', 'zebra', 'armyjet', 'enemypie', 'gasmask', 'jockey', 'midfred', 'midfredloud', 'sunny', 'sunnyloud' ]
        # texts = ['visit', 'visitloud', 'zoo', 'psaras', 'efeyreseis', 'sunny', 'midfred', 'midfredloud', 'armyjet', 'gasmask']
        # texts = ['zoo', 'visit']
        texts = ['testapartf3']
        
        # subs = [1455, 1456, 1459, 1460, 1461]
        # subs = [ person  for person  in range(908, 920) ]
        # subs = [x for x in range(13100, 13103)]
        subs = [14036]
        
        bypass = 1
        hardcases = 0
        onlylefteye = 1
        onlyrighteye = 0
        firstchoices = [bypass, hardcases, onlylefteye, onlyrighteye]


    # Orizw se poia exam einai to kathe subject
    exam = []
    


    # Kuria while loop gia na trexoun ola ta subject pou thelw ( trexw 1h loop gia ta subject kai 2h eswterikh loop gia ta texts tou subject )
    for i in range(len(subs)): 
        proceduredone = True

        search1 = getGazesFoldersandClass(subs[i])   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/
        search2 = createSubfile(subs[i])             # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Users/RADAR/Documents/Optotech/
        
        if( search1 == NULL ):
            if(search2==NULL):
                exam.append(1)
                print("Subject %s doesn't exist" %subs[i])
                time.sleep(5)
                continue
            else:
                gazesfolders, sub1class, subexam = search2[0], search2[1], search2[2]
                exam.append(int(subexam))
        
        else:
            if(search2==NULL):
                gazesfolders, sub1class, subexam = search1[0], search1[1], search1[2]
                exam.append(int(subexam)) 
            else:
                gazesfolders1, sub1class, subexam = search1[0], search1[1], search1[2]   # gazesfolders1 : ta keimena pou brethikan mesa sto individual
                gazesfolders2, sub1class, subexam = search2[0], search2[1], search2[2]   # gazesfolders2 : ta keimena pou brethikan mesa sto Documents/Optotech
                gazesfolders = gazesfolders1 + gazesfolders2   # sinolo keimenwn giafto to subject
                gazesfolders = list(dict.fromkeys(gazesfolders))
                exam.append(int(subexam))                               
                             


        # Briskw apo ta keimena pou exw epilexei gia poia apo afta exw dedomena wste na kanw thn analysh mono se afta    
        analysis_texts = []
        textanalysisfiles = []
        for text in texts:
            file = getGazesFolderbyText(subs[i], exam[i], text, gazesfolders, sub1class, from_runcrashes)
            
            if( file != NULL ):
                gazesfilepath = folder1 + folder2 + 'subject_' + str(subs[i]) + '/' + file + '/gazes.txt'  
                if not os.path.exists( gazesfilepath ):
                    shutil.rmtree(folder1 + folder2 + 'subject_' + str(subs[i]) + '/' + file)
                    gazesfolders.remove(file)
                    texts.append(text)
                    continue

            if( file != NULL ):
                createextra(subs[i], file)
                analysis_texts.append(text)
                textanalysisfiles.append(file)
                
                
        print("\n",*analysis_texts)
        for j in range (len(analysis_texts)):
            text = analysis_texts[j]
            file = textanalysisfiles[j]
            
            # Make the folders (if not exist) that i will use to store graphs and data for my texts
            if not os.path.exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_data/' + text + str(exam[i])):
                os.makedirs(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_data/' + text + str(exam[i]))

            if not os.path.exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i])):
                os.makedirs(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i]))
                        
            if not os.path.exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i]) + pyimagepath):
                os.makedirs(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i]) + pyimagepath)
            

            if os.path.exists( folder1 + folder2 + 'subject_' + str(subs[i]) + "/" + file + "/gazes-orignal-1920.txt" ):
                proceduredone = False
                print("\nFound SD gazes file on subject " + str(subs[i]))
                print("Considering changing analysis version or fix the file.")
                print("Do not forget that you also need the SD texts.\n")
                time.sleep(5)
                break
    
            if( (not exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i]) + '_pass.txt')) and (not exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i]) + '_crash.txt')) ):
                # Ksekinaei h analysh twn keimenwn 
                proceduredone = False
                Procedure(file, subs[i], exam[i], text, onlylefteye, onlyrighteye)  # Main procedure of the programme for each text
            
            
            elif( (bypass==1) and (exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i]) + '_pass.txt')) ):
                # Ksekinaei h analysh twn keimenwn 
                os.remove(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i]) + '_pass.txt')
                proceduredone = False
                Procedure(file, subs[i], exam[i], text, onlylefteye, onlyrighteye)  # Main procedure of the programme for each text
            
        
        # Handle some messages
        if(  proceduredone == True and  analysis_texts!=[] ):
            print("\nAnalysis has been done for Subject = %d " % subs[i])
            time.sleep(3)
        
        elif( analysis_texts==[] ):
            print("\nΝo texts were found for Subject = %d " % subs[i])
            time.sleep(3)

              
    #Delete unneeded .txts 
    for file in os.listdir():
        if( file.endswith(".txt") ):
            if( os.stat(file).st_size==0 ):
                os.remove(file)
    





#Procedure's args ={ (text : text i will analyze), (folder : main folder), (sub1 : subject's id), (sub1class : subject's class) }
def Procedure(file, sub1,  exam, text, onlylefteye, onlyrighteye):
    global mypagecollection
    
    from_runcrashes = False
 
    # # Loat some data # #
    newgazes, vergence_list, vergence_z = gazeshandling(file, sub1)


    # # # # # Collect vergence data per column  # # # # #
    vergenceindex, vergenceleftx, vergencelefty, vergencerightx, vergencerighty, vergencetimestamp, vergencepupilleft, vergencepupilright, vergenceleftz, vergencerightz = [], [], [], [], [], [], [], [], [], []
    for i in range(len(vergence_list)):
        vergenceindex.append( vergence_list[i][0] )
        vergenceleftx.append( vergence_list[i][1] )
        vergencelefty.append( vergence_list[i][2] )
        vergencerightx.append( vergence_list[i][3] )
        vergencerighty.append( vergence_list[i][4] )  
        vergencetimestamp.append( vergence_list[i][5] ) 
        vergencepupilleft.append( vergence_list[i][7] )  
        vergencepupilright.append(vergence_list[i][8] )        

        vergenceleftz.append( vergence_z[i][0] )
        vergencerightz.append( vergence_z[i][1] )



    # Load Gazes Data
    if( loadgazes ):
        uncutgazes_raw, uncutgazes, negativecheck, oneeyeindexes = loaduncutdata_hardcases(text, exam, file, sub1, onlylefteye, onlyrighteye)

        # # # # #  Collect gazes data per column  # # # # #
        index, x, y, timestamp, roi, validity, vergence, pupilsize = uncutgazes[0], uncutgazes[1], uncutgazes[2], uncutgazes[3], uncutgazes[4], uncutgazes[5], uncutgazes[6], uncutgazes[7]
    
    
    # Load cutgazes data
    elif ( not loadgazes ):
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
        if(   (loadgazes and i<len(index) and index[i] == 1)  or (not loadgazes and i>0 and index[i]<index[i-1])  or  (i == len(index))  or  (i==0)   ):
            pageno+=1

            if(pageno>0) :
                lines = getpagelines(text, pageno)                 # Βρισκω ποσες γραμμες εχει η σελιδα οπου βρισκομαι
                roibounds = getROIbounds(text, pageno)             # Βρισκω τα ROIbounds του κειμενου

                roistartpath = folder1 + 'texts/' + text + textends + '/py/mytext/page(' + str(pageno) + ')/ROIstart/ROIstart.xlsx'
                roistart = pd.read_excel(roistartpath, header=None).values[0][0]
                
                print("\nsubject %d, text %s, page %d " %(sub1, text, pageno))          #Βρισκω τα ROIbounds του κειμενου

            if( len(tempindex) != 0 ):                  #Οταν φτασω στο τελος της 1ης σελιδας και εχω συλλεξει τα δεδομενα μου                                                               
                
                mypagecollection = [tempindex, tempx, tempy, temptimestamp, temproi, tempvalidity, tempvergence, temppupilsize]

                # # # # # # # # # Store gazedata per page, i.e gazes_page1.txt, gazes_page2.txt, gazes_page3.txt, .....  # # # # # # # # #
                gazedatatxt = folder1 + folder2 + '/subject_' + str(sub1) + '/' + file + '/py/gazes_page' + str(pageno) + '.txt'
                gazedatafile = open(gazedatatxt, 'w')
                gazedatafile.close()
                storegazedata(gazedatatxt, mypagecollection)    # store raw data


                # # # # # # # # #  Store validationdata per page  # # # # # # # # #
                # #  vergence_page1.txt, vergence_page2.txt, vergence_page3.txt,  ......  
                # #  median_pupil_z_data_page1.txt, median_pupil_z_data_page2.txt,  ......
                # #  pupilsize_z_page1.txt, pupilsize_z_page2.txt,  ......
                if( vergence_list!= [] ):
                    # store vergence
                    validationdatatxt = folder1 + folder2 + '/subject_' + str(sub1) + '/' + file + '/py/vergence_page' + str(pageno) + '.txt'
                    validationdatafile = open(validationdatatxt, 'w')
                    validationdatafile.close()
                    storevergencedata(validationdatatxt, vergenceindex, vergenceleftx, vergencelefty, vergencerightx, vergencerighty, vergencetimestamp, vergencepupilleft, vergencepupilright)
                
                    # store pupilsize
                    pupildatatxt = folder1 + folder2 + '/subject_' + str(sub1) + '/' + file + '/py/pupilsize_z_page' + str(pageno) + '.txt'
                    pupildatafile = open(pupildatatxt, 'w')
                    pupildatafile.close()
                    store_pupil_z_data(pupildatatxt, vergencepupilleft, vergencepupilright, vergenceleftz, vergencerightz)  

                    # store pupilsize median 
                    medianpupilzdatatxt = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/median_pupil_z_data_page' + str(pageno) + '.txt'
                    medianpupilzdatafile = open(medianpupilzdatatxt, 'w')
                    
                        # # median pupil left & pupil right
                    medianpupilleft = statistics.median(vergencepupilleft)              
                    medianpupilright = statistics.median(vergencepupilright)
                        # # median Z left & Z right
                    medianleftz = statistics.median(vergenceleftz)              
                    medianrightz = statistics.median(vergencerightz)

                    medianpupilzdatafile.write( str(medianpupilleft) + "\t" + str(medianpupilright) + "\t" + str(medianleftz) + "\t" + str(medianrightz) + "\n" )  
                    medianpupilzdatafile.close()

                    # # # # # # # # End of Store Some Data # # # # # # # # 

            
                
                root, xs_entry, ys_entry, xe_entry, ye_entry = totalshift_askbox(text, pageno, setmypagecollection, getParam)
                MainProcedure(sub1, exam, text, pageno, mypagecollection, xs_entry, ys_entry, xe_entry, ye_entry)
                # root.mainloop()
                
                finalindexes = [tempindex[0], tempindex[-1]]
                cgdata = [tempindex, tempx, tempy, temptimestamp, temproi, tempvalidity, tempvergence, temppupilsize]
                
                
                # drawROIbounds(sub1, exam, text, pageno, roibounds, cgdata[1], cgdata[2], "rawgazes", [], plt, "close") #In order to draw and save the rawgazes(pageno).png images

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
                # drawFixations(sub1, exam, text, fixationdatagap, pageno, "yes", NULL)

                # Draw fixations(pane_number).png colored arrows
                drawEyeMovements(sub1, exam, text, fixationdatagap, pageno, NULL)
         
                #Draw cutgazes(pane_number).png images
                # drawROIbounds(sub1, exam, text, pageno, roibounds, cgdata[1], cgdata[2], "cutgazes", fixationdatagap, NULL, "close") 

                # Store finalindexes per page 
                storefinalindexes(sub1, pageno, file, finalindexes)
           

            #Αδειαζω τις λιστες που περιεχουν τα δεδομενα της σελιδας που επεξεργαστηκα, ωστε να αποθηκευσω τα νεα δεδομενα της επομενης σελιδας
            tempindex = []
            tempx = []
            tempy = []
            temptimestamp = []
            temproi = []
            tempvalidity = []
            tempvergence = []
            temppupilsize = []
            
            vergenceindex = []
            vergenceleftx = []
            vergencelefty = []
            vergencerightx = []
            vergencerighty = []
            vergencetimestamp = []

            vergencepupilleft = []
            vergencepupilright = []

            vergenceleftz = []
            vergencerightz = []

            
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



            if( vergence_list!=[] ):
                vergenceindex.append( vergence_list[i][0] )
                vergenceleftx.append( vergence_list[i][1] )
                vergencelefty.append( vergence_list[i][2] )
                vergencerightx.append( vergence_list[i][3] )
                vergencerighty.append( vergence_list[i][4] )  
                vergencetimestamp.append( vergence_list[i][5] ) 
                vergencepupilleft.append( vergence_list[i][7] )  
                vergencepupilright.append(vergence_list[i][8] )        

                vergenceleftz.append( vergence_z[i][0] )
                vergencerightz.append( vergence_z[i][1] )


    concatdata(sub1, exam, text, 'cutgazes', 'fixations')

    textpasstxt = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + '_pass.txt'
    textpassfile = open(textpasstxt, 'w')
    textpassfile.close()
    
    root.mainloop()


    

def MainProcedure(sub, exam, text, pageno, mypagecollection, xs_entry, ys_entry, xe_entry, ye_entry):
    global fig, ax

    fig, ax = Shift_Procedure(text, pageno, mypagecollection, xs_entry, ys_entry, xe_entry, ye_entry) 
    plt.show()
    
    SaveLinesteps(sub, exam, text, pageno,  mypagecollection[1], mypagecollection[2])  
    return 



def Shift_Procedure(text, pageno, mypagecollection, xs_entry, ys_entry, xe_entry, ye_entry):
    global fig, ax, rect_selector, rectangle, indicator
    tempx = mypagecollection[1]
    tempy = mypagecollection[2]
    
    
    image = folder1 + 'texts/'+ text + textends + '/Slide' + str(pageno) + '.PNG'
    img = plt.imread(image)
   
    fig, ax = plt.subplots(1,1,constrained_layout=True)
    fig.set_size_inches(9, 7)
    ax.margins(x=0)
    mpl.rcParams['savefig.pad_inches'] = 0
    
    plt.title("Test Attention - Gazes Preview\n")
    movefigure(fig, 350, 100)


    plt.scatter(tempx, tempy, marker='x')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis('off')
    
    ax.imshow(img)

    # # Initialize the RectangleSelector object outside of the main_plot() function
    # rect_selector = RectangleSelector(
    #     ax, line_select_callback, useblit=True, drawtype='box', button=[1], interactive=True)
    
    indicator = 0
    
    ax.figure.canvas.mpl_connect('button_press_event', on_mouse_press)
    ax.figure.canvas.mpl_connect('motion_notify_event', on_mouse_move)
    
    fig.canvas.mpl_connect('key_press_event', lambda event, xstart_entry=xs_entry, ystart_entry=ys_entry, xend_entry=xe_entry, yend_entry=ye_entry: on_key_press(event, xstart_entry, ystart_entry, xend_entry, yend_entry))


    return fig, ax




def on_mouse_press(event):
    global start_x, start_y, rectangle, indicator
    
    indicator += 1
    
    # Remove previous rectangle
    if( indicator>1 ):
        rectangle.set_xy((0, 0))
        rectangle.set_width(0)
        rectangle.set_height(0)
        rectangle.set_visible(False)
        fig.canvas.draw_idle()
        
        
    # Get the coordinates of the mouse click
    start_x = event.xdata
    start_y = event.ydata

    # Create a rectangle object
    rectangle = Rectangle((start_x, start_y), 0, 0, color='#ff8080', alpha=0.4)

    # Add the rectangle to the plot
    ax.add_patch(rectangle)


def on_mouse_move(event):
    global x, y, rectangle
    if event.button == 1:
        # Get the coordinates of the mouse cursor
        x = event.xdata
        y = event.ydata

        # Update the size and position of the rectangle
        rectangle.set_width(x - start_x)
        rectangle.set_height(y - start_y)
        rectangle.set_xy((start_x, start_y))

        # Redraw the plot
        fig.canvas.draw_idle()


    

# def line_select_callback(eclick, erelease):
#     global x1,x2,y1,y2
#     x1, y1 = eclick.xdata, eclick.ydata
#     x2, y2 = erelease.xdata, erelease.ydata
#     print("\n\nx1 = ", x1)
#     print("x2 = ", x2)
#     print("y1 = ", y1)
#     print("y2 = ", y2)
#     return x1,y1,x2,y2




def SaveLinesteps(sub, exam, text, pageno, tempx, tempy):
    # ygazesmedian = calcMedian(tempx, tempy)
    
    f = plt.figure()
    f.set_figwidth(14)
    f.set_figheight(9)
    ax = plt.subplot(1,1,1)
    ax.margins(x=0)
    # plt.subplots_adjust(left = 0.15)
    
    plt.plot(tempx,'yellow')
    if( hardcases ):
        plt.plot(tempy,'bo')
    else:
        plt.plot(tempy,'b')

    pagesfile = open(folder1 + "texts/" + text + textends + "/py/pages/pages.txt", "r")
    pages = pagesfile.read(1)


    plt.title( "Subject: "+ str(sub) + ", Text: " + text + ", Page: " + str(pageno) + " out of " + str(pages) )

    plt.savefig(folder1 + folder2 + 'subject_' + str(sub) + '/all_graphs/' + text + str(exam) + pyimagepath + '/linesteps' + str(pageno) + '.png')
    
    movefigure(f, 3, 10)

    return 


def on_key_press(event, xstart_entry, ystart_entry, xend_entry, yend_entry):
    x1 = rectangle.get_x()
    x2 = rectangle.get_x() + rectangle.get_width()
    y1 = rectangle.get_y()
    y2 = rectangle.get_y() + rectangle.get_height()
    if event.key == 'enter':
        # Enter the click x index into the x_entry entry field
        xstart_entry.delete(0, tk.END)
        xstart_entry.insert(0, str(x1))


        # Enter the click y index into the y_entry entry field
        ystart_entry.delete(0, tk.END)
        ystart_entry.insert(0, str(y1))
    
        # Enter the click x index into the x_entry entry field
        xend_entry.delete(0, tk.END)
        xend_entry.insert(0, str(x2))


        # Enter the click y index into the y_entry entry field
        yend_entry.delete(0, tk.END)
        yend_entry.insert(0, str(y2))





def setmypagecollection(param, paramno):
    global mypagecollection
    mypagecollection[paramno] = param


def getParam(paramname):
    if( paramname == "mypagecollection" ):
        return mypagecollection
    
    elif( paramname == "ax" ):
        return ax
    
    elif( paramname == "fig" ):
        return fig
    
    # elif( paramname == "rect_selector" ):
    #     return rect_selector
    





main1()

