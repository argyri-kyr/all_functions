from asyncio.windows_events import NULL
from scipy.fftpack import fft, ifft
import os
import time
import shutil
from os.path import exists
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)


from globalVars import folder1, folder2, pyimagepath, guiflag
from basic_function_gui import basic_function_gui
from GetSomeInitialData import createextra, getGazesFolderbyText, getGazesFoldersandClass
from createSubfile import createSubfile
from loaduncutdata_fastfourier_data import loaduncutdata_fastfourier_data




def main1():

    # Get Subject's Data from an Input Dialogue  

    global from_runcrashes
    from_runcrashes = False


    # Replace no valid gazes with valid
    global nonvalid2valid
    nonvalid2valid = 0   # 0 for do nothing, 1 for replace
    ###################################
    
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
        # texts = ['visit', 'zoo', 'morning', 'visitloud']
        # texts = ['testapartf3' ]
        texts = ['midfred', 'visit', 'sunny', 'zoo', 'visitloud', 'midfredloud']
        
        # subs = [1455, 1456, 1459, 1460, 1461]
        # subs = [ person  for person  in range(908, 920) ]
        # subs = [x for x in range(13100, 13103)]
        subs = [1424, 1428, 1429, 1431, 1441, 1461, 1505, 1512, 1513, 1541, 1655, 1482, 1531, 1532, 1632]
        
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
            
            if not os.path.exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i]) + '/py/extra_plots'):
                os.makedirs(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam[i]) + '/py/extra_plots')
                
                
    
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







#Procedure's args ={ (text : text i will analyze), (folder : main folder), (sub1 : subject's id), (sub1class : subject's class) }
def Procedure(file, sub1,  exam, text, onlylefteye, onlyrighteye):
    # Load Gazes Data 
    uncutgazesraw, uncutgazes, oneeyeindexes = loaduncutdata_fastfourier_data(text, file, sub1, onlylefteye, onlyrighteye)

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
                
                distance = finddistance(templeftx, templefty, temprightx, temprighty)
                fastfourier_analysis(sub1, exam, text, pageno, distance)
        
                    
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
    
    

def fastfourier_analysis(sub1, exam, text, pageno, mylist):
    X = fft(mylist)
    N = len(X)
    n = np.arange(N)
    # get the sampling rate
    sr = 90
    T = N/sr
    freq = n/T 

    # Get the one-sided specturm
    n_oneside = N//2
    # get the one side frequency
    f_oneside = freq[:n_oneside]

    plt.figure(figsize = (12, 6))
    plt.plot(f_oneside, np.abs(X[:n_oneside]), 'b')
    plt.xlabel('Freq (Hz)')
    plt.ylabel('FFT Amplitude |X(freq)|')
    # plt.show()
    plt.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/extra_plots/fastfourier_plot1_AND_' + str(pageno) + '.png', dpi=100)

    
    t_s = 1/f_oneside

    plt.figure(figsize=(12,6))
    plt.plot(t_s, np.abs(X[:n_oneside])/n_oneside)
    plt.xlabel('Period ($seconds$)')
    # plt.show()
    plt.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/extra_plots/fastfourier_plot2_AND_' + str(pageno) + '.png', dpi=100)

    


    
def fastfouries_analysis2(mylist):
    # compute DFT with optimized FFT 
    w = np.fft.fft(mylist)
    
    # compute frequency associated 
    # with coefficients 
    freqs = np.fft.fftfreq(len(mylist))
    
    # extract frequencies associated with FFT values 
    for coef, freq in zip(w, freqs): 
        if coef: 
            print('{c:>6} * exp(2 pi i t * {f})'.format(c=coef, 
                                                        f=freq)) 



def finddistance(leftx, lefty, rightx, righty):
    distance = []
    for i in range(len(leftx)):
        distance.append( np.sqrt( (leftx[i]-rightx[i])**2 + (lefty[i]-righty[i])**2 ) )
    
    return distance


main1()