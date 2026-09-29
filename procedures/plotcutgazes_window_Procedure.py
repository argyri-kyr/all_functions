


from asyncio.windows_events import NULL
import time
import pandas as pd
from moviepy.editor import VideoFileClip, concatenate_videoclips


import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2, textends
from GetSomeInitialData import getGazesFolderbyText
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass
from ploteyecutgazes_window import ploteyecutgazes_window



def plotcutgazes_window_Procedure(subs, texts, pages):
    from_runcrashes = True
    
    for sub in subs: 
        mergecheck = True
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
                    
                    cutgazespagetxt_final = folder1 + folder2 + 'subject_' + str(sub) + '/all_data/' + text + str(subexam) + '/cutgazespy' + str(pageno) + '.txt' 
                        
                    if( os.path.exists(cutgazespagetxt_final) ):
                        filefound = True
                
                                        
                    if( filefound==True ):
                        
                        # # # # # # # # # # # Collect cutgazes data  # # # # # # # # # # # #
                        cutgazesfilepath = open(cutgazespagetxt_final, 'r')
                        lines = cutgazesfilepath.readlines()
                        cutgazesindex = []
                        cutgazesx = []
                        cutgazesy = []
                        cutgazesroi = []
                        for p in lines:
                            cutgazesindex.append( int(p.split(None)[0]) ) 
                            cutgazesx.append( int(float(p.split(None)[1])) ) 
                            cutgazesy.append( int(float(p.split(None)[2])) ) 
                            cutgazesroi.append( int(p.split(None)[4]) ) 
                        # # # # # # # # # # # # #  end of collect data  # # # # # # # # # # # # 
                        

                        # # # # # # # # # Fill data at the Beginning and at the End to fit the data as size with gaze's size # # # # # # #
                        
                        # Fill at the Beginning
                        startindex = cutgazesindex[0]
                        for ino in range(1, startindex):
                            cutgazesindex.insert(ino-1, ino)
                            cutgazesx.insert(ino-1, None)
                            cutgazesy.insert(ino-1, None)
                            cutgazesroi.insert(ino-1, -1)
                        
                        # Fill at the End
                        gazesfilepath = folder1 + folder2 + 'subject_' + str(sub) + '/' + textfolder[0] + '/py/gazes_page' + str(pageno) + '.txt' 
                        gazesfile = open(gazesfilepath,"r")
                        lines = len(gazesfile.readlines())
                        endindex = cutgazesindex[-1]
                        for ino in range(endindex+1, lines+1):
                            cutgazesindex.insert(ino-1, ino)
                            cutgazesx.insert(ino-1, None)
                            cutgazesy.insert(ino-1, None)
                            cutgazesroi.insert(ino-1, -1)
                        
                        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  # # # # # # # # # # # #
                        
                        
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
                        cutgazesyline = []
                        for indexmyroi in range(len(cutgazesroi)):
                            myroi = cutgazesroi[indexmyroi]
                            if( myroi==-1 ):
                                cutgazesyline.append( cutgazesy[indexmyroi] )
                            else:
                                myline = RoisLines[myroi]
                                cutgazesyline.append( ylinedata[myline-1] )
                        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
                        
                    
                            
                        # # # # # # # # # # # # # # # #   PLOT EYE CUTGAZES   # # # # # # # # # # # # # # # #    
                        
                        ploteyecutgazes_window(sub, text, pageno, subexam, cutgazesx, cutgazesyline)    # ploteyecutgazes_window(sub, text, pageno, subexam, cutgazesx, cutgazesy, cutgazesduration)
                        
                        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #00000000000000000
                    
                    else:
                        mergecheck = False
                        print("\n\nNo folder or appropriate folder structure was found for subject=%d, text=%s, page=%d" % (sub, text, pageno)) 
            
            
            else:
                mergecheck = False
                print("\n\nNo data for subject=%d in text=%s" % (sub, text))

           
            # # # # # # # # # # # # # # # #  # # # # # Merge videos  # # # # # # # # # # # # # # # # # # # #
            totalpages = int(open(folder1 + 'texts/' + text + textends + '/py/pages/pages.txt', 'r').read()[0])
            totalpageslist = [x for x in range(1,totalpages+1)]
            if(mergecheck==True and pages==totalpageslist):
                # File paths of the input video files
                videolist = []
                for pno in pages:
                    videopath = folder1 + folder2 + 'subject_' + str(sub) + '/all_graphs/' + text + str(subexam) + '/py/ploteyecutgazes_window' + str(pno) + '.mp4'
                    videolist.append(videopath)
                
                # Load each video clip
                video_clips = [VideoFileClip(path) for path in videolist]
                
                # Concatenate the video clips
                final_clip = concatenate_videoclips(video_clips)
                
                # Write the concatenated video to a file
                final_clip.write_videofile(folder1 + folder2 + 'subject_' + str(sub) + '/all_graphs/' + text + str(subexam) + '/py/TotalReadingVideo.mp4')      
                # Close the video clips
                for clip in video_clips:
                    clip.close()
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #



