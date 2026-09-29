
from asyncio.windows_events import NULL
import ctypes
import os
import time
import shutil
import statistics
from os.path import exists
import tkinter as tk
from pylab import *
from tkinter.messagebox import askyesno
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)


from globalVars import folder1, folder2, textends, pyimagepath, dispersion, dispersion2, guiflag
from basic_function_gui import basic_function_gui
from GetSomeInitialData import createextra, getGazesFolderbyText, getGazesFoldersandClass
from createSubfile import createSubfile
from gazeshandling import gazeshandling
from makenoshift import makenoshift
from semiauto_or_auto_process.storerawdata import storegazedata, storevergencedata, store_pupil_z_data
from semiauto_or_auto_process.commonfunctions import CutGazes, ShowGazesAndCutGazes, getpagelines
from MakeFixationsFile import MakeFixationsTxt
from MakeGazesFile import MakeGazesTxt
from GetAndDrawROIS import getROIbounds, drawROIbounds
from creategazedata import CreateGazeData
from drawFixations import drawFixations
from fixationfungap import fixationfungap
from semiauto_or_auto_process.concatdata import concatdata
from storefinalindexes import storefinalindexes
from selectROIS_multilines import selectROIS
from findroisposition import findroisposition
from movefigure import movefigure
from GazesPreview import GazesPreview
from first_clarification import first_clarification
from calculateYline import calculateYline
from CutGazesROIs import CutGazesROIs
from nextLine import nextLine
from chosenrois import chosenrois
from find_y_fromhist import find_y_fromhist
from loaduncutdata import loaduncutdata
from drawEyeMovements import drawEyeMovements
from filteredgazes import filteredgazes
from MakeDispersionTxt import MakeDispersionTxt
from MakePageFixationsGap import MakePageFixationsGap
from plotoneeye import plot_one_eye
from colorPicker import colorPicker
from colorLeftplot import colorLeftplot
from colorRightplot import colorRightplot
from load_subs_initial_data import load_subs_initial_data
from make_textfolder_struct import make_textfolder_struct


