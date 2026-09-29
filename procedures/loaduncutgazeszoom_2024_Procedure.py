

from asyncio.windows_events import NULL
import ctypes
import os
import time
import statistics
from os.path import exists
from tkinter.messagebox import askyesno
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
# from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)


from globalVars import folder1, folder2, textends, pyimagepath, dispersion, dispersion2, guiflag
from gazeshandling import gazeshandling
from colorPicker import colorPicker

from semiauto_or_auto_process.storerawdata import storegazedata, storevergencedata, store_pupil_z_data
from semiauto_or_auto_process.commonfunctions import CutGazes, ShowGazesAndCutGazes, getpagelines

from MakeFixationsFile import MakeFixationsTxt
from MakeGazesFile import MakeGazesTxt
from GetAndDrawROIS import getROIbounds, drawROIbounds
from CutGazesROIs import CutGazesROIs
from creategazedata import CreateGazeData
from drawFixations import drawFixations
from semiauto_or_auto_process.concatdata import concatdata
from storefinalindexes import storefinalindexes
from GazesPreview_hardcases import GazesPreview_hardcases
from movefigure import movefigure
from calculateYline import calculateYline
from loaduncutdata_hardcases import loaduncutdata_hardcases
from fixationfungap import fixationfungap
from drawEyeMovements import drawEyeMovements
from filteredgazes import filteredgazes
from MakeDispersionTxt import MakeDispersionTxt
from  MakePageFixationsGap import MakePageFixationsGap
from Median import Median
from plotoneeye import plot_one_eye
from colorLeftplot import colorLeftplot
from colorRightplot import colorRightplot
from load_subs_initial_data import load_subs_initial_data
from make_textfolder_struct import make_textfolder_struct


def loaduncutgazeszoom_2024_Procedure(subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye):

    # Get Subject's Data from an Input Dialogue  

    global from_runcrashes
    from_runcrashes = False


    # Replace no valid gazes with valid
    global nonvalid2valid
    nonvalid2valid = 0   # 0 for do nothing, 1 for replace
    ###################################
    
    global hardcases_glob
    hardcases_glob = hardcases


    # Orizw se poia exam einai to kathe subject
    exam = 1
    
    
    # Kuria while loop gia na trexoun ola ta subject pou thelw ( trexw 1h loop gia ta subject kai 2h eswterikh loop gia ta texts tou subject )
    for i in range(len(subs)): 
        proceduredone = True

        # load subjects data, i.e if subject exist and which texts has this subject
        gazesfolders, analysis_texts, textanalysisfiles = load_subs_initial_data(subs[i], exam, texts, from_runcrashes)      
        if( gazesfolders == NULL ):
            continue                                

        for j in range (len(analysis_texts)):
            text = analysis_texts[j]
            file = textanalysisfiles[j]
            
            make_textfolder_struct(subs[i], exam, text)
            

            if os.path.exists( folder1 + folder2 + 'subject_' + str(subs[i]) + "/" + file + "/gazes-orignal-1920.txt" ):
                proceduredone = False
                print("\nFound SD gazes file on subject " + str(subs[i]))
                print("Considering changing analysis version or fix the file.")
                print("Do not forget that you also need the SD texts.\n")
                time.sleep(5)
                break
    
            if( (not exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_pass.txt')) and (not exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_crash.txt')) ):
                # Ksekinaei h analysh twn keimenwn 
                proceduredone = False
                Start_Text_Procedure(file, subs[i], exam, text, onlylefteye, onlyrighteye)  # Main procedure of the programme for each text
            
            
            # elif( (bypass==1) and (exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_pass.txt')) ):
            #     # Ksekinaei h analysh twn keimenwn 
            #     os.remove(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_pass.txt')
            #     proceduredone = False
            #     Start_Text_Procedure(file, subs[i], exam, text, onlylefteye, onlyrighteye)  # Main procedure of the programme for each text
            
            elif( bypass == 1 ): # and (exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i]) + '_pass.txt')) ):
                # Ksekinaei h analysh twn keimenwn 
                if exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_pass.txt'):
                    os.remove(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_pass.txt')
                if exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_crash.txt'):
                    os.remove(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_crash.txt')
                
                proceduredone = False
                Start_Text_Procedure(file, subs[i], exam, text, onlylefteye, onlyrighteye)  # Main procedure of the programme for each text
            
            
        
            # Handle some messages
            if(  proceduredone == True and  analysis_texts!=[] ):
                if exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_pass.txt'):
                    print("\nAnalysis has been done for Subject=%d  in text=%s " % (subs[i], text))
                if exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_crash.txt'):
                    print("\nAnalysis has been PARTIALLY done for Subject=%d in text=%s " % (subs[i], text))
                time.sleep(3)
        
        
        
        if( analysis_texts==[] ):
            print("\nΝo texts were found for Subject = %d " % subs[i])
            time.sleep(3)

              
    #Delete unneeded .txts 
    for file in os.listdir():
        if( file.endswith(".txt") ):
            if( os.stat(file).st_size==0 ):
                os.remove(file)




#Procedure's args ={ (text : text i will analyze), (folder : main folder), (sub1 : subject's id), (sub1class : subject's class) }
def Start_Text_Procedure(file, sub1,  exam, text, onlylefteye, onlyrighteye):
    from_runcrashes = False
 
    # gazesfilepath must be like: 
    # '/Radar_Iro_copy/individual/subject_696/ee_696_1_visit_wa_1_5_2021-11-25-03.05.21/gazes.txt'
    # OR
    # '/Radar_Iro_copy/individual/subject_696/ee_696_1_visit_wa_1_5_2021-11-25-03.05.21/gazespy.txt'    
    # the result depends on whether the file Tobii5L.txt exists or not
    newgazes, vergence_list, vergence_z = gazeshandling(file, sub1)

    # # # # # #  Plot eye vergence  # # # # #
    # if( vergence != NULL ):
    #     ploteyevergence(sub1, text, textends, 1, exam, vergence)


    # Load Gazes Data 
    uncutgazes_raw, uncutgazes, negativecheck, oneeyeindexes = loaduncutdata_hardcases(text, exam, file, sub1, onlylefteye, onlyrighteye)


    ### Convert non-valid gazes to valid from filtered gazes #########
    if( nonvalid2valid > 0 ):
        print("Attention: Convert non-valid to valid from filtered gazes")
        uncutgazes = filteredgazes(sub1, exam, text, file, uncutgazes)
        gazesfiltereannot = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/_nonvalid2valid.txt' 
        file2 = open(gazesfiltereannot, 'w')
        file2.close()
    ### End of --Convert non-valid gazes to valid from filtered gazes-- ##########


    index, x, y, timestamp, roi, validity, vergence, pupilsize = uncutgazes[0], uncutgazes[1], uncutgazes[2], uncutgazes[3], uncutgazes[4], uncutgazes[5], uncutgazes[6], uncutgazes[7]
    
    
    #Temporary lists that will save the cutgazes data per page
    pageno = -1             #page number, assumption pageno=-1
    tempindex = []          
    #temporary index list
    tempx = []              #temporary x list
    tempy = []              #temporary y list
    temptimestamp = []      #temporary timestamp list
    temproi = []
    tempvalidity = []
    tempvergence = []
    temppupilsize = []
    tempnegativecheck = []
    temponlylefteye = [[], []]
    temponlyrighteye = [[], []]

    i=-1

    #Μεχρι να φτασω στο τελος του αρχειου cutgazes.txt θα μπαινω να κανω την αναλυση
    #δηλαδη γεμιζω προσωρινες λιστες με τα data ανα σελιδα(index, x, y, timestamp)
    #και δημιουργω τα αρχεια fixations.txt , cutgazes.txt ,
    #κανω τα plot που χρειαζομαι και βρισκω fixations και rois οπου χρειαζεται
    while( i<len(index) ):
        i+=1
        if(  ( i<len(index) and index[i] == 1 )  or  ( i == len(index) )  ):
            pageno+=1

            if(pageno>0) :
                lines = getpagelines(text, pageno)                 # Βρισκω ποσες γραμμες εχει η σελιδα οπου βρισκομαι
                roibounds = getROIbounds(text, pageno)             # Βρισκω τα ROIbounds του κειμενου

                roistartpath = folder1 + 'texts/' + text + textends + '/py/mytext/page(' + str(pageno) + ')/ROIstart/ROIstart.xlsx'
                roistart = pd.read_excel(roistartpath, header=None).values[0][0]
                
                print("\nsubject %d, text %s, page %d " %(sub1, text, pageno))          #Βρισκω τα ROIbounds του κειμενου

            if( len(tempindex) != 0 ):                  #Οταν φτασω στο τελος της 1ης σελιδας και εχω συλλεξει τα δεδομενα μου                                                               
                
                mypagecollection = [tempindex, tempx, tempy, temptimestamp, temproi, tempvalidity, tempvergence, temppupilsize, tempnegativecheck, temponlylefteye, temponlyrighteye]

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

                
                # # Start Cuts Process 
                
                finalindexes, cgdata, f = CutsProcedure(sub1, exam, text, pageno, lines, roibounds, roistart, mypagecollection)
    
                answer = confirm()         #Ελεγχω εαν δεχομαι τα κοψιματα που εκανα
                
                while( answer == False ):  #Εαν η απαντηση ειναι 'οχι' τοτε ξανακανω την προηγουμενη διαδικασια
                    plt.close('all')
                    
                    # # Start Cuts Process 
                    finalindexes, cgdata, f = CutsProcedure(sub1, exam, text, pageno, lines, roibounds, roistart, mypagecollection)
                
                    answer = confirm()         #Ελεγχω εαν δεχομαι τα κοψιματα που εκανα
                 
                    
                if(answer == True ):    #Εαν η απαντηση ειναι 'ναι' (οτι δεχομαι δηλαδη τα κοψιματα που εκανα) τοτε φτιαχνω τις εικονες των cutgazes(page_number).png και κλεινω το τρεχον window 
                    f.set_size_inches(9.115, 6.833)
                    drawROIbounds(sub1, exam, text, pageno, roibounds, cgdata[1], cgdata[2], "rawgazes", [], plt, "close") #In order to draw and save the rawgazes(pageno).png images

                    plt.close()
                    window.destroy()
                
                
                window.mainloop()



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
            
            tempnegativecheck = []
            
            temponlylefteye = [[], []]
            temponlyrighteye = [[], []]

            
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
            tempnegativecheck.append( negativecheck[i] )
            temponlylefteye[0].append( oneeyeindexes[0][i] )
            temponlylefteye[1].append( oneeyeindexes[1][i] )
            temponlyrighteye[0].append( oneeyeindexes[2][i] )
            temponlyrighteye[1].append( oneeyeindexes[3][i] )


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
    



def CutsProcedure(sub1, exam, text, pageno, lines, roibounds, roistart, mypagecollection):
    tempx, tempy, negativecheck, onlylefteye, onlyrighteye = mypagecollection[1], mypagecollection[2], mypagecollection[8], mypagecollection[9], mypagecollection[10]
    
    # negativetempx = []
    negativetempy = []
    # for i in range(len(tempy)):
    #     if(negativecheck[i]==1):
    #         # negativetempx.append(tempx[i])
    #         negativetempy.append(tempy[i])
    #     else:
    #         # negativetempx.append(None)
    #         negativetempy.append(None)
                    
    # negativetemppoints = [negativetempx, negativetempy]
    

    # # # # # Cuts and Check of Cuts
    global g_ax, g

    g, g_ax = GazesPreview_hardcases(text, pageno, mypagecollection)  # preview
    finalindexes = ShowGazesMakeCuts_load(sub1, exam, text, pageno, lines, tempx, tempy, negativetempy)    # Make Cuts
    cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color = 'r', linewidth = 1)
    plot_one_eye(sub1, exam, text, pageno, onlylefteye, "Left Eye", [1410, 437])
    plot_one_eye(sub1, exam, text, pageno, onlyrighteye, "Right Eye", [1410, 715])
    plt.show()
    existNone, ascendingcuts = checkCuts(finalindexes)    # Check if cuts are correct
    # # # # End of Cuts
    

    while( (len(finalindexes)!=lines+1) or (existNone==True) or (ascendingcuts==False) ):
        print("\n")
        if( len(finalindexes)!=lines+1 ):
            print("--Wrong Cut. You made only %d cuts.You need %d more." %(len(finalindexes), lines+1 - len(finalindexes)))
        
        if( existNone==True ):
            print("--Wrong cut. You click out of the box.")
        
        if( existNone==False and ascendingcuts==False ):
            print("--Wrong cut. You make a backward cut.")

        print("Indexes = ", indexes)
        ctypes.windll.user32.MessageBoxW(0, "You need to do it again!", "Warning!", 16)

        # # # # # Cuts and Check of Cuts
        g, g_ax = GazesPreview_hardcases(text, pageno, mypagecollection)
        finalindexes = ShowGazesMakeCuts_load(sub1, exam, text, pageno, lines, tempx, tempy, negativetempy) 
        cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color = 'r', linewidth = 1)
        plot_one_eye(sub1, exam, text, pageno, onlylefteye, "Left Eye", [1410, 437])
        plot_one_eye(sub1, exam, text, pageno, onlyrighteye, "Right Eye", [1410, 715])
        plt.show()
        existNone, ascendingcuts = checkCuts(finalindexes)
        # # # # # 


    print("x = ", finalindexes)
    
    cgdata =  CutGazes(text, pageno, roibounds, roistart, mypagecollection)               #Φτιαχνω τις λιστες με τα cutgazes(index, x, y, timestamp)

    
    # Φτιαχνω το γραφημα των Gazes & Cutgazes
    global window
    flag = -1
    f, window = ShowGazesAndCutGazes(text, pageno, tempx, tempy, cgdata[1], cgdata[2], flag)             
           
    
    return finalindexes, cgdata, f



        
