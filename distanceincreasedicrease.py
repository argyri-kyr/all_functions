



from asyncio.windows_events import NULL
import os
import time
import shutil
import math
import matplotlib.pyplot as plt
from datetime import datetime
import xlsxwriter

# from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)


from globalVars import folder1, folder2, pyimagepath, guiflag
from basic_function_gui import basic_function_gui
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass
from createSubfile import createSubfile
from loaduncutdata_horizontal_eyeposition import loaduncutdata_horizontal_eyeposition


def main1():

    # Get Subject's Data from an Input Dialogue  

    global from_runcrashes
    
    from_runcrashes = False

    
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
        texts = ['visitloud', 'midfredloud']
        # texts = ['zoo', 'visit', 'efeyreseis', 'olympia', 'morning', 'zebra', 'visitloud']
        
        # subs = [1455, 1456, 1459, 1460, 1461]
        # subs = [ person  for person  in range(908, 920) ]
        # subs = [x for x in range(13001, 13021)]
        # subs = [13003, 13017, 13044, 13054, 13058, 13066, 13070, 13086, 13105, 13108, 13158, 13161, 13166, 13167, 13172, 13178, 13198, 13203, 13209, 13222, 13234]
        # subs = [1638, 1482, 13032]
        # subs = [1488, 1490, 1424, 1431, 1441, 1461, 1482, 1531, 1532, 1580, 1632]   #ofthalmos list, me exophoria oi 5 teleftaioi
        subs = [1621, 1636, 1638, 1482, 1531, 1532, 1632, 1424, 1428, 1429, 1431]
        
        bypass = 1
        hardcases = 0
        onlylefteye = 0
        onlyrighteye = 0
        firstchoices = [bypass, hardcases, onlylefteye, onlyrighteye]


    # Orizw se poia exam einai to kathe subject
    exam = []
    
    

    # Kuria while loop gia na trexoun ola ta subject pou thelw ( trexw 1h loop gia ta subject kai 2h eswterikh loop gia ta texts tou subject )
    for i in range(len(subs)): 
    
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
            
        
        if( analysis_texts==[] ):
            print("\nΝo texts were found for Subject = %d " % subs[i])
            time.sleep(3)
        
         
              
    #Delete unneeded .txts 
    for file in os.listdir():
        if( file.endswith(".txt") ):
            if( os.stat(file).st_size==0 ):
                os.remove(file)





#Procedure's args ={ (text : text i will analyze), (folder : main folder), (sub1 : subject's id), (sub1class : subject's class) }
def Procedure(file, sub1,  exam, text, onlylefteye, onlyrighteye):
    
    # Create excel to save data
    workbook = xlsxwriter.Workbook(folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/py/countdistances.xlsx')
    worksheet = workbook.add_worksheet()
    
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
                                                              
                countincrease, countdicrease, countequal = diagonal_eyeposition(templeftx, temprightx, templefty, temprighty ,templeftvalid, temprightvalid)
                worksheet.write_row(pageno-1, 0, [countincrease, countdicrease, countequal])
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
        

        # Collect and clear data at once
        if( i != len(index) ):

            if( uncutgazesraw!=[] ):
                tempindex.append( index[i] )
                
                if( leftvalid[i]==1 and rightvalid[i]==1 ):
                    templeftx.append( leftx[i] )
                    templefty.append( lefty[i] )
                    temprightx.append( rightx[i] )  
                    temprighty.append( righty[i] ) 
                else:
                    templeftx.append( 0 )
                    templefty.append( 0 )
                    temprightx.append( 0 )  
                    temprighty.append( 0 ) 
                    
                templeftvalid.append( leftvalid[i] )
                temprightvalid.append( rightvalid[i] )  
                temptimestamp.append( timestamp[i] )        
    
    workbook.close()




def diagonal_eyeposition(leftx, rightx, lefty, righty, leftvalidity, rightvalidity):
    # calculate disparity
    disparity = []
    for i in range(len(leftx)):
        distance = math.sqrt( (rightx[i]-leftx[i])**2 + (righty[i]-lefty[i])**2 )
        disparity.append( distance )

    # Clear disparity from non valid data
    cleardisparity = []
    for i in range(len(disparity)):
        if( disparity[i]==0 and (leftvalidity[i]==0 or rightvalidity[i]==0) ):
            continue
        else:
            cleardisparity.append(disparity[i])
    
    # Count increases, dicreases or equal situations, among one gaze distance to the next gaze distance   
    countincrease = 0
    countdicrease = 0
    countequal = 0
    distance1 = cleardisparity[0]
    for i in range(1, len(cleardisparity)):
        distance2 = cleardisparity[i]
        if( distance1-distance2 < 0 ):
            countdicrease += 1
        elif( distance1-distance2 > 0 ):
            countincrease += 1
        elif( distance1-distance2 == 0 ):
            countequal += 1

        distance1 = distance2
                

    
    return countincrease, countdicrease, countequal
    
main1()