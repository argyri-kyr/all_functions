


from asyncio.windows_events import NULL
import time
import pandas as pd


from ploteyevergencebypage_ofth import ploteyevergencebypage_ofth


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2, guiflag
from GetSomeInitialData import getGazesFolderbyText
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass
from vergence_gui import vergence_gui


#################################################
# INSTALL FFMPEG FIRST
"""
    You need to install ffmpeg first follow the instructions
    from extra_libraries folder.

"""
##################################################



def vergence_ofth_Procedure(subs, texts, pages, startgazesgui, endgazesgui):
    startvergence = time.time()
    
    exam = 1 

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
                        uncutgazesrawpath = folder1 + folder2 + 'subject_' + str(sub) + '/all_data/' + text + str(exam) + '/uncutgazesraw' + str(pageno) + '.xlsx'
                        if( os.path.exists(textpath)  and  os.path.exists(finalindexespath)  and  os.path.exists(uncutgazesrawpath) ):
                            filefound = True
                            break
                                        
                    if( filefound==True ):
                        # # # # # #  collect vergence data  # # # # # # 
                        uncutgazesraw = pd.read_excel(uncutgazesrawpath, header=None)
                        vergenceindex = list(uncutgazesraw.iloc[:,0].values)
                        vergenceleftx = list(uncutgazesraw.iloc[:,1].values)
                        vergencelefty = list(uncutgazesraw.iloc[:,2].values)
                        vergenceleftvalid = list(uncutgazesraw.iloc[:,4].values)
                        vergencerightx = list(uncutgazesraw.iloc[:,5].values)
                        vergencerighty = list(uncutgazesraw.iloc[:,6].values)
                        vergencerightvalid = list(uncutgazesraw.iloc[:,8].values)
                        vergencetimestamp = list(uncutgazesraw.iloc[:,9].values)
                        
                        
                        startgazes = 1
                        endgazes = len(vergenceindex)
                        
                        
                        # # # # # #  collect finalindexes data  # # # # # # #
                        finalindexestxt = folder1 + folder2 + '/subject_' + str(sub) + '/' + textfile + '/py/finalindexes_page' + str(pageno) + '.txt'
                        file = open(finalindexestxt, 'r')
                        lines = file.readlines()
                        for index, line in enumerate(lines):
                            finalindexes.append( int(float(line.strip())) )

                        # # # # # # # # # # # # #  end of collect data  # # # # # # # # # # # # #
                        
                            
                        ploteyevergencebypage_ofth(sub, text, pageno, subexam, vergenceindex, vergenceleftx, vergencelefty, vergenceleftvalid, vergencerightx, vergencerighty, vergencerightvalid, vergencetimestamp, startgazes, endgazes, finalindexes)
                    
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
    