#Φτιαχνω το γραφημα με τα Gazes
#args = { (sub1 : subject's id), (text : analysis text), (pageno : page number), (lines : total page lines), (tempx : list with X coords that have occur from my cut), (tempy : list with Y coords that have occur from my cut) }
def ShowGazesMakeCuts_load(sub1, exam, text, pageno, lines, tempx, tempy, negativetempy):
    global indexes, plines, linecuts, f, ax, ymin, gtempx, gtempy, gmin_xlim, gmax_xlim, gmin_ylim, gmax_ylim     #i made this global in order to use them some code below { (indexes : list with Index coords that have occur from my cut), (plines : page lines) }
    indexes, plines =  [], lines
    gtempx, gtempy = tempx, tempy
    
    
    # ygazesmedian = calcMedian(tempx, tempy)
    
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
        plt.plot(tempy,'b', markersize=1)
        
    # plt.plot(negativetempy, 'ro', markersize=1)
    # plt.plot(ygazesmedian, 'r')
    
    ylim = ax.get_ylim()
    gmin_ylim = ylim[0]
    gmax_ylim = ylim[1]

    xlim = ax.get_xlim()
    gmin_xlim = xlim[0]
    gmax_xlim = xlim[1]


    pagesfile = open(folder1 + "texts/" + text + textends + "/py/pages/pages.txt", "r")
    pages = pagesfile.read()

    yrange = ax.get_ylim()
    ymin = yrange[0]
    ymax = yrange[1]

    plt.title( "Subject: "+ str(sub1) + ", Text: " + text + ", Page: " + str(pageno) + " out of " + str(pages) + ", Lines: " + str(lines) )

    plt.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/linesteps' + str(pageno) + '.png')
    
    # linecuts, = ax.plot([], [], ls="None", linewidth=0, marker="o", color=(255/255, 31/255, 255/255), markersize=10, alpha=.5, markeredgewidth=2)
    linecuts = []
    
    # cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='r', linewidth=1 )
    
    f.canvas.mpl_connect('button_press_event' , onclick1)
    movefigure(f, 3, 10)


    # # # radio buttons
    # global radio, plot_states
    # global rax
    
    # plot_states = ["bo"]
    
    # axcolor = "lavenderblush"          # 'lightgoldenrodyellow'
    # rax = plt.axes([0, 0.84, 0.11, 0.14],  # 0: specific index of box in x-axis,   # 0.7: specific index of box in y-axis,   # 0.12: width of box,   # 0: height of box
    #             facecolor=axcolor)
    
    # radio = RadioButtons(rax, ['bo', 'b', 'show median', "show yellow", "hide yellow", "hide median"],
    #                     [True,False,False,False, False, False, False],
    #                     activecolor='r')
    
    # for r in radio.labels: r.set_fontsize(10)
    
    # # rax.axis('off')
    

    # radio.on_clicked(set_plot_state)
    # # # 
 
    return indexes

    



