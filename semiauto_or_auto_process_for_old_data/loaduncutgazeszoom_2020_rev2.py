
from asyncio.windows_events import NULL
import ctypes
import os
import time
import shutil
import statistics
from os.path import exists
import tkinter as tk
from tkinter.messagebox import askyesno
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)



from gazeshandling_2020_rev2 import gazeshandling
from commonfunctions_2020_rev2 import CutGazes, ShowGazesAndCutGazes, getpagelines


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2, textends, pyimagepath, guiflag
from basic_function_gui import basic_function_gui
from GetSomeInitialData import createextra, getGazesFolderbyText, getGazesFoldersandClass
from createSubfile import createSubfile
from MakeFixationsFile import MakeFixationsTxt
from MakeGazesFile import MakeGazesTxt
from GetAndDrawROIS import getROIbounds, drawROIbounds
from calcROI import calcROI
from creategazedata import CreateGazeData
from drawFixations import drawFixations
from fixationfun import fixationfun
from semiauto_or_auto_process.concatdata import concatdata
from storefinalindexes import storefinalindexes
from GazesPreview import GazesPreview
from movefigure import movefigure
from calculateYline import calculateYline
from Median import Median

from semiauto_or_auto_process.storerawdata import storegazedata_old_data, storevergencedata, store_pupil_z_data


                                                                                

                                                                           
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                 #
#                                                                                 #
#                                                                                 #
#    AFTH H SINARTHSH KOVEI DEDOMENA HD ALLA POY EXOUN MONO 5 STILES STA GAZES    #
#                                                                                 #         
#                                                                                 #
#                                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


                                                                                



def main():


    global from_runcrashes
    from_runcrashes = False
    
    filtered_flag = 0  # 0: for old type gazes, 1: for gazes_filtered.txt

    if( guiflag ):
        # Get Subject's Data from an Input Dialogue  
        textcheckedflag = 1                                                                                     
        subs = NULL
        while( subs==NULL ):
            subs, texts, firstchoices = basic_function_gui(textcheckedflag)
            bypass, hardcases, onlylefteye, onlyrighteye = firstchoices[0], firstchoices[1], firstchoices[2], firstchoices[3]

    else:
        # texts = [ 'visit', 'zoo', 'visitloud', 'psaras', 'morning', 'island', 'efeyreseis', 'zebra', 'armyjet', 'enemypie', 'gasmask', 'jockey', 'midfred', 'midfredloud', 'sunny', 'sunnyloud' ]
        texts = ['efeyreseis']
        # texts = ['sunny']
        # texts = ['visit', 'visitloud', 'zoo', 'psaras', 'efeyreseis', 'sunny', 'midfred', 'midfredloud', 'armyjet', 'gasmask']
                        
        #Orizw poia einai ta subjects pou thelw na treksw
        # subs = [696, 729, 11512, 11514, 11520, 11521, 11522, 11523, 11524, 11525, 11526, 11527, 11528, 11529, 11530, 11531, 11532, 11533, 11534, 11535, 11536, 11537, 11538, 11539, 11540, 11548]   #subject id
        # subs = [11513, 11514, 11521, 11522, 11523, 11525, 11526, 11529, 11530, 11532, 11533, 11534, 11536, 11538, 11540, 11544, 11545, 11548, 11549, 11550, 11551, 11553]
        # subs = [5007, 5025, 5032, 5037, 5038, 5044, 5045, 5051, 5053, 5064, 5068, 5069, 5077, 5082, 5085, 5089, 5094, 5098, 5122, 5123, 5140, 5144]
        # subs = [1455, 1461, 1488, 1523, 1527, 1533]
        # subs = [1455, 1456, 1459, 1460, 1461]
        # subs = [ person  for person  in range(908, 920) ]
        # subs = [x for x in range(1523, 1534)]
        subs = [1613]

        bypass = 0
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
                print("\nLoading gazes from gazes-original-1920.txt")
                time.sleep(5)
                # break
    
    
            if( (not exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i]) + '_pass.txt')) and (not exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i]) + '_crash.txt')) ):
                # Ksekinaei h analysh twn keimenwn 
                proceduredone = False
                Procedure(file, subs[i], exam[i], text, filtered_flag)  # Main procedure of the programme for each text
            
            if( (bypass==1) and (exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i]) + '_pass.txt')) ):
                # Ksekinaei h analysh twn keimenwn 
                os.remove(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i]) + '_pass.txt')
                proceduredone = False
                Procedure(file, subs[i], exam[i], text, filtered_flag)  # Main procedure of the programme for each text

        
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
def Procedure(file, sub1,  exam, text, filtered_flag):
    from_runcrashes = False
    
    global roibounds
 
    # gazesfilepath must be like: 
    # '/Radar_Iro_copy/individual/subject_696/ee_696_1_visit_wa_1_5_2021-11-25-03.05.21/gazes.txt'
    # OR
    # '/Radar_Iro_copy/individual/subject_696/ee_696_1_visit_wa_1_5_2021-11-25-03.05.21/gazespy.txt'    
    # the result depends on whether the file Tobii5L.txt exists or not
    gazesfile, lines, newgazes, vergence, vergence_z = gazeshandling(file, sub1, filtered_flag)

    # # # # # #  Plot eye vergence  # # # # #
    # if( vergence != NULL ):
    #     ploteyevergence(sub1, text, textends, 1, exam, vergence)

    
    # Load Gazes Data 
    index = []              #list that will contain the 'indexes' from gazes.txt
    x = []                  #list that will contain the 'x' from gazes.txt
    y = []                  #list that will contain the 'y' from gazes.txt
    timestamp = []          #list that will contain the timestamp from gazes.txt
    roi = []                #list that will contain the 'rois' from gazes.txt

    #Here i will load all gazes data into the lists I made before
    for p in lines:
        index.append( int(p.split(None)[0]) )                
        x.append( float(p.split(None)[1]) )                   
        y.append( float(p.split(None)[2]) )
        timestamp.append( float(p.split(None)[3]) )
        roi.append( int(p.split(None)[4]) )
    
    gazesfile.close()

    
    #Temporary lists that will save the cutgazes data per page
    pageno = -1             #page number, assumption pageno=-1
    tempindex = []          #temporary index list
    tempx = []              #temporary x list
    tempy = []              #temporary y list
    temptimestamp = []      #temporary timestamp list

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
                

                mypagecollection = [tempindex, tempx, tempy, temptimestamp]


                # # # # # # # # # Store gazedata per page, i.e gazes_page1.txt, gazes_page2.txt, gazes_page3.txt, .....  # # # # # # # # #
                gazedatatxt = folder1 + folder2 + '/subject_' + str(sub1) + '/' + file + '/py/gazes_page' + str(pageno) + '.txt'
                gazedatafile = open(gazedatatxt, 'w')
                gazedatafile.close()
                storegazedata_old_data(gazedatatxt, tempindex, tempx, tempy, temptimestamp)


                # # # # # # # # #  Store validationdata per page  # # # # # # # # #
                # #  vergence_page1.txt, vergence_page2.txt, vergence_page3.txt,  ......  
                # #  median_pupil_z_data_page1.txt, median_pupil_z_data_page2.txt,  ......
                # #  pupilsize_z_page1.txt, pupilsize_z_page2.txt,  ......
                if( vergence!= [] ):
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
                g, G_ax = GazesPreview(text, pageno, mypagecollection)
                finalindexes, cgdata, f = CutsProcedure(sub1, exam, text, pageno, lines, tempx, tempy, roistart, tempindex, temptimestamp, newgazes)
    
                answer = confirm()         #Ελεγχω εαν δεχομαι τα κοψιματα που εκανα
                
                while( answer == False ):  #Εαν η απαντηση ειναι 'οχι' τοτε ξανακανω την προηγουμενη διαδικασια
                    plt.close('all')
                    
                    # # Start Cuts Process 
                    g, G_ax = GazesPreview(text, pageno, mypagecollection)
                    finalindexes, cgdata, f = CutsProcedure(sub1, exam, text, pageno, lines, tempx, tempy, roistart, tempindex, temptimestamp,newgazes)
                
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

               
                #Find Fixations and Make fixations.txt file
                fixationdata = fixationfun( gazedata )
                MakeFixationsTxt(sub1, exam, text, pageno, roistart, fixationdata, roibounds)

             
                #Draw fixations(pane_number).png images
                drawFixations(sub1, exam, text, fixationdata, pageno, "yes", NULL)

         
                #Draw cutgazes(pane_number).png images
                drawROIbounds(sub1, exam, text, pageno, roibounds, cgdata[1], cgdata[2], "cutgazes", fixationdata, NULL, "close") 

                # Store finalindexes per page 
                storefinalindexes(sub1, pageno, file, finalindexes) 
           

            #Αδειαζω τις λιστες που περιεχουν τα δεδομενα της σελιδας που επεξεργαστηκα, ωστε να αποθηκευσω τα νεα δεδομενα της επομενης σελιδας
            tempindex = []
            tempx = []
            tempy = []
            temptimestamp = []

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

            if( vergence!=[] ):
                vergenceindex.append( vergence[i][0] )
                vergenceleftx.append( vergence[i][1] )
                vergencelefty.append( vergence[i][2] )
                vergencerightx.append( vergence[i][3] )
                vergencerighty.append( vergence[i][4] )  
                vergencetimestamp.append( vergence[i][5] ) 
                vergencepupilleft.append( vergence[i][7] )  
                vergencepupilright.append(vergence[i][8] )        

                vergenceleftz.append( vergence_z[i][0] )
                vergencerightz.append( vergence_z[i][1] )


    concatdata(sub1, exam, text, 'cutgazes', 'fixations')

    textpasstxt = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + '_pass.txt'
    textpassfile = open(textpasstxt, 'w')
    textpassfile.close()
    