def loaduncutgazeszoom_multilines_rois_2024_Procedure(subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye):

    # Get Subject's Data from an Input Dialogue  

    """
    dial = Dialogue()
    dial.mainloop()

    name = dial.inputDialog[0]
    sub1 = int(dial.inputDialog[1])
    texts = dial.get_text()
    print(texts)
    """
    global from_runcrashes
    from_runcrashes = False
   

    # Replace no valid gazes with valid
    global nonvalid2valid
    nonvalid2valid = 0      # 0 for do nothing, 1 for replace
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
            
            # Make the folders (if not exist) that i will use to store graphs and data for my texts
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
    
    global roibounds
 
    # gazesfilepath must be like: 
    # '/Radar_Iro_copy/individual/subject_696/ee_696_1_visit_wa_1_5_2021-11-25-03.05.21/gazes.txt'
    # OR
    # '/Radar_Iro_copy/individual/subject_696/ee_696_1_visit_wa_1_5_2021-11-25-03.05.21/gazespy.txt'    
    # the result depends on whether the file Tobii5L.txt exists or not
    newgazes, vergence_list, vergence_z = gazeshandling(file, sub1)  # to orisma newgazes den xrhsimopoieitai

    # # # # # #  Plot eye vergence  # # # # #
    # if( vergence != NULL ):
    #     ploteyevergence(sub1, text, textends, 1, exam, vergence)

    
    # Load Gazes Data 
    uncutgazes_raw, uncutgazes, oneeyeindexes = loaduncutdata(text, exam, file, sub1, onlylefteye, onlyrighteye)

    ### Convert non-valid gazes to valid from filtered gazes #########
    if( nonvalid2valid > 0 ):
        print("Attention: Convert non-valid to valid from filtered gazes")
        uncutgazes = filteredgazes(sub1, exam, text, file, uncutgazes)
        gazesfiltereannot = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/_nonvalid2valid.txt' 
        file2 = open(gazesfiltereannot, 'w')
        file2.close()
    
    ### Convert non-valid gazes to valid from filtered gazes ##########
    index, x, y, timestamp, roi, validity, vergence, pupilsize = uncutgazes[0], uncutgazes[1], uncutgazes[2], uncutgazes[3], uncutgazes[4], uncutgazes[5], uncutgazes[6], uncutgazes[7]
    

    
    #Temporary lists that will save the cutgazes data per page
    pageno = -1             #page number, assumption pageno=-1
    tempindex = []          #temporary index list
    tempx = []              #temporary x list
    tempy = []              #temporary y list
    temptimestamp = []      #temporary timestamp list
    temproi = []
    tempvalidity = []
    tempvergence = []
    temppupilsize = []
    temponlylefteye = [[], []]
    temponlyrighteye = [[], []]
    

    i=-1

    roiselectedpath = folder1 + folder2 + 'subject_' + str(sub1) + '/' + file + '/finalROISselected_multilines.txt'
    roiselectedtxt = open(roiselectedpath, 'w')


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
                
                mypagecollection = [tempindex, tempx, tempy, temptimestamp, temproi, tempvalidity, tempvergence, temppupilsize, temponlylefteye, temponlyrighteye]

                # # # # # # # # # Store gazedata per page, i.e gazes_page1.txt, gazes_page2.txt, gazes_page3.txt, .....  # # # # # # # # #
                gazedatatxt = folder1 + folder2 + '/subject_' + str(sub1) + '/' + file + '/py/gazes_page' + str(pageno) + '.txt'
                gazedatafile = open(gazedatatxt, 'w')
                gazedatafile.close()
                storegazedata(gazedatatxt, mypagecollection)


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


                # # # # # Start Level Defining Process
                global ylinesin
                print("\nDefine Line Levels")
                g, g_ax = GazesPreview(text, pageno, mypagecollection)
                ylinesin = CutLevels(sub1, exam, text, pageno, lines, mypagecollection)
                print("ylinesin = ", ylinesin)
                acceptlevels = cutLevelscheck()
                print()

                while( acceptlevels == False ):
                    print("\nDefine Line Levels")
                    g, g_ax = GazesPreview(text, pageno, mypagecollection)
                    ylinesin = CutLevels(sub1, exam, text, pageno, lines, mypagecollection)
                    print("ylinesin = ", ylinesin)
                    acceptlevels = cutLevelscheck()
                    print()
                # # # # # End of Level Defining Process
                

                
                # # Start Gazes Cut Process
                finalindexes, shifted_list, finalselectedrois, noshifted_list = GazesCutMain(sub1, exam, text, pageno, file, lines, roistart, roiselectedpath, mypagecollection)
                
                # # End Gazes Cut Process


                window1.mainloop()

    

                gazedata = CreateGazeData(shifted_list)


                if( noshifted_list != [] ):
                    #Make noshifts.txt file
                    noshifttxt = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/noshifted' + str(pageno) + '.txt'
                    noshiftfile = open(noshifttxt,"w")
                    noshiftfile.close()
                    makenoshift(noshifttxt, noshifted_list)

                    l1 = shifted_list[0]+noshifted_list[0]
                    l2 = shifted_list[1]+noshifted_list[1]
                    l3 = shifted_list[2]+noshifted_list[2]
                    l4 = shifted_list[3]+noshifted_list[3]
                    l5 = shifted_list[4]+noshifted_list[4]
                    l6 = shifted_list[5]+noshifted_list[5]
                    l7 = shifted_list[6]+noshifted_list[6]
                    l8 = shifted_list[7]+noshifted_list[7]
                    
                    gazedata = CreateGazeData([l1, l2, l3, l4, l5, l6, l7, l8])


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
                drawROIbounds(sub1, exam, text, pageno, roibounds, shifted_list[1], shifted_list[2], "cutgazes", fixationdatagap, NULL, "close") 

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
    




