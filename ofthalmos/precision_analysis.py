




from asyncio.windows_events import NULL
import os
import time
import shutil
import statistics
import copy
import numpy as np
import xlsxwriter
import matplotlib.pyplot as plt
from datetime import datetime

# from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2, pyimagepath, guiflag
from basic_function_gui import basic_function_gui
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass
from createSubfile import createSubfile
from loaduncutdata_horizontal_eyeposition import loaduncutdata_horizontal_eyeposition



def main1():

    # Get Subject's Data from an Input Dialogue  

    global from_runcrashes, disparitywsh1, disparitywsh2, disparitywsh3, disparitywsh4, disparitycounter1, disparitycounter2, disparitycounter3, disparitycounter4
    
    from_runcrashes = False
    disparitycounter1 = -1
    disparitycounter2 = -1
    disparitycounter3 = -1
    disparitycounter4 = -1
    
    # Date timestamp
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y_%H-%M-%S")  # format date in the way i want,like: dd-mm-YY  H-M-S


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
        # texts = ['visit', 'zoo', 'zebra', 'visitloud']
        texts = ['midfred', 'visit', 'midfredloud', 'visitloud' ]
        # texts = ['zoo', 'visit', 'efeyreseis', 'olympia', 'morning', 'zebra', 'visitloud']
        
        # subs = [1455, 1456, 1459, 1460, 1461]
        # subs = [ person  for person  in range(908, 920) ]
        # subs = [x for x in range(13001, 13021)]
        # subs = [13003, 13017, 13044, 13054, 13058, 13066, 13070, 13086, 13105, 13108, 13158, 13161, 13166, 13167, 13172, 13178, 13198, 13203, 13209, 13222, 13234]
        # subs = [1638, 1482, 13032]
        # subs = [1488, 1490, 1424, 1431, 1441, 1461, 1482, 1531, 1532, 1580, 1632]   #ofthalmos list, me exophoria oi 5 teleftaioi
        subs = [1482]
        
        bypass = 1
        hardcases = 0
        onlylefteye = 0
        onlyrighteye = 0
        firstchoices = [bypass, hardcases, onlylefteye, onlyrighteye]


    # Orizw se poia exam einai to kathe subject
    exam = []
    
    statistical_results_folder = 'statistical_data/'
    disparitywb1 = xlsxwriter.Workbook(folder1 + folder2 + statistical_results_folder + 'horizontal_disparityInfo_' + str(timestamp) + '.xlsx')
    disparitywsh1 = disparitywb1.add_worksheet()
        
    disparitywb2 = xlsxwriter.Workbook(folder1 + folder2 + statistical_results_folder + 'vertical_disparityInfo_' + str(timestamp) + '.xlsx')
    disparitywsh2 = disparitywb2.add_worksheet()

    disparitywb3 = xlsxwriter.Workbook(folder1 + folder2 + statistical_results_folder + 'diagonal_disparityInfo_' + str(timestamp) + '.xlsx')
    disparitywsh3 = disparitywb3.add_worksheet()
    
    disparitywb4 = xlsxwriter.Workbook(folder1 + folder2 + statistical_results_folder + 'diagonal_statistical_analysis_' + str(timestamp) + '.xlsx')
    disparitywsh4 = disparitywb4.add_worksheet()
    

    # Kuria while loop gia na trexoun ola ta subject pou thelw ( trexw 1h loop gia ta subject kai 2h eswterikh loop gia ta texts tou subject )
    for i in range(len(subs)): 
        disparitycounter1 += 1
        disparitycounter2 += 1
        disparitycounter3 += 1
        disparitycounter4 += 1
        
    
        search1 = getGazesFoldersandClass(subs[i])   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/
        search2 = createSubfile(subs[i])             # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Users/RADAR/Documents/Optotech/
        
        if( search1 == NULL ):
            if(search2==NULL):
                exam.append(1)
                print("Subject %s doesn't exist" %subs[i])
                print("Path to subject: ", folder1 + folder2 + 'subject_' + str(subs[i]) + '/')
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

            if not os.path.exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_data/' + text + str(exam[i]) + pyimagepath):
                os.makedirs(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_data/' + text + str(exam[i]) + pyimagepath)
            
            if not os.path.exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i]) + '/py/extra_plots'):
                os.makedirs(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i]) + '/py/extra_plots')
    

            Procedure(file, subs[i], exam[i], text, onlylefteye, onlyrighteye)  # Main procedure of the programme for each text
            # disparitycounter1 += 1
            # disparitycounter2 += 1
            # disparitycounter3 += 1
            # disparitycounter4 += 1
            
            
        
        if( analysis_texts==[] ):
            print("\nΝo texts were found for Subject = %d " % subs[i])
            time.sleep(3)
        
         
              
    #Delete unneeded .txts 
    for file in os.listdir():
        if( file.endswith(".txt") ):
            if( os.stat(file).st_size==0 ):
                os.remove(file)
    
    disparitywb1.close()
    disparitywb2.close()
    disparitywb3.close()
    disparitywb4.close()




#Procedure's args ={ (text : text i will analyze), (folder : main folder), (sub1 : subject's id), (sub1class : subject's class) }
def Procedure(file, sub1,  exam, text, onlylefteye, onlyrighteye):
    global disparitycounter1, disparitycounter2, disparitycounter3, disparitycounter4
    

    # Load Gazes Data 
    uncutgazesraw, uncutgazes, oneeyeindexes = loaduncutdata_horizontal_eyeposition(text, file, sub1, onlylefteye, onlyrighteye)


    index, leftx, lefty, leftvalid, rightx, righty, rightvalid, timestamp = uncutgazesraw[0], uncutgazesraw[1], uncutgazesraw[2], uncutgazesraw[3], uncutgazesraw[4], uncutgazesraw[5], uncutgazesraw[6], uncutgazesraw[7]
    
    
    #Temporary lists that will save the cutgazes data per page
    pageno = -1             #page number, assumption pageno=-1
    
    tempindex = []
    templeftx = []
    templefty = []
    templeftvalid = []
    
    temprightx = []
    temprighty = []
    temprightvalid = []
    
    temptimestamp = []
    
    # counter for gazes lines
    i=-1  


    while( i<len(index) ):
        i+=1
        if(  ( i<len(index) and index[i] == 1 )  or  ( i == len(index) )  ):
            pageno+=1

            if(pageno>0) :
                
                print("\nsubject %d, text %s, page %d " %(sub1, text, pageno))          #Βρισκω τα ROIbounds του κειμενου

            if( len(tempindex) != 0 ):                  #Οταν φτασω στο τελος της 1ης σελιδας και εχω συλλεξει τα δεδομενα μου      
                finalindexes = []                                                         
                if( uncutgazesraw!= [] ):
                    finalindexespath = folder1 + folder2 + '/subject_' + str(sub1) + '/' + file + '/py/finalindexes_page' + str(pageno) + '.txt'
                    f = open(finalindexespath, 'r')
                    for line in f.readlines():
                        fields = line.split('\n')
                        finalindexes.append(int(float(fields[0])))
                    
                    # # FIRST: clear(None) vergence data from start finalindex till end finalindex
                    # vergenceindex, vergenceleftx_clean1, vergencerightx_clean1, vergencelefty_clean1, vergencerighty_clean1, vergenceleftvalid, vergencerightvalid = eyeposition_finalindex_clear(tempindex, templeftx, temprightx, templefty, temprighty, templeftvalid, temprightvalid, finalindexes)
                    
                    
                    # # SECOND: clear(None) vergence data line by line 
                    # vergenceindex, vergenceleftx_clean2, vergencerightx_clean2, vergencelefty_clean2, vergencerighty_clean2, vergenceleftvalid, vergencerightvalid = eyeposition_changeLine_clear(sub1, file, pageno, vergenceindex, vergenceleftx_clean1, vergencerightx_clean1, vergencelefty_clean1, vergencerighty_clean1, vergenceleftvalid, vergencerightvalid, finalindexes)
                    
                    
                    # # # # # # # # # # # # # # # # # # # # VERGENCE ANALYSIS PROCESS # # # # # # # # # # # # # # # # # # #
                    
                    windowlen = 5
                    disparitywindowmean = stdev_window(sub1, exam, text, pageno, windowlen, templeftx, templefty, temprightx, temprighty)
                    
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    
                    
                    


            #Αδειαζω τις λιστες που περιεχουν τα δεδομενα της σελιδας που επεξεργαστηκα, ωστε να αποθηκευσω τα νεα δεδομενα της επομενης σελιδας
            
            tempindex = []
            templeftx = []
            templefty = []
            templeftvalid = []
            
            temprightx = []
            temprighty = []
            temprightvalid = []
            
            temptimestamp = []

            
            plt.close('all')
        

        #Εδω δημιουργω τις λιστες των δεδομενων ανα σελιδα   
        if( i != len(index) ):

            if( uncutgazesraw!=[] ):
                tempindex.append( index[i] )
                templeftx.append( leftx[i] )
                templefty.append( lefty[i] )
                templeftvalid.append( leftvalid[i] )
                temprightx.append( rightx[i] )  
                temprighty.append( righty[i] ) 
                temprightvalid.append( rightvalid[i] )  
                temptimestamp.append( timestamp[i] )        

    
    

def stdev_window(sub1, exam, text, pageno, windowlen, templeftx, templefty, temprightx, temprighty):
    start = 0
    end = windowlen
    
    result_leftx = []
    negvalues_leftx = []
    
    result_lefty = []
    negvalues_lefty = []
    
    result_rightx = []
    negvalues_rightx = []
    
    result_righty = []
    negvalues_righty = []
    
    
    leftx_omit = copy.deepcopy(templeftx)
    lefty_omit = copy.deepcopy(templefty)
    rightx_omit = copy.deepcopy(temprightx)
    righty_omit = copy.deepcopy(temprighty)
    for i in range(len(leftx_omit)):
        if(leftx_omit[i]==-1):
            leftx_omit[i]=np.NaN
        if(lefty_omit[i]==-1):
            lefty_omit[i]=np.NaN
        if(rightx_omit[i]==-1):
            rightx_omit[i]=np.NaN
        if(righty_omit[i]==-1):
            righty_omit[i]=np.NaN
        
    while(end<len(templeftx)):
        windowleftx = leftx_omit[start:end]
        # clear_windowleftx = [ x for x in windowleftx if x!=-1 ]
        # window_leftx_stdev = statistics.stdev(clear_windowleftx)
        window_leftx_stdev = np.nanstd(windowleftx)
        result_leftx.append(window_leftx_stdev)
        if( -1 in windowleftx ):
            negvalues_leftx.append(window_leftx_stdev)
        else:
            negvalues_leftx.append(None)
        
        
        windowlefty = lefty_omit[start:end]
        window_lefty_stdev = np.nanstd(windowlefty)
        result_lefty.append(window_lefty_stdev)
        if( -1 in windowlefty ):
            negvalues_lefty.append(window_lefty_stdev)
        else:
            negvalues_lefty.append(None)
        

    
        windowrightx = rightx_omit[start:end]
        window_rightx_stdev = np.nanstd(windowrightx)
        result_rightx.append(window_rightx_stdev)
        if( -1 in windowrightx ):
            negvalues_rightx.append(window_rightx_stdev)
        else:
            negvalues_rightx.append(None)
            
        
        windowrighty = righty_omit[start:end]
        window_righty_stdev = np.nanstd(windowrighty)
        result_righty.append(window_righty_stdev)
        if( -1 in windowrighty ):
            negvalues_righty.append(window_righty_stdev)
        else:
            negvalues_righty.append(None)
        
        
        start+=1
        end+=1
    
    spikes1 = []
    count1 = 0
    for j in range(len(result_leftx)):
        if( abs(abs(result_leftx[j])-abs(result_rightx[j]))>50 ):
            count1 += 1
            spikes1.append( result_leftx[j] )
        else:
            spikes1.append(None)
    print("count1 = ", count1)
    
    spikes2 = []
    count2 = 0
    for j in range(len(result_righty)):
        if( abs(abs(result_lefty[j]) - abs(result_righty[j]))>50 ):
            count2 += 1
            spikes2.append( result_lefty[j] )
        else:
            spikes2.append(None)
    print("count2 = ", count2)



    # right plot
    f1, ax1 = plt.subplots()
    f1.set_figwidth(18)
    f1.set_figheight(4)
    ax1.plot(result_leftx, 'steelblue')
    ax1.plot(result_rightx, 'orange')
    ax1.plot(negvalues_leftx, 'o', color='cyan', markersize=3, markeredgecolor='black', markeredgewidth=0.5)
    ax1.plot(negvalues_rightx, 'o', color = 'red', markersize=3, markeredgecolor='black', markeredgewidth=0.5)
    ax1.plot(spikes1, 'o', color = 'pink', markersize=5, markeredgecolor='black', markeredgewidth=0.5)
    # title and labels, setting initial sizes
    f1.suptitle(str(sub1) + '  ' + 'Leftx, Rightx Stdev Precision Window', fontsize=11, fontweight ="bold")
    ax1.set_xlabel('Time', fontsize=11)
    ax1.set_ylabel('Gazes', fontsize=11)
    ax1.margins(x=0.005)
    ax1.grid() 
    f1.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/extra_plots/window_precision_x_stdev' + str(pageno) + '.png', dpi=100)
    plt.show()
    
    f2, ax2 = plt.subplots()
    f2.set_figwidth(18)
    f2.set_figheight(4)
    ax2.plot(result_lefty, 'steelblue')
    ax2.plot(result_righty, 'orange')
    ax2.plot(negvalues_lefty, 'o', color='cyan', markersize=3, markeredgecolor='black', markeredgewidth=0.5)
    ax2.plot(negvalues_righty, 'o', color = 'red', markersize=3, markeredgecolor='black', markeredgewidth=0.5)
    ax2.plot(spikes2, 'o', color = 'magenta', markersize=5, markeredgecolor='black', markeredgewidth=0.5)
    # title and labels, setting initial sizes
    f2.suptitle(str(sub1) + '  ' + 'Lefty, Righty Stdev Precision Window', fontsize=11, fontweight ="bold")
    ax2.set_xlabel('Time', fontsize=11)
    ax2.set_ylabel('Gazes', fontsize=11)
    ax2.margins(x=0.005)
    ax2.grid() 
    f2.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/extra_plots/window_precision_y_stdev' + str(pageno) + '.png', dpi=100)
    plt.show()
    
        
    return result_leftx
    
    


main1()