#Βρισκω ποσες γραμμες εχει η σελιδα που βρισκομαι
def findpagelines(text, pageno):
    data = pd.read_excel (folder1 + 'texts/' + text + textends + '/py/lines/mytext.page(' + str(pageno) + ').lines.xlsx')
    x = data.iloc[:,0]
    return x[0]



#Φτιαχνω το γραφημα με τα Gazes
#args = { (sub1 : subject's id), (text : analysis text), (pageno : page number), (lines : total page lines), (tempx : list with X coords that have occur from my cut), (tempy : list with Y coords that have occur from my cut) }
def ShowGazesMakeCuts_load(sub1, exam, text, pageno, lines, tempx, tempy):
    global indexes, plines      #i made this global in order to use them some code below { (indexes : list with Index coords that have occur from my cut), (plines : page lines) }
    indexes, plines =  [], lines

    f = plt.figure()
    f.set_figwidth(14)
    f.set_figheight(8)
    ax = plt.subplot(1,1,1)
    ax.margins(x=0)
    plt.plot(tempx,'yellow')
    plt.plot(tempy,'b')

    pagesfile = open(folder1 + "texts/" + text + textends + "/py/pages/pages.txt", "r")
    pages = pagesfile.read(1)

    plt.title( "Subject: "+ str(sub1) + ", Text: " + text + ", Page: " + str(pageno) + " out of " + str(pages) + ", Lines: " + str(lines) )

    plt.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/linesteps' + str(pageno) + '.png')
    
    cursor = Cursor( ax, horizOn=True, vertOn=True, useblit=True, color='r', linewidth=1 )
    
    f.canvas.mpl_connect('button_press_event' , onclick1)
    movefigure(f, 3, 10)

    plt.show()
 
    return indexes




