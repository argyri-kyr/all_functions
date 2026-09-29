
from asyncio.windows_events import NULL
import fnmatch
import calendar
import glob
import time
from tkinter.messagebox import askyesno
import ctypes
from matplotlib import pyplot as plt
from win32comext.shell import shell, shellcon
from os.path import exists
from playsound import playsound
import pandas as pd



from commonfunctions_2020_rev2 import CutGazes, ShowGazesAndCutGazes, getpagelines



import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2, textends
from GetAndDrawROIS import getROIbounds, drawROIbounds
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass
from MakeFixationsFile import MakeFixationsTxt
from MakeGazesFile import MakeGazesTxt
from creategazedata import CreateGazeData
from drawFixations import drawFixations
from fixationfun import fixationfun
from drawEyeMovements import drawEyeMovements
from storefinalindexes import storefinalindexes
from GazesPreview import GazesPreview


from semiauto_or_auto_process.ShowGazesMakeCuts import ShowGazesMakeCuts
from semiauto_or_auto_process.concatdata import concatdata
from semiauto_or_auto_process.ygazesfilplot import ygazesfilPlot


class DictList(dict):
    def __setitem__(self, key, value):
        try:
            # Assumes there is a list on the key
            self[key].append(value)
        except KeyError: # If it fails, because there is no key
            super(DictList, self).__setitem__(key, value)
        except AttributeError: # If it fails because it is not a list
            super(DictList, self).__setitem__(key, [self[key], value])


#Sinartisi opou epistrefei listes( subs, exams, texts, pages ) pou periexoun ta subjects pou ekanan crash kai plhrofories gia to keimeno kai th selida sto opoio egine to fail kai se poia exam einai to subject 
def runcrashcases(filetxt):
    file = open(filetxt)
    
    subs = []
    exams = []
    texts = []
    pages = []
    findsubject = False
    findexam = False
    findtext = False
    findpage = False
    
    for line in file:
        for word in line.split():
            if(word == "Subject"):
                findsubject = True
                continue
            if(word == "Exam"):
                findexam = True
                continue
            if(word == "Text"):
                findtext = True
                continue
            if(word == "Page"):
                findpage = True
                continue
            
            
            if(findsubject == True):
                sub1 = int(word)
                subs.append(sub1)
                findsubject = False
            if(findexam == True):
                exam = int(word)
                exams.append(exam)
                findexam = False
            if(findtext ==True):
                text = word
                texts.append(text)
                findtext = False
            if(findpage == True):
                page = int(word)
                pages.append(page)
                findpage = False
                
        
    return subs, exams, texts, pages
 

def createtemplists(file):
    countwords=-1
    tempindex = []
    tempx = []
    tempy = []
    temptimestamp = []
    checkx = False
    checky = False
    for line in file:
        countwords=-1
        for word in line.split():
            countwords+=1
            if(countwords == 0):
                tempindex.append(word)
            if(countwords == 1):
                checkx = word
                tempx.append(word)
            if(countwords == 2):
                checky = word
                tempy.append(word)    
            if(countwords == 3):
                temptimestamp.append(word)
    
 
    return tempindex, tempx, tempy, temptimestamp


#Confirmation dialogue
def confirm():
    answer = askyesno(title='confirmation',
                    message='Accept cut?')
    
    if (answer==False):
        window.destroy()
        plt.close()
        
    return answer


#Sort cut points(kiklakia). Taxinomw ta x-indexes kai analoga th thesi mesa sth lista pou tha mpei to kathe x tha paw meta kai sthn idia thesi tha balw to antistoixw y-index aftou tou x, etsi wste ta shmeia (x,y) na einai kai pali sto telos ta idia ana thesi mesa stis listes.
def mySort(x,y):
    for i in range(len(x)):
        min_value = min(x[i:])
        min_index = x.index(min_value)
        x[i], x[min_index] = x[min_index], x[i]
        y[i], y[min_index] = y[min_index], y[i]
    
    return x,y


#Delete and move it to Recycle Bin
def deltorecyclebin(filename):
    if not os.path.exists(filename):
        return True
    res= shell.SHFileOperation((0,shellcon.FO_DELETE,filename,None, shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,None,None))
    if not res[1]:
        os.system('del '+filename)


#Copy subject's crashes data that doesn't exist into individual folder from << for_runcrashes_'timestamp'.txt >> to a new << for_runcrashes_'timestamp'.txt >> file
def copySubsdata(file, sub, exam, text, pageno):
    timestamp = calendar.timegm(time.gmtime())
    file = open(file)
    
    runcrashestxt = folder1 + 'for_runcrashes_' + str(timestamp) + '.txt'
    runcrashesfile = open(runcrashestxt, 'a+')
    
    found = False
    for line in file:
        for word in line.split():
            if(word == "Subject"):  
                if(line == "Subject %d Exam %d Text %s Page %d\n" %(sub, exam, text, pageno)):
                    found = True
                    break
                else:
                    found = False
                    break
        if(found == True):
            runcrashesfile.write(line)
        
        else:
            continue