def checkCuts(finalindexes):
    existNone = False
    ascendingcuts = False


    # # check if user has an out of the box cut, i.e None cut
    if(None in finalindexes):
        existNone = True
    else:
        existNone = False
    

    # # check if user has a backward cut
    if( existNone==False ):
        if( finalindexes==sorted(finalindexes) ):
            ascendingcuts = True
        else:
            ascendingcuts = False

    return existNone, ascendingcuts




#Φτιαχνω και Επιστρεφω τις λιστες με τα cutgazes(index, x, y, timestamp roi)
#args = { (text : text), (pageno : page_number), (tindex : temporary index list), (tx : temporary x list), (ty : temporary y list), (ttimestamp : temporary timestamp list) }\
#variables = { (cgi : cutgazes index list), (cgx : cutgazes x list), (cgy : cutgazes y list), (cgtimestamp : cutgazes timestamp list), (cgroi : cutgazes rois list), (start : index of first cut), (stop : index of last cut) }
def CutGazes(text, pageno, roibounds, roistart, mypagecollection):
    tindex, tx, ty, ttimestamp, tvalidity, tvergence, tpupilsize = mypagecollection[0], mypagecollection[1], mypagecollection[2], mypagecollection[3], mypagecollection[5], mypagecollection[6], mypagecollection[7]

    # Make data initializations
    global cgi, cgx ,cgy, cgtimestamp, cgroi, cgvalidity, cgvergence, cgpupilsize
    cgi, cgx, cgy, cgtimestamp, cgroi, cgvalidity, cgvergence, cgpupilsize = [], [], [], [], [], [], [], []

    start = int( indexes[0] )
    stop = int( indexes[-1] )

    #Εδω θα φτιαξω τις cgi, cgx, cgtimestamp
    for i in range( start , stop ):
        cgi.append( tindex[i] )
        cgx.append( tx[i] )
        cgtimestamp.append( ttimestamp[i] )
        cgvalidity.append( tvalidity[i] )
        cgvergence.append( tvergence[i] )
        cgpupilsize.append( tpupilsize[i] )


    #Εδω θα φτιαξω την cgy με τα shift
    yline = calculateYline(text, pageno)
    for i in range(len(indexes)-1):
        start = int( indexes[i] )
        stop = int( indexes[i+1] )
        tempcgy = []
        for j in range(start, stop):
            tempcgy.append(ty[j])  #tempcgy : λιστα που περιεχει τα cutgazes y χωρις το shift
        

        nonzerostempcgy = [nonzerocgy for nonzerocgy in tempcgy if nonzerocgy!=-1] # to nonzerocgy y exei ola ta gazes kai ta valid kai ta nonvalid. Gia na ipologisw omws th median ta -1 mou einaio axrista kai ta petaw.
        ymedian = Median(nonzerostempcgy, 0)


        #Εδω φτιαχνω τη λιστα οπου περιχει τα cutgazes y με το shift
        for j in range(start, stop): 
            cgy.append( ty[j] + (yline[i]-ymedian) + 1 )


    cgroi = CutGazesROIs(roibounds, roistart, cgx, cgy)  #Και αυτη η συναρτηση θα μου φτιαξει τη λιστα με τα rois των cutgazes 
    
    return cgi, cgx, cgy, cgtimestamp, cgroi, cgvalidity, cgvergence, cgpupilsize




