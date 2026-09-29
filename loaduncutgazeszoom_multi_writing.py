
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
import xlsxwriter
from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)


from globalVars import folder1, folder2, textends, pyimagepath, guiflag
from basic_function_gui import basic_function_gui
from GetSomeInitialData import createextra, getGazesFolderbyText, getGazesFoldersandClass
from createSubfile import createSubfile
from gazeshandling import gazeshandling
from makenoshift import makenoshift
from restoreDrops import restoreDrops
from semiauto_or_auto_process.storerawdata import storegazedata, storevergencedata, store_pupil_z_data
from semiauto_or_auto_process.commonfunctions import CutGazes, ShowGazesAndCutGazes, getpagelines
from MakeFixationsFile import MakeFixationsTxt
from MakeGazesFile_writing import MakeGazesTxt_writing
from GetAndDrawROIS import getROIbounds, drawROIbounds
from creategazedata import CreateGazeData
from drawFixations import drawFixations
from semiauto_or_auto_process.concatdata import concatdata
from storefinalindexes import storefinalindexes
from movefigure import movefigure
from GazesPreview import GazesPreview
from first_clarification import first_clarification
from calculateYline import calculateYline
from CutGazesROIs import CutGazesROIs
from nextLine import nextLine
from chosenrois import chosenrois
from find_y_fromhist import find_y_fromhist
from calculateYline import calculateYline
from countDrops import countDrops
from fixationfungap import fixationfungap
from loaduncutdata import loaduncutdata
from MakePageFixationsGap import MakePageFixationsGap



def main():

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

    global hardcases
    
    
    if( guiflag ):
        textcheckedflag = 1
        subs = NULL
        while( subs==NULL ):
            subs, texts, firstchoices = basic_function_gui(textcheckedflag)
            bypass, hardcases, onlylefteye, onlyrighteye = firstchoices[0], firstchoices[1], firstchoices[2], firstchoices[3]

    else:
        # texts = ['visit', 'zoo', 'visitloud', 'psaras', 'morning', 'island', 'efeyreseis', 'zebra', 'armyjet', 'enemypie', 'gasmask', 'jockey', 'midfred', 'midfredloud', 'sunny', 'sunnyloud']
        # texts = ['visit', 'zoo']
        # texts = ['visit', 'visitloud', 'zoo', 'psaras', 'efeyreseis', 'sunny', 'midfred', 'midfredloud', 'armyjet', 'gasmask']
        texts = ['adk1k2part1']


        #Orizw poia einai ta subjects pou thelw na treksw
        # subs = [696, 729, 11512, 11514, 11520, 11521, 11522, 11523, 11524, 11525, 11526, 11527, 11528, 11529, 11530, 11531, 11532, 11533, 11534, 11535, 11536, 11537, 11538, 11539, 11540, 11548]   #subject id
        # subs = [11513, 11514, 11521, 11522, 11523, 11525, 11526, 11529, 11530, 11532, 11533, 11534, 11536, 11538, 11540, 11544, 11545, 11548, 11549, 11550, 11551, 11553]
        # subs = [5007, 5025, 5032, 5037, 5038, 5044, 5045, 5051, 5053, 5064, 5068, 5069, 5077, 5082, 5085, 5089, 5094, 5098, 5122, 5123, 5140, 5144]
        # subs = [x for x in range(1533, 1534)]
        subs = [1786]
        # subs = [1455, 1461, 1488, 1523, 1527, 1533]
        # subs = [1455, 1523]

        bypass = 1
        hardcases = 0
        onlylefteye = 0
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

            if( (bypass==1) and (exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i]) + '_pass.txt')) ):
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
    
    global roibounds
 
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
    uncutgazes_raw, uncutgazes, oneeyeindexes = loaduncutdata(text, exam, file, sub1, onlylefteye, onlyrighteye)
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

    i=-1

    roiselectedpath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/finalROISselected.txt'
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
                
                mypagecollection = [tempindex, tempx, tempy, temptimestamp, temproi, tempvalidity, tempvergence, temppupilsize]

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



                global ylinesin
                ylinesin = calculateYline(text, pageno)


                # # Start Gazes Cut Process
                finalindexes, shifted_list, noshifted_list = GazesCutMain(sub1, exam, text, pageno, lines, roistart, mypagecollection)
                # # End Gazes Cut Process


                window1.mainloop()

    
                gazedata = CreateGazeData(shifted_list)


                if( noshifted_list[0] != [] ):
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



                # # # # # # # # # # # # Some extra for writing/gap procedure  # # # # # # # # # # # #

                #Make cutgazes.txt file
                cutgazesgappagetxt = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/cutgazes' + str(pageno) + '.txt'
                cutgazesgappagefile = open(cutgazesgappagetxt,"w")
                cutgazesgappagefile.close()
                MakeGazesTxt_writing(cutgazesgappagetxt, gazedata)


                # # # # # # # # # # # # # # # # # # # # # # #  Gap Process -- NEW FIXATION  # # # # # # # # # # # # # # # # # # # # # # 

                #Find Fixations and Make fixations.txt file
                fixationdatagap, gazestart, gazeend, fixationstart, fixationend, gap_data = fixationfungap(gazedata, roistart, roibounds)
                MakeFixationsTxt(sub1, exam, text, pageno, roistart, fixationdatagap, roibounds)
                MakePageFixationsGap(sub1, exam, text, pageno, gazestart, gazeend, fixationstart, fixationend, gap_data)

                # # # # # # # # # # # # # # # # # # # # # # End Gap Process # # # # # # # # # # # # # # # # # # # # # #          



                #Draw fixations(pane_number).png images
                drawFixations(sub1, exam, text, fixationdatagap, pageno, "yes", NULL)

         
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


    # # # # # # # # # # count gaps / find some data according to gaps # # # # # # # # # #
    dropsfilepath1 = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/count_drops.xlsx'
    dropsbook   = xlsxwriter.Workbook(dropsfilepath1)
    worksheet1 = dropsbook.add_worksheet('Cutgazes_Drops')
    cutgazesdrops = countDrops(sub1, exam, text, 'cutgazes', worksheet1)
    # worksheet2 = dropsbook.add_worksheet('Fixations_Drops')
    # fixationdrops= countDrops(sub1, exam, text, 'fixations', worksheet2)
    dropsbook.close()

    
    dropsfilepath2 = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/restore_from_drops.txt'
    dropstxtcutgazes  = open(dropsfilepath2, "w")


    dropsfilepath3 = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/restore_from_drops.xlsx'
    dropsbook   = xlsxwriter.Workbook(dropsfilepath3)
    worksheet2 = dropsbook.add_worksheet('Drops_Before_ROI')
    worksheet3 = dropsbook.add_worksheet('Drops_After_ROI')


    restoreDrops(sub1, exam, text, 'cutgazes', dropstxtcutgazes, worksheet2, worksheet3)
    dropstxtcutgazes.close()
    dropsbook.close()
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



    textpasstxt = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + '_pass.txt'
    textpassfile = open(textpasstxt, 'w')
    textpassfile.close()




def gazesloop(sub1, exam, text, pageno, lines, roistart, mypagecollection):
    # # # # # Start Cuts Process 
    g, G_ax = GazesPreview(text, pageno, mypagecollection)
    finalindexes, cgdata, f, firstchosenline, noshifted_y = CutsProcedure(sub1, exam, text, pageno, lines, roistart, mypagecollection)
    
    return finalindexes, cgdata, f, firstchosenline, noshifted_y