def gazesloop(sub1, exam, text, pageno, lines, roistart, mypagecollection):
    # # # # # Start Cuts Process 
    global G, G_ax
    G, G_ax = GazesPreview(text, pageno, mypagecollection)
    finalindexes, cgdata, f, firstchosenline, noshifted_y = CutsProcedure(sub1, exam, text, pageno, lines, roistart, mypagecollection)
    

    return finalindexes, cgdata, f, firstchosenline, noshifted_y


def shiftemProced(sub1, exam, text, pageno, tempx, tempy, roistart, firstchosenline, lines, cgdata, noshifted_y):
    # # Start Shift by Line Procedure  
    lastlinewords_data = pd.read_excel( folder1 + 'texts/'+ text + textends + '/py/mytext/lastlinewords/lastlinewords(' + str(pageno) + ').xlsx', header=None)
    lastlinewords = lastlinewords_data.iloc[:,0]
    lastlinewords = lastlinewords.to_list()
    # print("LASTLINEWORDS = ", lastlinewords)
    
    shiftedLines = [firstchosenline]
    chosenroislist = chosenrois(firstchosenline, lastlinewords)
    # print("SHIFTEDLINES = ", shiftedLines)
    # print("CHOSENROIS = ", chosenroislist)
    
    shifted_list, noshifted_list = first_clarification(cgdata, noshifted_y, chosenroislist)
    shifted_i, shifted_x, shifted_y, shifted_timestamp, shifted_validity, shifted_vergence, shifted_pupilsize = shifted_list[0], shifted_list[1], shifted_list[2], shifted_list[3], shifted_list[4], shifted_list[5],shifted_list[6]
    noshifted_cgi, noshifted_cgx, noshifted_raw_y, noshifted_cgtimestamp, noshifted_cgroi, noshifted_cgvalidity, noshifted_cgvergence, noshifted_cgpupilsize = noshifted_list[0], noshifted_list[1], noshifted_list[2], noshifted_list[3], noshifted_list[4], noshifted_list[5], noshifted_list[6], noshifted_list[7]
    

    # Start Line by Line Shift Process
    for runtime in range( lines - 1 ):
        nextchosenline, chosenlist, nochosenlist = nextLine(text, pageno, noshifted_list, shiftedLines, lastlinewords, roistart, roibounds, ylinesin)
        chosen_i = chosenlist[0]
        chosen_x = chosenlist[1]
        chosen_y = chosenlist[2]
        chosen_timestamp = chosenlist[3]
        chosen_validity = chosenlist[4]
        chosen_vergence = chosenlist[5]
        chosen_pupilsize = chosenlist[6]
        
        shifted_i += chosen_i
        shifted_x += chosen_x
        shifted_y += chosen_y
        shifted_timestamp += chosen_timestamp
        shifted_validity += chosen_validity
        shifted_vergence += chosen_vergence
        shifted_pupilsize += chosen_pupilsize

        noshifted_cgi = nochosenlist[0]
        noshifted_cgx = nochosenlist[1]
        noshifted_raw_y = nochosenlist[2]
        noshifted_cgtimestamp = nochosenlist[3]
        noshifted_cgroi = nochosenlist[4]
        noshifted_cgvalidity = nochosenlist[5]
        noshifted_cgvergence = nochosenlist[6]
        noshifted_cgpupilsize = nochosenlist[7]

        noshifted_list = [ noshifted_cgi, noshifted_cgx, noshifted_raw_y, noshifted_cgtimestamp, noshifted_cgroi, noshifted_cgvalidity, noshifted_cgvergence, noshifted_cgpupilsize ]
        
        shiftedLines.append(nextchosenline)
    
    # # End Shift Line by Line Process

    
    shifted_roi = CutGazesROIs(roibounds, roistart, shifted_x, shifted_y)
    f = ShowGazesAndCutGazesSecond(sub1, exam, text, pageno, tempx, tempy, shifted_x, shifted_y)
    
    shifted_list = [shifted_i, shifted_x, shifted_y, shifted_timestamp, shifted_roi, shifted_validity, shifted_vergence, shifted_pupilsize]
    noshifted_list = [noshifted_cgi, noshifted_cgx, noshifted_raw_y, noshifted_cgtimestamp, noshifted_cgroi, noshifted_cgvalidity, noshifted_cgvergence, noshifted_cgpupilsize]

    return shifted_list, noshifted_list



