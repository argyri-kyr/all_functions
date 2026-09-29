

from asyncio.windows_events import NULL
import os
import time
from os.path import exists
from pylab import *
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)



from globalVars import folder1, folder2
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass
from GetAndDrawROIS import getROIbounds
from selectROIS_audio import selectROIS_audio
from loaduncutdata_rois import loaduncutdata_rois
from loadshifteddata import loadshifteddata
from UI_audio import audio_main, getParamAudioUI
from checkValidNotesAudio import checkValidNotes
from audio_define import audio_define
from findnumberoftextpages import findnumberoftextpages


globParams = {}


def rois_audio_Procedure(subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye):

    # Get Subject's Data from an Input Dialogue  

    """
    dial = Dialogue()
    dial.mainloop()

    name = dial.inputDialog[0]
    sub1 = int(dial.inputDialog[1])
    texts = dial.get_text()
    print(texts)
    """

    from_runcrashes = False
   
    setglobParams("file", NULL)
    setglobParams("sub", NULL)
    setglobParams("exam", NULL)
    setglobParams("text", NULL)
    setglobParams("pageno", NULL)
    setglobParams("totalpages", NULL)
    setglobParams("index", NULL)
    setglobParams("x", NULL)
    setglobParams("y", NULL)
    setglobParams("roiselectedpath", NULL)
    setglobParams("wordsselectedpath", NULL)
    setglobParams("notespath", NULL)
    setglobParams("flag_seegazes", 0)       # --1-- for seeing gazes & cutgazes into text with roibounds, --0-- for seeing only text with bounds 
    setglobParams("flag_roischecked", 0)    # rois all checked or all unckecked when start, --0-- for all unchecked, --1-- for all checked
    setglobParams("Xevent", [])
    setglobParams("Yevent", [])
    
    global finalselectedrois

    ##########################################
        

    # Orizw se poia exam einai to kathe subject
    exam = 1
    
    start_page = 1
    
    
    # Kuria while loop gia na trexoun ola ta subject pou thelw ( trexw 1h loop gia ta subject kai 2h eswterikh loop gia ta texts tou subject )
    for i in range(len(subs)): 

        search1 = getGazesFoldersandClass(subs[i])   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/
        if(search1==NULL):
            print("Subject %s doesn't exist" %subs[i])
            print("Path to subject: ", folder1 + folder2 + 'subject_' + str(subs[i]) + '/')
            time.sleep(5)
            continue
        gazesfolders, sub1class, subexam = search1[0], search1[1], search1[2]        
                               
                             
        # Briskw apo ta keimena pou exw epilexei gia poia apo afta exw dedomena wste na kanw thn analysh mono se afta    
        analysis_texts = []
        textanalysisfiles = []
        for text in texts:
            file = getGazesFolderbyText(subs[i], exam, text, gazesfolders, sub1class, from_runcrashes)
            
            if( file != NULL ):
                analysis_texts.append(text)
                textanalysisfiles.append(file)
                
                
        print("\nYour input texts = ", *analysis_texts)
        
        for textno in range(len(analysis_texts)):
            if( ('zoo' not in analysis_texts) and ('visitloud' not in analysis_texts) and ('midfredloud' not in analysis_texts) and ('grkislaloud' not in analysis_texts) and ('grkislaextloud' not in analysis_texts) ):
                print("\nROIS selection only for loud texts (i.e visitloud, midfredloud, grkislaloud, grkislaextloud, ....)\n")
                
            else:
                if( analysis_texts[textno] == 'visitloud' ):
                    totalpages = findnumberoftextpages('visitloud')
                    setglobParams("totalpages", totalpages)
                    text = analysis_texts[textno]
                
                elif( analysis_texts[textno] == 'midfredloud' ):
                    totalpages = findnumberoftextpages('midfredloud')
                    setglobParams("totalpages", totalpages)
                    text = analysis_texts[textno]
                    
                elif( analysis_texts[textno] == 'grkislaloud' ):
                    totalpages = findnumberoftextpages('grkislaloud')
                    setglobParams("totalpages", totalpages)
                    text = analysis_texts[textno]
                    
                elif( analysis_texts[textno] == 'grkislaextloud' ):
                    totalpages = findnumberoftextpages('grkislaextloud')
                    setglobParams("totalpages", totalpages)
                    text = 'grkislaextloud'
                if( analysis_texts[textno] == 'zoo' ):
                    totalpages = findnumberoftextpages('zoo')
                    setglobParams("totalpages", totalpages)
                    text = analysis_texts[textno]
                
                
                file = textanalysisfiles[textno]
                # finalselectedrois = [[[],[]], [[],[]], [[],[]], [[],[]], [[],[]]]
                finalselectedrois = [ [[],[]] for k in range(globParams["totalpages"]) ]
        
                if(  exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_pass.txt') ):
                    # arxikopoihsh merikwn .txt 
                    roiselectedpath = folder1 + folder2 + 'subject_' + str(subs[i]) + '/' + file + '/finalROISselected.txt'
                    open(roiselectedpath, 'a')
                    
                    wordsselectedpath = folder1 + folder2 + 'subject_' + str(subs[i]) + '/' + file + '/decodingErrors.txt'
                    open(wordsselectedpath, 'a')
                    
                    notespath = folder1 + folder2 + 'subject_' + str(subs[i]) + '/' + file + '/My_Audio_Notes.txt'
                    # open(notespath, 'a')
                    
                    setglobParams("roiselectedpath", roiselectedpath), setglobParams("wordsselectedpath", wordsselectedpath), setglobParams("notespath", notespath)
                    
                    # # # # # Arxikopoihsh Hxhtikou # # # # #
                    audiopath = folder1 + folder2 + 'subject_' + str(subs[i]) + '/' + file + '/AudioRecording.wav'
                    audio_define(subs[i], file)
                    # # # # # # # # # # # # # # # # # # # #
                    
                    audio_main(audiopath, previous_page, next_page, getParamAudiomain)
                    
                    
                    # Ksekinaei h diadikasia epiloghs ROIS
                    index, finalraw_x, finalraw_y, timestamp, roi = loaduncutdata_rois(file, subs[i])
                    

                    setglobParams("file", file), setglobParams("sub", subs[i]), setglobParams("exam", exam), setglobParams("text", text), setglobParams("pageno", start_page), setglobParams("index", index), setglobParams("x", finalraw_x), setglobParams("y", finalraw_y)
                    Page_Procedure(subs[i], exam, text, start_page, index, finalraw_x, finalraw_y, globParams["flag_seegazes"], globParams["flag_roischecked"])  # Main procedure of the programme for each text
                    
                    getParamAudioUI("root").mainloop()
                    
                
                else:
                    print("At first you MUST run the analysis for this text with loaduncutgazeszoom_2023 or with autoloaduncutgazeszoom or with an other programme that make cuts.")  
                
        if( analysis_texts==[] ):
            print("\nΝo texts were found for Subject = %d " % [i])
            time.sleep(3)

              
    #Delete unneeded .txts 
    for file in os.listdir():
        if( file.endswith(".txt") ):
            
            if( os.stat(file).st_size==0 ):
                os.remove(file)


def collectrawpagedata(pageno, index, finalraw_x, finalraw_y):
    tempx = []
    tempy = []
    
    count = 0

    #Εδω δημιουργω τις λιστες των δεδομενων ανα σελιδα   
    for i in range(len(index)):
        if( index[i] == 1 ):
            count+=1
        
        if( count == pageno ):
            tempx.append( finalraw_x[i] )
            tempy.append( finalraw_y[i] )
    
    return tempx, tempy
    
    

#Procedure's args ={ (text : text i will analyze), (folder : main folder), (sub1 : subject's id), (sub1class : subject's class) }
def Page_Procedure(sub1,  exam, text, pageno, index, finalraw_x, finalraw_y, flag_seegazes, flag_roischecked):

    tempx, tempy = collectrawpagedata(pageno, index, finalraw_x, finalraw_y)

    if(pageno>0) :
        roibounds = getROIbounds(text, pageno)             # Βρισκω τα ROIbounds του κειμενου
        
        print("\nsubject %d, text %s, page %d " %(sub1, text, pageno))          #Βρισκω τα ROIbounds του κειμενου
                                                        
        shifted_x, shifted_y = loadshifteddata(text, exam, pageno, sub1)
        
        roismain(sub1, exam, text, pageno, roibounds, tempx, tempy, shifted_x, shifted_y, flag_seegazes, flag_roischecked)


    return


def roismain(sub1, exam, text, pageno, roibounds, tempx, tempy, shifted_x, shifted_y, flag_seegazes, flag_roischecked):
    selectROIS_audio(sub1, exam, text, pageno, roibounds, tempx, tempy, shifted_x, shifted_y, flag_seegazes, flag_roischecked, finalselectedrois, setglobParams)
    plt.show()
    return
    


def getParamAudiomain(param):
    d = {"file":globParams["file"], "sub":globParams["sub"], "exam":globParams["exam"], "pageno":globParams["pageno"], "totalpages":globParams["totalpages"], "index":globParams["index"], "x":globParams["x"], "y":globParams["y"], "text":globParams["text"], "groiselectedpath":globParams["roiselectedpath"], "gwordsselectedpath":globParams["wordsselectedpath"], "gnotespath":globParams["notespath"], "Xevent":globParams["Xevent"], "Yevent":globParams["Yevent"], "finalselectedrois":finalselectedrois, "eventdataTofinaldata":eventdataTofinaldata} 
    return d[param]



def setglobParams(paramname, param):
    global globParams
    globParams[paramname] = param


# check if a new ROI is selected and if it is so, then check it is already in finalselectedrois
def eventdataTofinaldata(current_page):
    for j in range(len(globParams["Xevent"])):
        if( (globParams["Xevent"][j] not in finalselectedrois[current_page-1][0]) and (globParams["Yevent"][j] not in finalselectedrois[current_page-1][1]) ):
            finalselectedrois[current_page-1][0] += globParams["Xevent"]
            finalselectedrois[current_page-1][1] += globParams["Yevent"]
    print("finalselectedrois:")
    print("finalselectedrois_page1 = ", finalselectedrois[0])
    print("finalselectedrois_page2 = ", finalselectedrois[1])
    print("finalselectedrois_page3 = ", finalselectedrois[2])
    print("finalselectedrois_page4 = ", finalselectedrois[3])
    print("finalselectedrois_page5 = ", finalselectedrois[4])
    
    return

            


######################################## FUNCTIONS FOR UI ########################################

def getEvent(Eventparam):
    return Eventparam


def previous_page():
    # at first check for wrong notes
    wrongNotes, data1, data2, data3 = checkValidNotes(globParams["text"], getParamAudioUI)
    if(wrongNotes):
        return
    
    plt.close('all')
    
    current_page = globParams["pageno"]
    
    # eventdataTofinaldata(current_page)
    
    current_page -= 1
    
    if( current_page == 0 ):
        current_page = globParams["totalpages"]
    
    setglobParams("pageno", current_page)
    
    Page_Procedure(globParams["sub"], globParams["exam"], globParams["text"], globParams["pageno"], globParams["index"], globParams["x"], globParams["y"], globParams["flag_seegazes"], globParams["flag_roischecked"])
    return


def next_page():
    # at first check for wrong notes
    wrongNotes, data1, data2, data3 = checkValidNotes(globParams["text"], getParamAudioUI)
    if(wrongNotes):
        return
    
    plt.close('all')
    
    current_page = globParams["pageno"]

    # eventdataTofinaldata(current_page)
    
    current_page += 1
    
    if( current_page == globParams["totalpages"]+1 ):
        current_page = 1
    
    setglobParams("pageno", current_page)

    Page_Procedure(globParams["sub"], globParams["exam"], globParams["text"], globParams["pageno"], globParams["index"], globParams["x"], globParams["y"], globParams["flag_seegazes"], globParams["flag_roischecked"])    
    return

    