def shiftemProced(sub1, exam, text, pageno, tempx, tempy, roistart, firstchosenline, lines, cgdata, noshifted_y):
    # # Start Shift by Line Procedure  
    lastlinewords_data = pd.read_excel( folder1 + 'texts/'+ text + textends + '/py/mytext/lastlinewords/lastlinewords(' + str(pageno) + ').xlsx', header=None)
    lastlinewords = lastlinewords_data.iloc[:,0]
    lastlinewords = lastlinewords.to_list()
    
    shiftedLines = [firstchosenline]
    chosenroislist = chosenrois(firstchosenline, lastlinewords)
    
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



def GazesCutMain(sub1, exam, text, pageno, lines, roistart, mypagecollection):

    finalindexes, cgdata, f, firstchosenline, noshifted_y = gazesloop(sub1, exam, text, pageno, lines, roistart, mypagecollection)
    answer1 = confirmation_box1("Shift'em")         #Ελεγχω εαν δεχομαι τα κοψιματα που εκανα

    while( answer1 == 'No' ):  #Εαν η απαντηση ειναι 'οχι' τοτε ξανακανω την προηγουμενη διαδικασια
        plt.close()
        finalindexes, cgdata, f, firstchosenline, noshifted_y = gazesloop(sub1, exam, text, pageno, lines, roistart, mypagecollection)
        answer1 = confirmation_box1("Shift'em")
        
    if(answer1 == 'Yes' ):    #Εαν η απαντηση ειναι 'ναι' (οτι δεχομαι δηλαδη τα κοψιματα που εκανα) τοτε φτιαχνω τις εικονες των cutgazes(page_number).png και κλεινω το τρεχον window 

        plt.close('all')
        return finalindexes, cgdata, []
    
    
    if(answer1 == "Shift'em" ):
        
        shifted_list, noshifted_list = shiftemProced(sub1, exam, text, pageno, mypagecollection[1], mypagecollection[2], roistart, firstchosenline, lines, cgdata, noshifted_y)


    
    return finalindexes, shifted_list, noshifted_list
        



def close_figure_enter(event):
    if( event.key == 'enter' ):
        # plt.close(event.canvas.figure)
        plt.close('all')



#Φτιαχνω το γραφημα με τα Gazes
#args = { (sub1 : subject's id), (text : analysis text), (pageno : page number), (lines : total page lines), (tempx : list with X coords that have occur from my cut), (tempy : list with Y coords that have occur from my cut) }
def ShowGazesMakeCuts(sub1, exam, text, pageno, lines, tempx, tempy):
    global indexes, plines      #i made this global in order to use them some code below { (indexes : list with Index coords that have occur from my cut), (plines : page lines) }
    indexes, plines =  [], lines

    
    f = plt.figure()
    f.set_figwidth(14)
    f.set_figheight(9)
    ax1 = plt.subplot(1,1,1)
    ax1.margins(x=0)

    plt.plot(tempx,'yellow')
    if( hardcases ):
        plt.plot(tempy,'bo')
    else:
        plt.plot(tempy,'b')
        

    pagesfile = open(folder1 + "texts/" + text + textends + "/py/pages/pages.txt", "r")
    pages = pagesfile.read()

    ax1.set_title( 'Click to set the START and END of each line consecutively. When finished press ENTER\n' + "Subject: "+ str(sub1) + ", Text: " + text + ", Page: " + str(pageno) + " out of " + str(pages) + ", Lines: " + str(lines) )

    extent = ax1.get_window_extent().transformed(f.dpi_scale_trans.inverted())
    f.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/linesteps' + str(pageno) + '.png', bbox_inches=extent)

    
    cursor = Cursor( ax1, horizOn=True, vertOn=True, useblit=True, color='r', linewidth=1 )
    
    f.canvas.mpl_connect('button_press_event' , onclick1)
    movefigure(f, 3, 10)

    plt.gcf().canvas.mpl_connect('key_press_event', close_figure_enter)

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
    
    cursor = Cursor( ax, horizOn=True, vertOn=True, useblit=True, color='r', linewidth=1 )
    
    f.canvas.mpl_connect('button_press_event' , onclick2)


    plt.show()
 
    return levels