def roismain(sub1, exam, text, pageno, file, roibounds, tempx, tempy, shifted_x, shifted_y, answer2, roiselectedpath):
    finalselectedrois = []
    if( answer2 == True):
        selectedrois = selectROIS(sub1, exam, text, pageno, file, roibounds, tempx, tempy, shifted_x, shifted_y)
        finalselectedrois = selectedrois

        with open(roiselectedpath, 'a') as roifile:
            roifile.write('\n'.join(str(roi) for roi in selectedrois))
            roifile.write("\n")
        

    else:
        positionprevroi = findroisposition(text, pageno)
        xroi = len( roibounds[0] )
        allrois = [i for i in range(positionprevroi + 1, positionprevroi + xroi + 1)]
        finalselectedrois = allrois

        with open(roiselectedpath, 'a') as roifile:
            roifile.write('\n'.join(str(roi) for roi in allrois))
            roifile.write("\n")
    
    return finalselectedrois



def GazesCutMain(sub1, exam, text, pageno, file, lines, roistart, roiselectedpath, mypagecollection):
    tempx = mypagecollection[1]
    tempy = mypagecollection[2]

    finalindexes, cgdata, f, firstchosenline, noshifted_y = gazesloop(sub1, exam, text, pageno, lines, roistart, mypagecollection)
    answer1 = confirmation_box1("Shift'em")         #Ελεγχω εαν δεχομαι τα κοψιματα που εκανα


    while( answer1 == 'No' ):  #Εαν η απαντηση ειναι 'οχι' τοτε ξανακανω την προηγουμενη διαδικασια
        plt.close()
        finalindexes, cgdata, f, firstchosenline, noshifted_y = gazesloop(sub1, exam, text, pageno, lines, roistart, mypagecollection)
        answer1 = confirmation_box1("Shift'em")
        

    if(answer1 == 'Yes' ):    #Εαν η απαντηση ειναι 'ναι' (οτι δεχομαι δηλαδη τα κοψιματα που εκανα) τοτε φτιαχνω τις εικονες των cutgazes(page_number).png και κλεινω το τρεχον window 

        # Temporary disable the question for ROI selection
        # until it is trylly needed.
        answer2 = False
        # answer2 = cutROIScheck()  # uncomment this line if you want the question for ROI selection
        
        plt.close()
        
        finalselectedrois = roismain(sub1, exam, text, pageno, file, roibounds, tempx, tempy, cgx, cgy, answer2, roiselectedpath)

        return finalindexes, cgdata, finalselectedrois, []
    

    if(answer1 == "Shift'em" ):
        
        shifted_list, noshifted_list = shiftemProced(sub1, exam, text, pageno, tempx, tempy, roistart, firstchosenline, lines, cgdata, noshifted_y)

        # Temporary disable the question for ROI selection
        # until it is trylly needed.
        answer2 = False
        # answer2 = cutROIScheck()  # uncomment this line if you want the question for ROI selection

        plt.close('all')
        
        window2.destroy()
        window2.quit()

        shifted_x = shifted_list[1]
        shifted_y = shifted_list[2]
        finalselectedrois = roismain(sub1, exam, text, pageno, file, roibounds, tempx, tempy, shifted_x, shifted_y, answer2, roiselectedpath)

    
    return finalindexes, shifted_list, finalselectedrois, noshifted_list
        



def close_figure_enter(event):
    if( event.key == 'enter' ):
        # plt.close(event.canvas.figure)
        plt.close('all')



#Φτιαχνω το γραφημα με τα Gazes
#args = { (sub1 : subject's id), (text : analysis text), (pageno : page number), (lines : total page lines), (tempx : list with X coords that have occur from my cut), (tempy : list with Y coords that have occur from my cut) }
def ShowGazesMakeCuts(sub1, exam, text, pageno, lines, tempx, tempy):
    global indexes, plines, linecuts, f, ax1, xmin, xmax, ymin, ymax, gtempx, gtempy      #i made this global in order to use them some code below { (indexes : list with Index coords that have occur from my cut), (plines : page lines) }
    indexes, plines, gtempx, gtempy =  [], lines, tempx, tempy

    
    f = plt.figure()
    f.set_figwidth(14)
    f.set_figheight(9)
    ax1 = plt.subplot(1,1,1)
    movefigure(f, 3, 10)
    ax1.margins(x=0)
    
    plt.plot(tempx,'yellow')
    if( hardcases_glob ):
        plt.plot(tempy,'bo', markersize=1)
    else:
        plt.plot(tempy,'b')

    pagesfile = open(folder1 + "texts/" + text + textends + "/py/pages/pages.txt", "r")
    pages = pagesfile.read()



    ax1.set_title( 'Click to set the START and END of each line consecutively. When finished press ENTER\n' + "Subject: "+ str(sub1) + ", Text: " + text + ", Page: " + str(pageno) + " out of " + str(pages) + ", Lines: " + str(lines) )
    
    cursor = Cursor( ax1, horizOn=True, vertOn=True, useblit=True, color='r', linewidth=1 )
    
    extent = ax1.get_window_extent().transformed(f.dpi_scale_trans.inverted())
    f.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/linesteps' + str(pageno) + '.png')

    linecuts, = ax1.plot([], [], ls="None", linewidth=0, marker="o", color=(255/255, 31/255, 255/255), markersize=10, alpha=.5, markeredgewidth=2)


    xrange = ax1.get_xlim()
    xmin = xrange[0]
    xmax = xrange[1]
    
    yrange = ax1.get_ylim()
    ymin = yrange[0]
    ymax = yrange[1]
    
    f.canvas.mpl_connect('button_press_event' , onclick1)
    f.canvas.mpl_connect('key_press_event', close_figure_enter)
    # plt.gcf().canvas.mpl_connect('key_press_event', close_figure_enter)

    plt.show()
 
    return indexes



def ShowGazesMakeLevelCuts(sub1, exam, text, pageno, lines, tempx, tempy):
    global levels, plines      #i made this global in order to use them some code below { (indexes : list with Index coords that have occur from my cut), (plines : page lines) }
    levels, plines =  [], lines

    f = plt.figure()
    f.set_figwidth(14)
    f.set_figheight(9)
    ax = plt.subplot(1,1,1)
    movefigure(f, 3, 10)

    ax.margins(x=0.002)
    plt.plot(tempx,'#66E9B9')
    plt.plot(tempy,'#E240C7')

    pagesfile = open(folder1 + "texts/" + text + textends + "/py/pages/pages.txt", "r")
    pages = pagesfile.read(1)

    plt.title( "Click to set the level of  each successive line\n" + "Subject: "+ str(sub1) + ", Text: " + text + ", Page: " + str(pageno) + " out of " + str(pages) + ", Lines: " + str(lines) )
    
    # cursor = Cursor( ax, horizOn=True, vertOn=True, useblit=True, color='r', linewidth=1 )
    
    f.canvas.mpl_connect('button_press_event' , onclick2)


    # plt.show()
 
    return levels, ax



