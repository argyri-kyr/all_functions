


from asyncio.windows_events import NULL
import time
import pandas as pd


import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2, textends
from GetSomeInitialData import getGazesFolderbyText
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass
from ploteyefixations_window import ploteyefixations_window



def plotfixation_window_Procedure(subs, texts, pages):
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
                        
                        # # # # # # Collect fixation data  # # # # # # #
                        fixationfilepath = open(fixationspagetxt_final, 'r')
                        lines = fixationfilepath.readlines()
                        fixationx = []
                        fixationy = []
                        fixationduration = []
                        fixationroi = []
                        for p in lines:
                            fixationx.append( int(p.split(None)[1]) ) 
                            fixationy.append( float(p.split(None)[2]) ) 
                            fixationduration.append( float(p.split(None)[4]) ) 
                            fixationroi.append( int(p.split(None)[5]) ) 
                        # # # # # # # # # # # # #  end of collect data  # # # # # # # # # # # # #

                        
                        # # # # # # # # # # # # Define Yline according to Roi # # # # # # # # # # # #
                        
                        # 1st: read yline
                        ylinepath = folder1 + 'texts/' + text + textends + '/py/Yline/mytext.page(' + str(pageno) + ').line.yline.xlsx'
                        ylinedata = pd.read_excel(ylinepath)
                        ylinedata = ylinedata.iloc[:,0].values.tolist()
                        
                        # 2nd: read rois_lines file
                        roislinespath = folder1 + 'texts/' + text + textends + '/py/mytext/page(' + str(pageno) + ')/Rois_Lines.xlsx'
                        roislinesdata = pd.read_excel(roislinespath, header=None)
                        roisdata = roislinesdata.iloc[:,0].values.tolist()
                        linesdata = roislinesdata.iloc[:,1].values.tolist()
                        
                        RoisLines = dict(zip(roisdata, linesdata))
                        
                        # find yline, according to roi's line
                        fixationyline = []
                        for indexmyroi in range(len(fixationroi)):
                            myroi = fixationroi[indexmyroi]
                            if( myroi==-1 ):
                                fixationyline.append( fixationy[indexmyroi] )
                            else:
                                myline = RoisLines[myroi]
                                fixationyline.append( ylinedata[myline-1] )
                        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
                        
                    
                            
                        # # # # # # # # # # # # # # # #   PLOT EYE FIXATIONS   # # # # # # # # # # # # # # # #    
                        ploteyefixations_window(sub, text, pageno, subexam, fixationx, fixationyline, fixationduration)    # ploteyefixations_window(sub, text, pageno, subexam, fixationx, fixationy, fixationduration)
                    
                    else:
                        print("\n\nNo folder or appropriate folder structure was found for subject=%d, text=%s, page=%d" % (sub, text, pageno))
            else:
                print("\n\nNo data for subject=%d in text=%s" % (sub, text))