# def set_plot_state(labels):
#     global yellow_plot, ymedian
    
#     if( labels=="bo" ):
#         ax.cla()
#         ax.plot(gtempy,'bo', markersize=1)
#         ax.set_ylim(gmin_ylim, gmax_ylim)
#         ax.set_xlim(gmin_xlim, gmax_xlim)
       
        
#     if( labels=="b" ):
#         ax.cla()
#         ax.plot(gtempy,'b')
#         ax.set_ylim(gmin_ylim, gmax_ylim)
#         ax.set_xlim(gmin_xlim, gmax_xlim) 

    
    
#     if( labels=="show median" ):
#         ygazesmedian = calcMedian(gtempx, gtempy)
#         ymedian = ax.plot(ygazesmedian, 'r')   
    
    
#     if( labels=="show yellow" ):
#         bo_indexappear = max([index for index, item in enumerate(plot_states) if item == "bo"], default=-1)
#         b_indexappear = max([index for index, item in enumerate(plot_states) if item == "b"], default=-1)
#         print("bo_indexappear = ", bo_indexappear)
#         print("b_indexappear = ", b_indexappear)
        
#         yellow_plot = ax.plot(gtempx,'yellow')

#         if(bo_indexappear > b_indexappear):
#             ax.plot(gtempy,'bo', markersize=1) 
#         else:
#             ax.plot(gtempy,'b')
            
    
#     if( labels=="hide yellow" ):
#         if(len(yellow_plot)>0):
#             line = yellow_plot.pop(0)
#             line.remove()
#         else:
#             return
  

