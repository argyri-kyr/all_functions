from asyncio.windows_events import NULL
import calendar
import shutil
import time
import pandas as pd
from os.path import exists
import matplotlib
import matplotlib.pyplot as plt
import statistics



from commonfunctions_2020_rev2 import CutGazes
from gazeshandling_2020_rev2 import gazeshandling


import sys
matplotlib.use('Agg')

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2, pyimagepath, textends, guiflag
from basic_function_gui import basic_function_gui
from GetAndDrawROIS import getROIbounds, drawROIbounds
from GetSomeInitialData import createextra, getGazesFolderbyText, getGazesFoldersandClass
from MakeFixationsFile import MakeFixationsTxt
from MakeGazesFile import MakeGazesTxt
from creategazedata import CreateGazeData
from drawFixations import drawFixations
from fixationfun import fixationfun
from drawEyeMovements import drawEyeMovements
from createSubfile import createSubfile
from storefinalindexes import storefinalindexes


from semiauto_or_auto_process.pagelinelimitsfun import pagelinelimitsfun
from semiauto_or_auto_process.ShowGazesMakeCuts import ShowGazesMakeCuts
from semiauto_or_auto_process.commonfunctions import ShowGazesAndCutGazes, getpagelines
from semiauto_or_auto_process.concatdata import concatdata
from semiauto_or_auto_process.saveCrash import saveCrashList
from semiauto_or_auto_process.ygazesfilplot import ygazesfilPlot
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
    start = time.time()

    timestamp = calendar.timegm(time.gmtime())

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
        # texts = ['morning', 'visit', 'zoo', 'efeyreseis']
        # texts = ['visit', 'visitloud', 'zoo', 'psaras', 'efeyreseis', 'sunny', 'midfred', 'midfredloud', 'armyjet', 'gasmask']
        # texts = ['visit', 'zoo']
        texts = ['RAN']


        #Orizw poia einai ta subjects pou thelw na treksw
        # subs = [696, 729, 11512, 11514, 11520, 11521, 11522, 11523, 11524, 11525, 11526, 11527, 11528, 11529, 11530, 11531, 11532, 11533, 11534, 11535, 11536, 11537, 11538, 11539, 11540, 11548]   #subject id
        # subs = [11513, 11514, 11521, 11522, 11523, 11525, 11526, 11529, 11530, 11532, 11533, 11534, 11536, 11538, 11540, 11544, 11545, 11548, 11549, 11550, 11551, 11553]
        # subs = [5007, 5025, 5032, 5037, 5038, 5044, 5045, 5051, 5053, 5064, 5068, 5069, 5077, 5082, 5085, 5089, 5094, 5098, 5122, 5123, 5140, 5144]
        # subs = [1461, 1488, 1527, 1533]
        # subs = [1455, 1456, 1459, 1460, 1461]
        # subs = [ person  for person  in range(908, 920)]
        # subs = [x for x in range(1533, 1534)]
        subs = [11949]

        bypass = 0
        hardcases = 0
        onlylefteye = 0
        onlyrighteye = 0
        firstchoices = [bypass, hardcases, onlylefteye, onlyrighteye]
        

    # Orizw se poia exam einai to kathe subject
    exam = []
    

    if( len(sys.argv) > 1 ):
        subs = []
        texts = []
        multiplesubjects = sys.argv[-1]

        if( multiplesubjects == "True" ):
            
            if( len(sys.argv) == 4 ):
                number = sys.argv[1]
                if(number[0]!="["):
                    subs.append(int(number))
                else:
                    startsub = ""
                    endsub = ""
                    komma = False
                    for i in range(1,len(number)-1):
                        
                        if( number[i]!="," and komma==False ):
                            startsub += number[i]
                        
                        if( number[i]=="," ):
                            komma = True
                        
                        if( number[i]!="," and komma==True ):
                            endsub += number[i]
                
                    subs = [i for i in range(int(startsub), int(endsub))]

            elif( len(sys.argv) > 4):
                for i in range(1, len(sys.argv)-2):
                    subs.append(int(sys.argv[i]))
                
            texts = [ str(sys.argv[-2]) ]
        
        
        elif(multiplesubjects == "False"):
            subs = [ int(sys.argv[1]) ]
            for i in range(2, len(sys.argv)-1):
                texts.append(str(sys.argv[i]))

    

    #Arxikopoiw kapoia .txt arxeia pou tha xreiastw
    global cutsUItxt, errorcrashtxt, runcrashestxt, secondtimetxt, crashtxt

    #Arxikopoiw kapoia .txt pou tha xreiastw sth sunexeia
    cutsUItxt = folder1 + 'cutsforUImanip_py.txt'
    cutsUIfile = open(cutsUItxt, 'w')
    cutsUIfile.close()

    errorcrashtxt = folder1 + 'pagelinelimits_crash_list_py.txt'
    errorcrashfile = open(errorcrashtxt, 'w')
    errorcrashfile.close()
    
    runcrashestxt = folder1 + 'for_runcrashes_' + str(timestamp) + '.txt'
    runcrashesfile = open(runcrashestxt, 'w')
    runcrashesfile.close()

    secondtimetxt = folder1 + 'second_time_list_py.txt'
    secondtimefile = open(secondtimetxt, 'w')
    secondtimefile.close()

    crashtxt = folder1 +'crash_list_py.txt'
    crashfile = open(crashtxt, 'a')
    crashfile.close()

    
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

    # Delete runcrashestxt if it is null
    if( os.path.getsize(runcrashestxt) == 0 ):
            os.remove(runcrashestxt)                                        


    end = time.time()
    t1 = end - start
    
    hours = int(t1/3600)
    t1 = t1 - (hours*3600)
    
    minutes = int(t1/60)
    t1 = t1 - (minutes*60)
    
    seconds = t1

    print("\nTime needed to execute")
    print("Hours:", hours)
    print("Minutes:", minutes)
    print("Seconds:", seconds)



#Procedure's args ={ (file : subject's text file that is analyzing), (sub1 : subject's id), (exam : subject's exam), (text : text i will analyze) }
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

    crash = False
    crashlist = []
    secondRun = False


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
                
                print("\nsubject %d, text %s, page %d " %(sub1, text, pageno))


            # # # Loop per PAGE
            if( len(tempindex) != 0 ):                                                         
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
                    
                    
                if(secondRun==False):
                    firstruncuts = 0
                else:
                    firstruncuts = run[3]    # afto einai to prohgoumeno run
                
                run = pagelinelimitsfun(tempx, tempy, lines, sub1, exam, text, pageno, cutsUItxt, errorcrashtxt, runcrashestxt, crashlist, secondRun, firstruncuts)
                flag = run[1]


                if(flag==0):
                    print("run: failed")

                    crashlist = run[2]
                    if(secondRun==False):
                        if(crashlist!=[]):
                            saveCrashList(sub1, text, crashlist, secondtimetxt)

                    ygfil = ygazesfilPlot(cutsUItxt, sub1, exam, text, pageno)
                    xo, yo, average = ygfil[0], ygfil[1], ygfil[2]
                    
                    finalindexes = ShowGazesMakeCuts(sub1, exam, text, pageno, lines, tempx, tempy, xo, yo, average, flag, secondRun, from_runcrashes) 
                    plt.close()


                    if not secondRun:
                        i -= 1
                        pageno -= 1
                        secondRun = True
                        continue
                    
                    if secondRun:
                        crash = True

                if(flag==1):
                    print("run: success")

                    if(secondRun):
                        del crashlist[-1]

                    ygfil = ygazesfilPlot(cutsUItxt, sub1, exam, text, pageno)
                    xo, yo, average = ygfil[0], ygfil[1], ygfil[2]
                    
                    finalindexes = ShowGazesMakeCuts(sub1, exam, text, pageno, lines, tempx, tempy, xo, yo, average, flag, secondRun, from_runcrashes) 
                    plt.close()
                    finalindexes.sort()
                    
                    cgdata =  CutGazes(text, pageno, roistart, tempindex, tempx, tempy, temptimestamp, finalindexes, roibounds, from_runcrashes)


                    # # # # # OMIT all gazes that are not valid # # # #
                    # cgdata, noshifted_y = clearcutgazes(cgdata, []) 


                    ShowGazesAndCutGazes(text, pageno, tempx, tempy, cgdata[1], cgdata[2], flag)
                    
                    drawROIbounds(sub1, exam, text, pageno, roibounds, cgdata[1], cgdata[2], "rawgazes", [], plt, "close") #In order to draw and save the rawgazes(pageno).png images
                                   

                    gazedata = CreateGazeData(cgdata)

                    #Make cutgazes.txt file
                    MakeGazesTxt(sub1, exam, text, pageno, gazedata)

                
                    # Find Fixations and Make fixations.txt file
                    fixationdata = fixationfun( gazedata )
                    MakeFixationsTxt(sub1, exam, text, pageno, roistart, fixationdata, roibounds)

                
                    # Draw fixations(pane_number).png images
                    drawFixations(sub1, exam, text, fixationdata, pageno, "yes", NULL)

                    # Draw fixations(pane_number).png colored arrows
                    drawEyeMovements(sub1, exam, text, fixationdata, pageno, NULL)
            
                    # Draw cutgazes(pane_number).png images
                    drawROIbounds(sub1, exam, text, pageno, roibounds, cgdata[1], cgdata[2], "cutgazes", fixationdata, NULL, "close") 

                    # Store finalindexes per page 
                    storefinalindexes(sub1, pageno, file, finalindexes) 


                if secondRun:
                    secondRun = False


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


            
    
    if(crashlist!=[]):
        saveCrashList(sub1, text, crashlist, crashtxt)

    if(crash == False):
        concatdata(sub1, exam, text, 'cutgazes', 'fixations')

        textpasstxt = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + '_pass.txt'
        textpassfile = open(textpasstxt, 'w')
        textpassfile.close()

    if(crash == True):
        textcrashtxt = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + '_crash.txt'
        textcrashfile = open(textcrashtxt, 'w')
        textcrashfile.close()




main()