#Φτιαχνω και Επιστρεφω τις λιστες με τα cutgazes(index, x, y, timestamp roi)
#args = { (text : text), (pageno : page_number), (tindex : temporary index list), (tx : temporary x list), (ty : temporary y list), (ttimestamp : temporary timestamp list) }\
#variables = { (cgi : cutgazes index list), (cgx : cutgazes x list), (cgy : cutgazes y list), (cgtimestamp : cutgazes timestamp list), (cgroi : cutgazes rois list), (start : index of first cut), (stop : index of last cut) }
def CutGazes(text, pageno, roistart, mypagecollection):
    #Make data initializations
    global cgi, cgx ,cgy, cgtimestamp, cgroi, cgvalidity, cgvergence, cgpupilsize, noshifted_y
    cgi, cgx, cgy, cgtimestamp, cgroi, cgvalidity, cgvergence, cgpupilsize, noshifted_y = [], [], [], [], [], [], [], [], []



    start = int( indexes[0] )
    stop = int( indexes[-1] )

    #Εδω θα φτιαξω τις cgi, cgx, cgtimestamp
    for i in range( start , stop):
        cgi.append(mypagecollection[0][i])
        cgx.append(mypagecollection[1][i])
        noshifted_y.append( mypagecollection[2][i] )
        cgtimestamp.append(mypagecollection[3][i])
        cgvalidity.append( mypagecollection[5][i] )
        cgvergence.append( mypagecollection[6][i] )
        cgpupilsize.append( mypagecollection[7][i] )
        


    #Εδω θα φτιαξω την cgy με τα shift
    yline = calculateYline(text, pageno)
    for lineno in range(len(indexes)-1):
        start = int( indexes[lineno] )
        stop = int( indexes[lineno+1] )
        tempcgy = []
        for j in range(start,stop):
            tempcgy.append(mypagecollection[2][j])  #tempcgy : λιστα που περιεχει τα cutgazes y χωρις το shift
        
        avg = find_y_fromhist(tempcgy)

        nonzerostempcgy = [i for i in tempcgy if i != 0]


        if( nonzerostempcgy == [] ):
            ymedian = 0
            ymode = 0
        else:
            ymedian = statistics.median(nonzerostempcgy)
            ymode = statistics.mode(nonzerostempcgy)
        
        # print("ymedian = ",ymedian)
        # print("ymode = ",ymode)
        # print("count(ymode) = ", nonzerostempcgy.count(ymode))


        # print("avg_occ = ",avg)


        # identify chosen line
        templinedist = []
        for origlineno in range(len(ylinesin)):
            templinedist.append( abs(ymedian - ylinesin[origlineno]) )
        # print("templinedist = ",templinedist)
        linedist_lineno = templinedist.index( min(templinedist) )
        chosenline = linedist_lineno + 1
        print("chosenline = ", chosenline)


        # make SHIFTED y
        # print("yline[linedist_lineno]-ymedian = ",yline[linedist_lineno]-ymedian)
        for j in range(start,stop): 
            cgy.append( mypagecollection[2][j] + (yline[linedist_lineno]-ymedian) )


    cgroi = CutGazesROIs(roibounds, roistart, cgx, cgy)  #Και αυτη η συναρτηση θα μου φτιαξει τη λιστα με τα rois των cutgazes 

    
    return cgi, cgx, cgy, cgtimestamp, cgroi, cgvalidity, cgvergence, cgpupilsize, chosenline, noshifted_y



#CLICK AND OTHER EVENTS

#Η συναρτηση αυτη αποθηκευει σε καθε κλικ τα indexes και οταν κανω τον αριθμο των κοψιματων που πρεπει κλεινει το παραθυρο με τα κοψιματα
def onclick1(event):
    indexes.append(int(event.xdata))  #σε καθε κλικ αποθηκευει τα στοιχεια που βρισκονται στον αξονα των x, δηλαδη τα indexes των gazes
    
    global length, mycolor
    length = len(indexes)

    yvalue = 0
    if( ymin>=0 ):
        yvalue = ymin + 25
    yvals = [yvalue for d in range(len(indexes))]
    linecuts.set_xdata(indexes)
    linecuts.set_ydata(yvals)
    linecuts.set_data(indexes,yvals)
    
    mycolor = colorPicker(indexes, plines)
    
    from_multilines = True
    colorLeftplot(event, indexes, plines, gtempy, hardcases_glob, mycolor, f, ax1, ymin, ymax, xmin, xmax, from_multilines)
    colorRightplot(event, indexes, plines, gtempx, gtempy, G, G_ax, mycolor, from_multilines)
    
    f.canvas.draw_idle()