def main():
    flag = 0
    crash = False
    from_runcrashes = True
    global window

    collection = []
    for file in os.listdir(folder1):
        if (fnmatch.fnmatch(file , 'for_runcrashes_' + '*')):
            collection.append(file)

    for file in collection:
        crash = True

        file2 = folder1 + file
        run1 = runcrashcases(file2)
        subs = run1[0]
        exams = run1[1]
        texts = run1[2]
        pages = run1[3]
            
            
        for i in range(len(subs)):

            #Briskw to fakelo(for example)->  /Radar_Iro_copy/individual/subject_729/ag_729_1_zoo_wa_2_7_2022-02-22-04.05.05/py , etsi  wste na paw apo ekei mesa na parw ta gazes ana selida pou tha xreiastw parakatw wste na kanw thn analysh
            run2 = getGazesFoldersandClass(subs[i])
               
            if( run2==NULL ):
                print("\nSubject %d does't exist" %subs[i])
                copySubsdata(file, subs[i], exams[i], texts[i], pages[i])
                continue
                
            if( exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + texts[i] + str(exams[i]) + '_pass.txt')):
                print("\nSubject %d With Text %s in Page %d has been done" %(subs[i],texts[i],pages[i]))
                continue
            
            if( not exists (folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + texts[i] + str(exams[i]) + '_page' + str(pages[i]) +  '_pass.txt') ):
                print("\nsubject %s, text %s, page %d" %(subs[i], texts[i], pages[i]))
                gazesfolders, sub1class, subexam = run2[0], run2[1], run2[2]
                        
                #Αδειαζω τις λιστες που περιεχουν τα δεδομενα της σελιδας που επεξεργαστηκα, ωστε να αποθηκευσω τα νεα δεδομενα της επομενης σελιδας
                tempindex = []
                tempx = []
                tempy = []
                temptimestamp = []

                for text in texts:
                    textfolder = getGazesFolderbyText(subs[i], exams[i], texts[i], gazesfolders, sub1class, from_runcrashes)

                for textfile in textfolder:    
                    textpath = folder1 + folder2 + 'subject_' + str(subs[i]) + '/' + textfile + '/py/gazes_page' + str(pages[i]) + '.txt'   
                    if(  os.path.exists(textpath) ):
                        filepath = open(textpath)
                        break
                        
                array = createtemplists(filepath)
                tempindex = list(map(int, array[0]))
                tempx = list(map(float, array[1]))
                tempy = list(map(float, array[2]))
                temptimestamp = list(map(float, array[3]))

                mypagecollection = [tempindex, tempx, tempy, temptimestamp]
                        

                #Briskw lines kai roibounds 
                lines = getpagelines(texts[i], pages[i])                     #Βρισκω ποσες γραμμες εχει η σελιδα οπου βρισκομαι
                
                roibounds = getROIbounds(texts[i], pages[i]) 
                
                roistartpath = folder1 + 'texts/' + texts[i] + textends + '/py/mytext/page(' + str(pages[i]) + ')/ROIstart/ROIstart.xlsx'
                roistart = pd.read_excel(roistartpath, header=None).values[0][0]

                #Paw na brw telika poia tha einai ta kopsimata mou (x,y)
                        
                #H ygazesfilPlot mou epistrefei ta lanthasmena kopsimata(x,y)  pou exoun ginei
                ygfil = ygazesfilPlot(file2, subs[i], exams[i], texts[i], pages[i])

                x, y, average = ygfil[0], ygfil[1], ygfil[2]

                # # # # # clear x,y from doubles # # # # #
                for index in range(len(x)-1):
                    if( x[index] in x[index+1:] ):
                        del x[index]
                        del y[index]
                # # # # # end clear # # # # #
                        
                secondRun = True # Kathws exei ginei se oles tis apotuxhmenes periptwseis secondRun

                global g
                g, G_ax = GazesPreview(texts[i], pages[i], mypagecollection)
                finalindexes, cgdata, answer, f = mainProcedure_firstcheck(subs[i], exams[i], texts[i], pages[i], lines, tempindex, tempx, tempy, temptimestamp, x, y, roistart, roibounds, average, flag, secondRun, from_runcrashes)
                    
                while( answer == False ):  #Εαν η απαντηση ειναι 'οχι' τοτε ξανακανω την προηγουμενη διαδικασια
                    plt.close('all')

                    g, G_ax = GazesPreview(texts[i], pages[i], mypagecollection)
                    finalindexes, cgdata, answer, f = mainProcedure_firstcheck(subs[i], exams[i], texts[i], pages[i], lines, tempindex, tempx, tempy, temptimestamp, x, y, roistart, roibounds, average, flag, secondRun, from_runcrashes)
                        
                if(answer == True):
                    f.set_size_inches(13.66, 7.68)
                    drawROIbounds(subs[i], exams[i], texts[i], pages[i], roibounds, cgdata[1], cgdata[2], "rawgazes", [], plt, "close") #In order to draw and save the rawgazes(pageno).png images
                    plt.close('all')
                    window.destroy()
                            
                window.mainloop()

                    
                gazedata = CreateGazeData(cgdata)

                #Make cutgazes.txt file
                MakeGazesTxt(subs[i], exams[i], texts[i], pages[i], gazedata)

                                
                #Find Fixations and Make fixations.txt file
                fixationdata = fixationfun( gazedata )
                MakeFixationsTxt(subs[i], exams[i], texts[i], pages[i], roistart, fixationdata, roibounds)

                                
                #Draw fixations(pane_number).png images
                drawFixations(subs[i], exams[i], texts[i], fixationdata, pages[i], "yes", NULL)

                #Draw fixations(pane_number).png colored arrows
                drawEyeMovements(subs[i], exams[i], texts[i], fixationdata, pages[i], NULL)

                            
                #Draw cutgazes(pane_number).png images
                drawROIbounds(subs[i], exams[i], texts[i], pages[i], roibounds, cgdata[1], cgdata[2], "cutgazes", fixationdata, NULL, "close") 
            

                storefinalindexes(subs[i], pages[i], textfile, finalindexes[0])


                textpasstxt = folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + texts[i] + str(exams[i]) + '_page' + str(pages[i]) +  '_pass.txt'
                textpassfile = open(textpasstxt, 'w')
                textpassfile.close()
                


        dl = DictList()
        for i in range(len(subs)):
            if(subs[i] not in dl.keys()):
                dl[subs[i]]  = [ [texts[i], exams[i]] ]
            else:
                if( [texts[i], exams[i]]  not in dl[subs[i]] ):
                    dl[subs[i]] = [texts[i], exams[i]]
                    
        print("dl = ",dl)

        for sub in dl:

            mypath = folder1 + folder2 + 'subject_' + str(sub) + '/'
            if not os.path.exists(mypath):
                continue

            sublist = list(dl[sub])
            for j in range(len(dl[sub])):
                text = sublist[j][0]
                exam = sublist[j][1]

                concat = concatdata(sub, exam, text, 'cutgazes', 'fixations')

                if(concat!=NULL):
                    delrest = folder1 + folder2 + 'subject_' + str(sub) + '/all_graphs/' + text + str(exam) + '*.txt'
                    for f in glob.glob(delrest):
                        os.remove(f)
                    

                    textpasstxt = folder1 + folder2 + 'subject_' + str(sub) + '/all_graphs/' + text + str(exam) + '_pass.txt'
                    textpassfile = open(textpasstxt, 'w')
                    textpassfile.close()
                    

          
        deltorecyclebin( file2 )
    
        playsound('C:\Windows\Media\Ring06.wav')
    
    if(crash == False):
        print("\nNo crashes to run")
        time.sleep(3) # Sleep for 3 seconds



