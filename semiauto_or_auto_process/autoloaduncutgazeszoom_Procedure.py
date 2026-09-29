

from asyncio.windows_events import NULL
import calendar
import time
from os.path import exists
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import statistics
import sys
import datetime
matplotlib.use('Agg')



import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,currentdir)
from pagelinelimitsfun import pagelinelimitsfun
from ShowGazesMakeCuts import ShowGazesMakeCuts
from commonfunctions import CutGazes, ShowGazesAndCutGazes, getpagelines
from concatdata import concatdata
from saveCrash import saveCrashList
from ygazesfilplot import ygazesfilPlot
from storerawdata import storegazedata, storevergencedata, store_pupil_z_data


parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from globalVars import folder1, folder2, textends, dispersion, dispersion2
from basic_function_gui import basic_function_gui
from GetAndDrawROIS import getROIbounds, drawROIbounds
from MakeFixationsFile import MakeFixationsTxt
from MakeGazesFile import MakeGazesTxt
from creategazedata import CreateGazeData
from drawFixations import drawFixations
from fixationfungap import fixationfungap
from drawEyeMovements import drawEyeMovements
from gazeshandling import gazeshandling
from storefinalindexes import storefinalindexes
from loaduncutdata import loaduncutdata
from MakeDispersionTxt import MakeDispersionTxt
from MakePageFixationsGap import MakePageFixationsGap
from load_subs_initial_data import load_subs_initial_data
from make_textfolder_struct import make_textfolder_struct



def autoloaduncutgazeszoom_Procedure(subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye):
    global cutsUItxt, errorcrashtxt, runcrashestxt, secondtimetxt, crashtxt, disparitycounter

    from_runcrashes = False
    disparitycounter = 0
    
    
    start = time.time()
    timestamp = calendar.timegm(time.gmtime())
    

    # Orizw se poia exam einai to kathe subject
    exam = 1
    

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

        # load subjects data, i.e if subject exist and which texts has this subject
        gazesfolders, analysis_texts, textanalysisfiles = load_subs_initial_data(subs[i], exam, texts, from_runcrashes)      
        if( gazesfolders == NULL ):
            continue        
        
        for j in range (len(analysis_texts)):
            text = analysis_texts[j]
            file = textanalysisfiles[j]
            
            # Make the folders (if not exist) that i will use to store graphs and data for my texts
            make_textfolder_struct(subs[i], exam, text)
            
    
            if( (not exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_pass.txt')) and (not exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_crash.txt')) ):
                # Ksekinaei h analysh twn keimenwn 
                proceduredone = False
                Start_Text_Procedure(file, subs[i], exam, text, onlylefteye, onlyrighteye)  # Main procedure of the programme for each text
            
            # elif( (bypass==1) and (exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i]) + '_pass.txt')) ):
            elif( bypass == 1 ):
                # Ksekinaei h analysh twn keimenwn 
                if( os.path.exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_pass.txt')):
                    os.remove(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_pass.txt')
                if( os.path.exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_crash.txt')):
                    os.remove(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_crash.txt')
                
                proceduredone = False
                Start_Text_Procedure(file, subs[i], exam, text, onlylefteye, onlyrighteye)  # Main procedure of the programme for each text
        
        
        
            # Handle some messages
            if(  proceduredone == True and  analysis_texts!=[] ):
                if exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_pass.txt'):
                    print("\nAnalysis has been done for subject=%d and text=%s " % (subs[i], text))
                if exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_crash.txt'):
                    print("\nAnalysis has been PARTIALLY done for subject=%d and text=%s " % (subs[i], text))
                time.sleep(3)
        
        
        if( analysis_texts==[] ):
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
def Start_Text_Procedure(file, sub1,  exam, text, onlylefteye, onlyrighteye):
    global roibounds, disparitycounter
    
    
    from_runcrashes = False
    
    newgazes, vergence_list, vergence_z = gazeshandling(file, sub1)
    
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


                if(secondRun==False):
                    firstruncuts = 0
                else:
                    firstruncuts = run[3]    # afto einai to prohgoumeno run
                
                
                # # # # # # # Catch Errors Occured from pagelinelimits() # # # # # # #
                try:
                    run = pagelinelimitsfun(mypagecollection[1], mypagecollection[2], lines, sub1, exam, text, pageno, cutsUItxt, errorcrashtxt, runcrashestxt, crashlist, secondRun, firstruncuts)
                except:
                    print("eyeRadar: An exception occurred") 
                    exceptionFile = open(folder1 + folder2 + 'subject_' + str(sub1) + '/error_python_101.txt', "a")
                    exceptionFile.write("eyeRadar: An exception occurred_" + str(text) + "_p" + str(pageno))
                    exceptionFile.close()
                    run = [0, [0], 0]
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    

                # run = pagelinelimitsfun(mypagecollection[1], mypagecollection[2], lines, sub1, exam, text, pageno, cutsUItxt, errorcrashtxt, runcrashestxt, crashlist, secondRun, firstruncuts)
                flag = run[1]


                if(flag==0):
                    print("run: failed")

                    crashlist = run[2]
                    if(secondRun==False):
                        if(crashlist!=[]):
                            saveCrashList(sub1, text, crashlist, secondtimetxt)

                    ygfil = ygazesfilPlot(cutsUItxt, sub1, exam, text, pageno)
                    xo, yo, average = ygfil[0], ygfil[1], ygfil[2]
                    
                    finalindexes = ShowGazesMakeCuts(sub1, exam, text, pageno, lines, mypagecollection[1], mypagecollection[2], xo, yo, average, flag, secondRun, from_runcrashes) 
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
                    
                    finalindexes = ShowGazesMakeCuts(sub1, exam, text, pageno, lines, mypagecollection[1], mypagecollection[2], xo, yo, average, flag, secondRun, from_runcrashes) 
                    plt.close()
                    finalindexes.sort()
                    
                    cgdata =  CutGazes(text, pageno, roistart, mypagecollection, finalindexes, roibounds, from_runcrashes)


                    ShowGazesAndCutGazes(text, pageno, mypagecollection[1], mypagecollection[2], cgdata[1], cgdata[2], flag)
                    
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

                
                    # Draw fixations(pane_number).png images
                    print("Creating fixation images with dispersion ", dispersion, "-", dispersion2)
                    drawFixations(sub1, exam, text, fixationdatagap, pageno, "yes", NULL)

                    # Draw fixations(pane_number).png colored arrows
                    drawEyeMovements(sub1, exam, text, fixationdatagap, pageno, NULL)
            
                    # Draw cutgazes(pane_number).png images
                    drawROIbounds(sub1, exam, text, pageno, roibounds, cgdata[1], cgdata[2], "cutgazes", fixationdatagap, NULL, "close") 

                    # Store finalindexes per page 
                    storefinalindexes(sub1, pageno, file, finalindexes) 


                if secondRun:
                    secondRun = False


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




