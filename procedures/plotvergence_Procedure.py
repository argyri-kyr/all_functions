
from asyncio.windows_events import NULL
import time

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2
from GetSomeInitialData import getGazesFolderbyText
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass
from ploteyevergencebypage import ploteyevergencebypage



def plotvergence_Procedure(subs, texts, pages, startgazesgui, endgazesgui):
    startvergence = time.time()

    from_runcrashes = True
    
    
    for sub in subs:
        filefound = False
        search1 = getGazesFoldersandClass(sub)
        if(search1==NULL):
            print("Subject %d doesnt exist" % sub)
            time.sleep(3)
            continue
        gazesfolders, sub1class, subexam = search1[0], search1[1], int(search1[2])


        for text in texts:
            # # # # # # find textfile with vergence data # # # # # #
            textfolder = getGazesFolderbyText(sub, subexam, text, gazesfolders, sub1class, from_runcrashes)

            if( textfolder!=NULL ):
                for pageno in pages:
                    finalindexes = []
                    filefound = False

                    for textfile in textfolder:    
                        textpath = folder1 + folder2 + 'subject_' + str(sub) + '/' + textfile + '/py/gazes_page' + str(pageno) + '.txt'   
                        finalindexespath = folder1 + folder2 + 'subject_' + str(sub) + '/' + textfile + '/py/finalindexes_page' + str(pageno) + '.txt'   
                        vergencepath = folder1 + folder2 + '/subject_' + str(sub) + '/' + textfile + '/py/vergence_page' + str(pageno) + '.txt'
                        if( os.path.exists(textpath) and os.path.exists(finalindexespath) and  os.path.exists(vergencepath) ):
                            filefound = True
                            break
                                        
                    if( filefound==True ):
                        # # # # # #  collect vergence data  # # # # # # 
                        vergencefilepath = open(vergencepath, 'r')
                        lines = vergencefilepath.readlines()
                        vergenceindex = []
                        vergenceleftx = []
                        vergencelefty = []
                        vergencerightx = []
                        vergencerighty = []
                        vergencetimestamp = []
                        for p in lines:
                            vergenceindex.append( int(p.split(None)[0]) ) 
                            vergenceleftx.append( float(p.split(None)[1]) ) 
                            vergencelefty.append( float(p.split(None)[2]) ) 
                            vergencerightx.append( float(p.split(None)[3]) ) 
                            vergencerighty.append( float(p.split(None)[4]) ) 
                            vergencetimestamp.append( float(p.split(None)[5]) )

                        # # # # # #  collect finalindexes data  # # # # # # #
                        finalindexestxt = folder1 + folder2 + '/subject_' + str(sub) + '/' + textfile + '/py/finalindexes_page' + str(pageno) + '.txt'
                        file = open(finalindexestxt, 'r')
                        lines = file.readlines()
                        for index, line in enumerate(lines):
                            finalindexes.append( int(float(line.strip())) )

                        # # # # # # # # # # # # #  end of collect data  # # # # # # # # # # # # #


                        # # # # # # #  start main process  # # # # # # #
                        if( startgazesgui=='' ):
                            startgazes = finalindexes[0]
                        else:
                            startgazes = startgazesgui

                        if( endgazesgui=='' ):
                            endgazes = finalindexes[-1]
                        else:
                            endgazes = endgazesgui
                            
                        ploteyevergencebypage(sub, text, pageno, subexam, vergenceindex, vergenceleftx, vergencelefty, vergencerightx, vergencerighty, vergencetimestamp, startgazes, endgazes, finalindexes)
                    
                    else:
                        print("\nNo folder or appropriate folder structure was found for subject=%d, text=%s, page=%d" % (sub, text, pageno))
            else:
                print("\nNo data for subject=%d in text=%s" % (sub, text))
            
        endvergence = time.time()
        t1 = endvergence - startvergence

        hours = int(t1/3600)
        t1 = t1 - (hours*3600)
                
        minutes = int(t1/60)
        t1 = t1 - (minutes*60)
                
        seconds = t1

        print("\nVergence plot time:")
        print("Hours:", hours, "  Minutes:", minutes, "  Seconds:", seconds, "\n")
    

