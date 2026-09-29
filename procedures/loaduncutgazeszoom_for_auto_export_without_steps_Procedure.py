
from asyncio.windows_events import NULL
import os
import time
import shutil
import statistics
from os.path import exists
import pandas as pd
import matplotlib.pyplot as plt


from globalVars import folder1, folder2, textends, pyimagepath, dispersion, dispersion2, guiflag
from basic_function_gui import basic_function_gui
from gazeshandling import gazeshandling
from calculateYline import calculateYline

from semiauto_or_auto_process.storerawdata import storegazedata, storevergencedata, store_pupil_z_data
from semiauto_or_auto_process.commonfunctions import getpagelines
from MakeFixationsFile import MakeFixationsTxt
from MakeGazesFile import MakeGazesTxt
from GetAndDrawROIS import getROIbounds, drawROIbounds
from creategazedata import CreateGazeData
from drawFixations import drawFixations
from semiauto_or_auto_process.concatdata import concatdata
from storefinalindexes import storefinalindexes
from GazesPreview_testattention import GazesPreview_testattention
from movefigure import movefigure
from loaduncutdata_hardcases import loaduncutdata_hardcases
from fixationfungap import fixationfungap
from drawEyeMovements import drawEyeMovements
from MakeDispersionTxt import MakeDispersionTxt
from MakePageFixationsGap import MakePageFixationsGap
from load_subs_initial_data import load_subs_initial_data
from make_textfolder_struct import make_textfolder_struct
from Median import Median



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                 #
#                                                                                 #
#                                                                                 #
#       AFTH H SINARTHSH ANALYEI DEDOMENA XORIS KOPSIMATA XWRIS SHIFT               #
#       STA RAW GAZES DHLADH, OPWS VGIKAN APO TON TRACKER                         #
#                                                                                 #
#                                                                                 #
#                                                                                 #
#                                                                                 #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



def loaduncutgazeszoom_for_auto_export_without_steps_Procedure(subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye, extra_flag_shift_gazes):

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
                Start_Text_Procedure(file, subs[i], exam, text, onlylefteye, onlyrighteye, extra_flag_shift_gazes)  # Main procedure of the programme for each text
            
            
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
                Start_Text_Procedure(file, subs[i], exam, text, onlylefteye, onlyrighteye, extra_flag_shift_gazes)  # Main procedure of the programme for each text

            
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
def Start_Text_Procedure(file, sub1,  exam, text, onlylefteye, onlyrighteye, extra_flag_shift_gazes):
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
    uncutgazes_raw, uncutgazes, negativecheck, oneeyeindexes = loaduncutdata_hardcases(text, exam, file, sub1, onlylefteye, onlyrighteye)

    # # # # #  Collect gazes data per column  # # # # #
    index, x, y, timestamp, roi, validity, vergence, pupilsize = uncutgazes[0], uncutgazes[1], uncutgazes[2], uncutgazes[3], uncutgazes[4], uncutgazes[5], uncutgazes[6], uncutgazes[7]
    
    
    
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

                finalindexes = [tempindex[0], tempindex[-1]]
                cgdata = [tempindex, tempx, tempy, temptimestamp, temproi, tempvalidity, tempvergence, temppupilsize]
                
                if( extra_flag_shift_gazes ):
                    shift_ygazes(text, pageno, cgdata, finalindexes)  
                    
                TestAttentionProcedure(sub1, exam, text, pageno, mypagecollection, cgdata)              
                
                drawROIbounds(sub1, exam, text, pageno, roibounds, cgdata[1], cgdata[2], "rawgazes", [], plt, "close") #In order to draw and save the rawgazes(pageno).png images

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
    


def shift_ygazes(text, pageno, cgdata, finalindexes):
    gazesy = cgdata[2]
    shifted_y = []
    validity = cgdata[5]
    
    #Εδω θα φτιαξω την cgy με τα shift
    yline = calculateYline(text, pageno)
    

    nonzerostempcgy = [nonzerocgy for nonzerocgy in gazesy if nonzerocgy!=0] # to nonzerocgy y exei ola ta gazes kai ta valid kai ta nonvalid. Gia na ipologisw omws th median ta -1 mou einaio axrista kai ta petaw.
    # ymedian = Median(nonzerostempcgy, 0)
    ymedian = +20
    

    #Εδω φτιαχνω τη λιστα οπου περιχει τα cutgazes y με το shift
    for j in range(finalindexes[0]-1, finalindexes[1]): 
        # shifted_y.append( gazesy[j] + (yline[0]-ymedian) + 1 )
        shifted_y.append( gazesy[j] + ymedian ) 
            
    cgdata[2] = shifted_y
    
    
            
def TestAttentionProcedure(sub, exam, text, pageno, mypagecollection, cgdata):
    global g_ax, g

    SaveLinesteps(sub, exam, text, pageno,  mypagecollection[1], mypagecollection[2])  

    g, g_ax = GazesPreview_testattention(text, pageno, mypagecollection, cgdata) 
    # plt.show(block=False)
    # plt.pause(1)    
    
    return 


        
def SaveLinesteps(sub, exam, text, pageno, tempx, tempy):
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
        plt.plot(tempy,'b')
        

    pagesfile = open(folder1 + "texts/" + text + textends + "/py/pages/pages.txt", "r")
    pages = pagesfile.read(1)


    plt.title( "Subject: "+ str(sub) + ", Text: " + text + ", Page: " + str(pageno) + " out of " + str(pages) )

    plt.savefig(folder1 + folder2 + 'subject_' + str(sub) + '/all_graphs/' + text + str(exam) + pyimagepath + '/linesteps' + str(pageno) + '.png')
    
    movefigure(f, 3, 10)
    plt.close()

    return 