def mainProcedure_firstcheck(sub, exam, text, pageno, lines, tempindex, tempx, tempy, temptimestamp, x, y, roistart, roibounds, average, flag, secondRun, from_runcrashes):

    # Kalw thn ShowGazesMakeCuts prokeimenou na kanw ta kopsimata me to xeri ekei pou thelw egw
    finalindexes = ShowGazesMakeCuts(sub, exam, text, pageno, lines, tempx, tempy, x, y, average, flag, secondRun, from_runcrashes) 

    while( len(finalindexes[0])!=lines+1 ):
        print("Wrong Cut.You made only %d cuts.You need %d more." %(len(finalindexes[0]), lines+1 - len(finalindexes[0])))
        ctypes.windll.user32.MessageBoxW(0, "You need more cuts", "Warning!", 16)

        finalindexes = ShowGazesMakeCuts(sub, exam, text, pageno, lines, tempx, tempy, x, y, average, flag, secondRun, from_runcrashes) 
    
    x , y = finalindexes[0] , finalindexes[1]
    mySort(x,y)
    # plt.savefig(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + texts[i] + str(exams[i]) + '/linesteps' + str(pages[i]) + '.png')

    print("x = ",x)
    cgdata =  CutGazes(text, pageno, roistart, tempindex, tempx, tempy, temptimestamp, x, roibounds, from_runcrashes)

    # # # # # OMIT all gazes that are not valid # # # #
    # cgdata, noshifted_y = clearcutgazes(cgdata, []) 

    run3 =  ShowGazesAndCutGazes(text, pageno, tempx, tempy, cgdata[1], cgdata[2], flag)

    global window
    f = run3[0]
    window = run3[1]
            
    answer = confirm()
    
    return finalindexes, cgdata, answer, f


main()