#Φτιαχνω και Επιστρεφω τις λιστες με τα cutgazes(index, x, y, timestamp roi)
#args = { (text : text), (pageno : page_number), (tindex : temporary index list), (tx : temporary x list), (ty : temporary y list), (ttimestamp : temporary timestamp list) }\
#variables = { (cgi : cutgazes index list), (cgx : cutgazes x list), (cgy : cutgazes y list), (cgtimestamp : cutgazes timestamp list), (cgroi : cutgazes rois list), (start : index of first cut), (stop : index of last cut) }
def CutGazes(text, pageno, roistart, mypagecollection):
    tindex, tx, ty, ttimestamp, tvalidity, tvergence, tpupilsize = mypagecollection[0], mypagecollection[1], mypagecollection[2], mypagecollection[3], mypagecollection[5], mypagecollection[6], mypagecollection[7]

    #Make data initializations
    global cgi, cgx ,cgy, cgtimestamp, cgroi, cgvalidity, cgvergence, cgpupilsize, noshifted_y
    cgi, cgx, cgy, cgtimestamp, cgroi, cgvalidity, cgvergence, cgpupilsize, noshifted_y = [], [], [], [], [], [], [], [], []



    start = int( indexes[0] )
    stop = int( indexes[-1] )

    #Εδω θα φτιαξω τις cgi, cgx, cgtimestamp
    for i in range( start , stop):
        cgi.append(tindex[i])
        cgx.append(tx[i])
        cgtimestamp.append(ttimestamp[i])
        cgvalidity.append(tvalidity[i])
        cgvergence.append(tvergence[i])
        cgpupilsize.append(tpupilsize[i])
        noshifted_y.append( ty[i] )


    #Εδω θα φτιαξω την cgy με τα shift
    yline = calculateYline(text, pageno)
    for lineno in range(len(indexes)-1):
        start = int( indexes[lineno] )
        stop = int( indexes[lineno+1] )
        tempcgy = []
        for j in range(start,stop):
            tempcgy.append(ty[j])  #tempcgy : λιστα που περιεχει τα cutgazes y χωρις το shift
        
        avg = find_y_fromhist(tempcgy)

        nonzerostempcgy = [i for i in tempcgy if i != 0]


        if( nonzerostempcgy == [] ):
            ymedian = 0
            ymode = 0
        else:
            ymedian = statistics.median(nonzerostempcgy)
            ymode = statistics.mode(nonzerostempcgy)
        
        print("ymedian = ",ymedian)
        print("ymode = ",ymode)
        # print("count(ymode) = ", nonzerostempcgy.count(ymode))


        print("avg_occ = ",avg)


        # identify chosen line
        templinedist = []
        for origlineno in range(len(ylinesin)):
            templinedist.append( abs(ymedian - ylinesin[origlineno]) )
        print("templinedist = ",templinedist)
        linedist_lineno = templinedist.index( min(templinedist) )
        chosenline = linedist_lineno + 1
        # print("chosenline = ", chosenline)


        # make SHIFTED y
        print("yline[linedist_lineno]-ymedian = ",yline[linedist_lineno]-ymedian)
        for j in range(start,stop): 
            cgy.append( ty[j] + (yline[linedist_lineno]-ymedian) )


    cgroi = CutGazesROIs(roibounds, roistart, cgx, cgy)  #Και αυτη η συναρτηση θα μου φτιαξει τη λιστα με τα rois των cutgazes 
    
    return cgi, cgx, cgy, cgtimestamp, cgroi, cgvalidity, cgvergence, cgpupilsize, chosenline, noshifted_y



#CLICK AND OTHER EVENTS

#Η συναρτηση αυτη αποθηκευει σε καθε κλικ τα indexes και οταν κανω τον αριθμο των κοψιματων που πρεπει κλεινει το παραθυρο με τα κοψιματα
def onclick1(event):
    indexes.append(event.xdata)  #σε καθε κλικ αποθηκευει τα στοιχεια που βρισκονται στον αξονα των x, δηλαδη τα indexes των gazes
    
    global length
    length = len(indexes)


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



def cutLevelscheck():
    answer = askyesno(title='confirmation',
                    message="Accept Line Levels?")
    
    if (answer==False):
        plt.close()
        
    
    return answer



def CutLevels(sub1, exam, text, pageno, lines, tempx, tempy):

    ylinesin = ShowGazesMakeLevelCuts(sub1, exam, text, pageno, lines, tempx, tempy)   # Make level Cuts
    
    while( len(ylinesin) != lines ):
        print("\n")
        if( len(ylinesin) != lines ):
            print("--Wrong Cut. You made only %d cuts.You need %d more." %(len(ylinesin), lines - len(ylinesin)) )

        ctypes.windll.user32.MessageBoxW(0, "You need to do it again!", "Warning!", 16)

        ylinesin = ShowGazesMakeLevelCuts(sub1, exam, text, pageno, lines, tempx, tempy)(sub1, exam, text, pageno, lines, tempx, tempy)    # Make Cuts

        
    return ylinesin



def CutsProcedure(sub1, exam, text, pageno, lines, roistart, mypagecollection):


    # # # # # Cuts and Check of Cuts
    finalindexes = ShowGazesMakeCuts(sub1, exam, text, pageno, lines, mypagecollection[1], mypagecollection[2])    # Make Cuts
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
        finalindexes = ShowGazesMakeCuts(sub1, exam, text, pageno, lines, mypagecollection[1], mypagecollection[2]) 
        existNone, ascendingcuts = checkCuts(finalindexes)
        # # # # # 

    print("x = ", finalindexes)
    
    cgi, cgx, cgy, cgtimestamp, cgroi, cgvalidity, cgvergence, cgpupilsize, chosenline, noshifted_y =  CutGazes(text, pageno, roistart, mypagecollection)               #Φτιαχνω τις λιστες με τα cutgazes(index, x, y, timestamp)
    cgdata = [cgi, cgx, cgy, cgtimestamp, cgroi, cgvalidity, cgvergence, cgpupilsize]


    # # # # # OMIT all gazes that are not valid # # # #
    # cgdata, noshifted_y = clearcutgazes(cgdata, noshifted_y)


    # Φτιαχνω το γραφημα των Gazes & Cutgazes
    global window1
    flag = -1
    f, window1 = ShowGazesAndCutGazes(text, pageno, mypagecollection[1], mypagecollection[2], cgdata[1], cgdata[2], flag)     
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
    
    plt.gcf().canvas.mpl_connect('key_press_event', close_figure_enter)

    plt.show()
    
    return f



def confirmation_box1(last_button_name):
    # Create a GUI app
    global app, global_last_button_name

    global_last_button_name = last_button_name

    app = Tk()
    w = 250 # width for the Tk root
    h = 200 # height for the Tk root
    # get screen width and height
    ws = app.winfo_screenwidth() # width of the screen
    hs = app.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2) + 200
    y = (hs/2) - (h/2) - 50

    # set the dimensions of the screen 
    # and where it is placed
    app.geometry('%dx%d+%d+%d' % (w, h, x, y))


    label1 = tk.Label(app, text="Accept Line Cuts?", font=('times', 13))
    label1.grid(row=0, column=0, columnspan=2, pady=20)



    # Creating and displaying of button b1
    b1 = Button(app, text="Yes",
                command=lambda m="Yes": which_button(m), width=6, height=2)

    b1.grid(row=1, column=0, padx=20)
    
    # Creating and displaying of button b2
    b2 = Button(app, text="No",
                command=lambda m="No": which_button(m), width=6, height=2)

    b2.grid(row=1, column=1, padx=10, pady=30)


    # Creating and displaying of button b2
    b3 = Button(app, text=last_button_name,
                command=lambda m=last_button_name: which_button(m), width=6, height=2)

    b3.grid(row=1, column=2, padx=15, pady=30)

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



main()