#Η συναρτηση αυτη αποθηκευει σε καθε κλικ το επιπεδο y της καθε γραμμης
def onclick2(event):
    levels.append(event.ydata)  #σε καθε κλικ αποθηκευει τα στοιχεια που βρισκονται στον αξονα των y, δηλαδη τα levels των γραμμων
    
    if( len(levels) == plines):
        plt.close('all')


#Δημιουργει ενα dialogue με το χρηστη για το αν δεχεται τα κοψιματα που εκανε ή οχι
def confirm():
    answer = askyesno(title='confirmation',
                    message='Accept Line Cuts?')
    
    if (answer==False):
        window1.destroy()
        plt.close()
        
    
    return answer


def cutROIScheck():
    answer = askyesno(title='confirmation',
                    message="Do you want to select ROIS?", 
                    default='no')
    
    if (answer==False):
        plt.close()   

    return answer


def cutLevelscheck():
    answer = askyesno(title='confirmation',
                    message="Accept Line Levels?")
    
    if (answer==False):
        plt.close()
        
    
    return answer



def CutLevels(sub1, exam, text, pageno, lines, mypagecollectiony):
    tempx = mypagecollectiony[1]
    tempy = mypagecollectiony[2]
    temponlylefteye = mypagecollectiony[8]
    temponlyrighteye = mypagecollectiony[9]
    
    ylinesin, ax = ShowGazesMakeLevelCuts(sub1, exam, text, pageno, lines, tempx, tempy)   # Make level Cuts
    cursor = Cursor( ax, horizOn=True, vertOn=True, useblit=True, color='r', linewidth=1 )
    plot_one_eye(sub1, exam, text, pageno, temponlylefteye, "Left Eye", [1410, 487])
    plot_one_eye(sub1, exam, text, pageno, temponlyrighteye, "Right Eye", [1410, 765])
    plt.show()
    
    while( len(ylinesin) != lines ):
        print("\n")
        if( len(ylinesin) != lines ):
            print("--Wrong Cut. You made only %d cuts.You need %d more." %(len(ylinesin), lines - len(ylinesin)) )

        ctypes.windll.user32.MessageBoxW(0, "You need to do it again!", "Warning!", 16)

        ylinesin, ax = ShowGazesMakeLevelCuts(sub1, exam, text, pageno, lines, tempx, tempy)(sub1, exam, text, pageno, lines, tempx, tempy)    # Make Cuts
        cursor = Cursor( ax, horizOn=True, vertOn=True, useblit=True, color='r', linewidth=1 )
        plot_one_eye(sub1, exam, text, pageno, temponlylefteye, "Left Eye", [1410, 437])
        plot_one_eye(sub1, exam, text, pageno, temponlyrighteye, "Right Eye", [1410, 715])
        plt.show()
    
    return ylinesin



def CutsProcedure(sub1, exam, text, pageno, lines, roistart, mypagecollection):
    tempx = mypagecollection[1]
    tempy = mypagecollection[2]

    # # # # # Cuts and Check of Cuts
    finalindexes = ShowGazesMakeCuts(sub1, exam, text, pageno, lines, tempx, tempy)    # Make Cuts
    existNone, ascendingcuts = checkCuts(finalindexes)    # Check if cuts are correct
    # # # # End of Cuts
    

    while( (existNone==True) or (ascendingcuts==False) ):
        print("\n")
        if( existNone==True ):
            print("--Wrong cut. You click out of the box.")
        
        if( existNone==False and ascendingcuts==False ):
            print("--Wrong cut. You make a backward cut.")

        ctypes.windll.user32.MessageBoxW(0, "You need to do it again!", "Warning!", 16)

        # # # # # Cuts and Check of Cuts
        finalindexes = ShowGazesMakeCuts(sub1, exam, text, pageno, lines, tempx, tempy) 
        existNone, ascendingcuts = checkCuts(finalindexes)
        # # # # # 

    print("x = ", finalindexes)
    
    cgi, cgx, cgy, cgtimestamp, cgroi, cgvalidity, cgvergence, cgpupilsize, chosenline, noshifted_y =  CutGazes(text, pageno, roistart, mypagecollection)               #Φτιαχνω τις λιστες με τα cutgazes(index, x, y, timestamp)
    cgdata = [cgi, cgx, cgy, cgtimestamp, cgroi, cgvalidity, cgvergence, cgpupilsize]


    # Φτιαχνω το γραφημα των Gazes & Cutgazes
    global window1
    flag = -1
    f, window1 = ShowGazesAndCutGazes(text, pageno, tempx, tempy, cgdata[1], cgdata[2], flag)     
    drawROIbounds(sub1, exam, text, pageno, roibounds, cgdata[1], cgdata[2], "rawgazes", [], plt, "noclose")        
           
    
    return finalindexes, cgdata, f, chosenline, noshifted_y



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