#     if( labels=="hide median" ):
#         try:
#             line = ymedian.pop(0)
#             line.remove()  
#         except NameError:
#             return
    
#     plot_states.append(radio.value_selected)
    
#     f.canvas.draw()
        



#CLICK AND OTHER EVENTS


#Η συναρτηση αυτη αποθηκευει σε καθε κλικ τα indexes και οταν κανω τον αριθμο των κοψιματων που πρεπει κλεινει το παραθυρο με τα κοψιματα
def onclick1(event):
    global length, mycolor, gevent
    gevent = event
    
    
    # # # Check in which plot I click (because in left plot there is also the box option in left corner and i want to avoid troubles due to click event in this plot)
    if(event.inaxes==ax):
        indexes.append(int(event.xdata))  #σε καθε κλικ αποθηκευει τα στοιχεια που βρισκονται στον αξονα των x, δηλαδη τα indexes των gazes
    
        length = len(indexes)

        mycolor = colorPicker(indexes, plines)
        
        colorPointCutsLeftPlot(event)   # color the fuchsia dots?(i.e the clicks for cut process I have made) in left plot
        
        from_multilines = False
        colorLeftplot(event, indexes, plines, gtempy, hardcases_glob, mycolor, f, ax, gmin_ylim, gmax_ylim, gmin_xlim, gmax_xlim, from_multilines)
        colorRightplot(event, indexes, plines, gtempx, gtempy, g, g_ax, mycolor, from_multilines)          # color right plot
        
        
        # # # Remove choices window when I start clicks
        # if( len(indexes) == 1 ):
        #     rax.remove()
            # rax.cla()
            # rax.axis('off')
            # rax.set_facecolor("white")
        # # #
    
    # # #
 

    # # # --Pause-- plot to see the final cut and --Close-- all plots after that
    if( len(indexes) == plines+1):
        plt.pause(1)
        plt.close('all')
    # # #
    
    return


        

def colorPointCutsLeftPlot(event):
    # # # # # # # # # # #   Color the Fuchsia Dots in Left Plot / Color the clicks I have made   # # # # # # # # # # # # # # #
    
    # # # diadikasia pou zografizei me kiklo se xroma magenta to shmeio sto opoio ekopsa 
    yvalue = 0
    # if( gmin_ylim >= 0 ):
    yvalue = gmin_ylim + 30
    yvals = [yvalue for d in range(len(indexes))]
    
    linecuts.append(event.xdata)

    ax.scatter(linecuts, yvals, s=150, facecolors="fuchsia", alpha=.5)

    # linecuts.set_xdata(indexes)
    # linecuts.set_ydata(yvals)
    # linecuts.set_data(indexes, yvals)
    
    f.canvas.draw_idle() 
    # # # # # # # #
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    return




#Δημιουργει ενα dialogue με το χρηστη για το αν δεχεται τα κοψιματα που εκανε ή οχι
def confirm():
    answer = askyesno(title='confirmation',
                    message='Accept Line Cuts?')
    
    if (answer==False):
        window.destroy()
        plt.close()
        
    return answer







