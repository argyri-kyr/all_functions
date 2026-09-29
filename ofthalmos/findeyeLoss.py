


from asyncio.windows_events import NULL
import time
import pandas as pd
import xlsxwriter


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2, textends, guiflag
from GetSomeInitialData import getGazesFolderbyText
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass
from vergence_gui import vergence_gui



def findeyeLoss():
    startvergence = time.time()
    exam = 1
    
    if( guiflag ):
        subs, texts, pages, startgazesgui, endgazesgui = vergence_gui()

    else:
        # subs = [1426, 1427, 1428, 1429, 1655, 1505, 1512, 1513, 1541]
        # subs = [1488, 1490, 1424, 1431, 1441, 1461, 1482, 1531, 1532, 1580, 1632]   #ofthalmos list, me exophoria oi 5 teleftaioi
        subs = [1532]
        # subs = [1]
        # texts = [ 'visit', 'zoo', 'visitloud', 'psaras', 'morning', 'island', 'efeyreseis', 'zebra', 'armyjet', 'enemypie', 'gasmask', 'jockey', 'midfred', 'midfredloud', 'sunny', 'sunnyloud' ]
        texts = ['midfred']
        # texts=['visitloud', 'midfredloud']
        # pages=[1,2,3,4,5]
        # pages = [3]

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
                pagesfile = open(folder1 + "texts/" + text + textends + "/py/pages/pages.txt", "r")
                pages = int(pagesfile.read(1))
                
                countblock = []
                countblockleft = []
                countblockright = []
                countnonblock = []
                countnonblockleft = []
                countnonblockright = []
                
                for pageno in range(1,pages+1):
                    filefound = False

                    for textfile in textfolder:    
                        uncutgazesrawpath = folder1 + folder2 + 'subject_' + str(sub) + '/all_data/' + text + str(exam) + '/uncutgazesraw' + str(pageno) + '.xlsx'
                        if( os.path.exists(uncutgazesrawpath) ):
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
                
                    block, blockleft, blockright, nonblock, nonblockleft, nonblockright = eyeLossdetect(vergenceindex, vergenceleftvalid, vergencerightvalid)
                    countblock.append(block)
                    countblockleft.append(blockleft)
                    countblockright.append(blockright)
                    countnonblock.append(nonblock)
                    countnonblockleft.append(nonblockleft)
                    countnonblockright.append(nonblockright)
                    
                
                tracklosswb = xlsxwriter.Workbook(folder1 + folder2 + 'subject_' + str(sub) + '/all_data/' + text + str(exam) + '/trackloss.xlsx')
                tracklosswsh = tracklosswb.add_worksheet()
                tracklosswsh.write_row(0, 0, ["Block" , "Block Loss Left" , "Block Loss Right" , "Non Block" , "Non Block Left" , "Non Block Right"] )
                
                width= len("long text hidden test-1")
                tracklosswsh.set_column(0, 0, width)
                tracklosswsh.set_column(0, 1, width)
                tracklosswsh.set_column(0, 2, width)
                tracklosswsh.set_column(0, 3, width)
                tracklosswsh.set_column(0, 4, width)
                tracklosswsh.set_column(0, 5, width)
                
                for j in range(len(countblock)):
                    tracklosswsh.write_row( j+1, 0, [countblock[j] , countblockleft[j] , countblockright[j] , countnonblock[j] , countnonblockleft[j] , countnonblockright[j] ])
                
                tracklosswb.close()
                        

def eyeLossdetect(vergenceindex, vergenceleftvalid, vergencerightvalid):
    lostindexes = []
    countblock = 0
    countblockleft = 0
    countblockright = 0
    countnonblock = 0
    countnonblockleft = 0
    countnonblockright = 0
    
    for i in range(len(vergenceindex)):
        
        if(vergenceleftvalid[i]==1 and vergencerightvalid[i]==0):
            if( (vergenceleftvalid[i-1]==0 and vergencerightvalid[i-1]==0) or (vergenceleftvalid[i+1]==0 and vergencerightvalid[i+1]==0) ):
                lostindexes.append( vergenceindex[i] )
                countblock += 1
                countblockright += 1
            else:
                countnonblock += 1
                countnonblockright += 1
                
            
        if(vergenceleftvalid[i]==0 and vergencerightvalid[i]==1):
            if( (vergenceleftvalid[i-1]==0 and vergencerightvalid[i-1]==0) or (vergenceleftvalid[i+1]==0 and vergencerightvalid[i+1]==0) ):
                lostindexes.append( vergenceindex[i] )
                countblock += 1
                countblockleft += 1
            else:
                countnonblock += 1
                countnonblockleft += 1
                
                
    
    return countblock, countblockleft, countblockright, countnonblock, countnonblockleft, countnonblockright



findeyeLoss()