#Φτιαχνω και Επιστρεφω τις λιστες με τα cutgazes(index, x, y, timestamp roi)
#args = { (text : text), (pageno : page_number), (tindex : temporary index list), (tx : temporary x list), (ty : temporary y list), (ttimestamp : temporary timestamp list) }\
#variables = { (cgi : cutgazes index list), (cgx : cutgazes x list), (cgy : cutgazes y list), (cgtimestamp : cutgazes timestamp list), (cgroi : cutgazes rois list), (start : index of first cut), (stop : index of last cut) }
def CutGazes(text, pageno, roistart, tindex, tx, ty, ttimestamp):
    #Make data initializations
    global cgi, cgx ,cgy, cgtimestamp, cgroi
    cgi, cgx, cgy, cgtimestamp, cgroi = [], [], [], [], []

    start = int( indexes[0] )
    stop = int( indexes[-1] )

    #Εδω θα φτιαξω τις cgi, cgx, cgtimestamp
    for i in range( start , stop ):
        cgi.append(tindex[i])
        cgx.append(tx[i])
        cgtimestamp.append(ttimestamp[i])


    #Εδω θα φτιαξω την cgy με τα shift
    yline = calculateYline(text, pageno)
    for i in range(len(indexes)-1):
        start = int( indexes[i] )
        stop = int( indexes[i+1] )
        tempcgy = []
        for j in range(start,stop):
            tempcgy.append(ty[j])  #tempcgy : λιστα που περιεχει τα cutgazes y χωρις το shift
        
        
        ymedian = Median(tempcgy, 0)


        #Εδω φτιαχνω τη λιστα οπου περιχει τα cutgazes y με το shift    
        for j in range(start,stop): 
            cgy.append( ty[j] + (yline[i]-ymedian) )


    cgroi = CutGazesROIs(roistart, cgx, cgy)  #Και αυτη η συναρτηση θα μου φτιαξει τη λιστα με τα rois των cutgazes 
    
    return cgi, cgx, cgy, cgtimestamp, cgroi


#Φτιαχνω και επιστρεφω μια λιστα που περιεχει τα rois των cutgazes
#args = { (xlist : λιστα με τα cutgazes_x), (ylist : λιστα με τα cutgazes_y) }
def CutGazesROIs(roistart, xlist, ylist):
    cgroi = []
    for i in range( len(xlist) ):
        point_roi = calcROI(roistart, xlist[i], ylist[i], roibounds[0], roibounds[1], roibounds[2], roibounds[3]) #Find point's ROI
        cgroi.append(point_roi)
        
    return cgroi



#UNTIL HERE I HAVE COLLECT CUTGAZES AND I HAVE MAKE CUTGAZES FILE WITH THEIR ROIS
#AND NOW I PLOT THESE SPOTS (X,Y) ( SPOTS FROM CUTGAZES ) 


  
#CLICK AND OTHER EVENTS

#Η συναρτηση αυτη αποθηκευει σε καθε κλικ τα indexes και οταν κανω τον αριθμο των κοψιματων που πρεπει κλεινει το παραθυρο με τα κοψιματα
def onclick1(event):
    indexes.append(event.xdata)  #σε καθε κλικ αποθηκευει τα στοιχεια που βρισκονται στον αξονα των x, δηλαδη τα indexes των gazes
    
    global length
    length = len(indexes)
    
    if( len(indexes) == plines+1):
        plt.close('all')


#Δημιουργει ενα dialogue με το χρηστη για το αν δεχεται τα κοψιματα που εκανε ή οχι
def confirm():
    answer = askyesno(title='confirmation',
                    message='Accept Line Cuts?')
    
    if (answer==False):
        window.destroy()
        plt.close()
        
    
    return answer


def CutsProcedure(sub1, exam, text, pageno, lines, tempx, tempy, roistart, tempindex, temptimestamp, newgazes):

    # # # # # Cuts and Check of Cuts
    finalindexes = ShowGazesMakeCuts_load(sub1, exam, text, pageno, lines, tempx, tempy)    # Make Cuts
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

        ctypes.windll.user32.MessageBoxW(0, "You need to do it again!", "Warning!", 16)

        # # # # # Cuts and Check of Cuts
        finalindexes = ShowGazesMakeCuts_load(sub1, exam, text, pageno, lines, tempx, tempy) 
        existNone, ascendingcuts = checkCuts(finalindexes)
        # # # # # 

    print("x = ", finalindexes)
    
    cgdata =  CutGazes(text, pageno, roistart, tempindex, tempx, tempy, temptimestamp)               #Φτιαχνω τις λιστες με τα cutgazes(index, x, y, timestamp)

    
    # # # # # OMIT all gazes that are not valid # # # #
                         
    # cgdata, noshifted_y = clearcutgazes(cgdata, [])

    
    # Φτιαχνω το γραφημα των Gazes & Cutgazes
    global window
    flag = -1
    f, window = ShowGazesAndCutGazes(text, pageno, tempx, tempy, cgdata[1], cgdata[2], flag)             
           
    
    return finalindexes, cgdata, f



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


main()

