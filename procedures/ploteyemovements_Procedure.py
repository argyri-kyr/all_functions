
from asyncio.windows_events import NULL
import time


import os,sys,inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2
from GetSomeInitialData import getGazesFolderbyText
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass
from ploteyemovements import plotEyeMovements



#################################################
# INSTALL FFMPEG FIRST
"""
    You need to install ffmpeg first follow the instructions
    from extra_libraries folder.

"""
##################################################



def ploteyemovements_Procedure(subs, texts, pages):
    starteyemovementsplot = time.time()

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
                    filefound = False
   
                    fixationspagetxt_final = folder1 + folder2 + 'subject_' + str(sub) + '/all_data/' + text + str(subexam) + '/fixationspy' + str(pageno) + '.txt' 
                        
                    if( os.path.exists(fixationspagetxt_final) ):
                        filefound = True
                
                                        
                    if( filefound==True ):
                        # # # # # # collect vergence data  # # # # # # #
                        fixationfilepath = open(fixationspagetxt_final, 'r')
                        lines = fixationfilepath.readlines()
                        fixationx = []
                        fixationy = []
                        fixationduration = []
                        for p in lines:
                            fixationx.append( int(p.split(None)[1]) ) 
                            fixationy.append( float(p.split(None)[2]) ) 
                            fixationduration.append( float(p.split(None)[4]) ) 
            

                        # # # # # # # # # # # # #  end of collect data  # # # # # # # # # # # # #

                        # # # # # # # # # # # # # # # #   PLOT EYE FIXATIONS   # # # # # # # # # # # # # # # #    
                        plotEyeMovements(sub, subexam, text, pageno, fixationx, fixationy)
                    
                    else:
                        print("\n\nNo folder or appropriate folder structure was found for subject=%d, text=%s, page=%d" % (sub, text, pageno))
            else:
                print("\n\nNo data for subject=%d in text=%s" % (sub, text))
            
        endeyemovementsplot = time.time()
        t1 = endeyemovementsplot - starteyemovementsplot

        hours = int(t1/3600)
        t1 = t1 - (hours*3600)
                
        minutes = int(t1/60)
        t1 = t1 - (minutes*60)
                
        seconds = t1

        print("\nVergence plot time:")
        print("Hours:", hours, "  Minutes:", minutes, "  Seconds:", seconds, "\n")