#Gazes & Cutgazes Plot
def ShowGazesAndCutGazesSecond(sub1, exam, text, pageno, tempx, tempy, finalcgx, finalcgy):
    f = plt.figure()
    ax = plt.subplot()
    f.set_size_inches(8, 7)

    image = folder1 + 'texts/'+ text + textends + '/Slide' + str(pageno) + '.PNG'
    img = plt.imread(image)
    ax.imshow(img)

    ax.plot(tempx, tempy, 'x', color = '#32F7E2', markeredgewidth=0.5)
    ax.plot(finalcgx, finalcgy, 'x', color = '#F78F32', markeredgewidth=0.5)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.axis('off')
    ax.set_title("Auto shifted gazes\n")
    
    # movefigure(f,500, 500)
    

    drawROIbounds(sub1, exam, text, pageno, roibounds, finalcgx, finalcgy, "shift'em", [], plt, "noclose")

    # plt.show()

    global window2
    window2 = tk.Tk()
    canvas = FigureCanvasTkAgg(f,master = window2)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    
    return f


def confirmation_box1(last_button_name):
    # Create a GUI app
    global app, global_last_button_name

    global_last_button_name = last_button_name

    app = Tk()
    w = 300 # width for the Tk root
    h = 135 # height for the Tk root
    # get screen width and height
    ws = app.winfo_screenwidth() # width of the screen
    hs = app.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2) + 200
    y = (hs/2) - (h/2) - 50

    # set the dimensions of the screen 
    # and where it is placed
    app.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    # Confirmation box gets the focus and stays on top
    app.lift()
    app.attributes('-topmost', True)
    app.focus_force()


    label1 = tk.Label(app, text="Accept Line Cuts???", font=('Segoe UI', 10))
    label1.grid(row=0, column=0, columnspan=3, pady=(20,10))




    # Creating and displaying of button b1
    b1 = Button(app, text="Yes", font=('Segoe UI', 10),
                command=lambda m="Yes": which_button(m), width=8, height=1, default='active')

    b1.grid(row=2, column=0, padx=20)
    # 🔹 Set initial focus to Yes button
    b1.focus_set()  # combine it with the command -,default='active'- from above
    app.bind('<Return>', lambda event: b1.invoke())
    
    # Creating and displaying of button b2
    b2 = Button(app, text="No", font=('Segoe UI', 10),
                command=lambda m="No": which_button(m), width=8, height=1)

    b2.grid(row=2, column=1, padx=10, pady=30)


    # Creating and displaying of button b2
    b3 = Button(app, text=last_button_name, font=('Segoe UI', 10),
                command=lambda m=last_button_name: which_button(m), width=8, height=1)

    b3.grid(row=2, column=2, padx=15, pady=30)

    # Make the infinite loop for displaying the app
    app.mainloop()
    return gb



# Create a function with one parameter, i.e., of
# the text you want to show when button is clicked
def which_button(button_press):
    # Printing the text when a button is clicked
    global gb
    gb = button_press

    app.quit()
    app.destroy()
    window1.destroy()
    window1.quit()

    return button_press




