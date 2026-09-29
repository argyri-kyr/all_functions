
from asyncio.windows_events import NULL
import os
import pandas as pd
import xlsxwriter



from globalVars import folder1, folder2, textends, pyimagepath
from GetAndDrawROIS import getROIbounds
from MakeFixationsFile import MakeFixationsTxt
from fixationfungap import fixationfungap
from concatdata_v2Fix import concatdata_v2Fix
from drawFixations import drawFixations
from drawEyeMovements import drawEyeMovements
from GetAndDrawROIS import drawROIbounds
from filteredfixation import filteredfixation
from MakeGazesFile import MakeGazesTxt
from MakePageFixationsGap import MakePageFixationsGap


#################################################################################
#                                                                               #
# This funtion reads the cutgazes for the files and recalculates the fixations. #
# Check the globalvar.py for the settings (dispersion, cutoff, paths etc)       #
#                                                                               #
#################################################################################


def findfixationsonly():
    # subs = [i for i in range(13100, 13101)] 
    # exams = [1 for i in range(13100, 13101)]
    # texts = ['zoo','visit','zebra', 'visitloud']
    subs = [13010]
    exams = [1]
    texts = ['zebra']

    # Replace no valid gazes with valid
    global nonvalid2valid
    nonvalid2valid = 1    # '1' for replacing
    ###################################
    

    for i in range(len(subs)):
        for text in texts:
            if not os.path.exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_data/' + text + str(exams[i])):
                continue
            

            textpagespath = folder1 + 'texts/' + text + textends + '/py/pages/pages.txt'
            pages = open(textpagespath, "r").readlines()
            pages = int(pages[0])
            print("\nsubject %d, text %s" %(subs[i], text))
            
            # Make the folders (if not exist) that i will use to store graphs and data for my texts
            if not os.path.exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_data/' + text + str(exams[i])):
                os.makedirs(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_data/' + text + str(exams[i]))

            if not os.path.exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exams[i])):
                os.makedirs(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exams[i]))
                        
            if not os.path.exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exams[i]) + pyimagepath):
                os.makedirs(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exams[i]) + pyimagepath)
            

            for pageno in range(1, pages+1):
                roibounds = getROIbounds(text, pageno)             # Βρισκω τα ROIbounds του κειμενου

                roistartpath = folder1 + 'texts/' + text + textends + '/py/mytext/page(' + str(pageno) + ')/ROIstart/ROIstart.xlsx'
                roistart = pd.read_excel(roistartpath, header=None).values[0][0]

                cgpath = folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_data/' + text + str(exams[i]) + "/cutgazespy" + str(pageno) + '.txt'
                gazedata = []

                f = open(cgpath, "r")
                lines = f.readlines()

                for x in lines:
                    splited = x.split('\t')
                    gazedata.append( [int(splited[0]), float(splited[1]), float(splited[2]), float(splited[3]), int(splited[4]), int(splited[5]), float(splited[6]), float(splited[7])] )   

                cgdata = [[], [], [], [], [], [], [], []]
                for k in range(len(gazedata)):
                    cgdata[0].append(gazedata[k][0])
                    cgdata[1].append(gazedata[k][1])
                    cgdata[2].append(gazedata[k][2])
                    cgdata[3].append(gazedata[k][3])
                    cgdata[4].append(gazedata[k][4])
                    cgdata[5].append(gazedata[k][5])
                    cgdata[6].append(gazedata[k][6])

                
                # # # # # # # REPLACE NON VALID GAZES WITH VALID GAZES OF FILTERED DATA # # # # # # # #
                
                if( nonvalid2valid > 0 ):
                    gazedata = filteredfixation(subs[i], exams[i], text, pageno, gazedata, cgdata)
                                    
                    #Make cutgazes.txt file
                    MakeGazesTxt(subs[i], exams[i], text, pageno, gazedata)

                
                ############# END REPLACE NON VALID GAZES WITH VALID GAZES #############################

                 
                # # # # # # # # # # # # # # # # # # # # # # #  Gap Process -- NEW FIXATION  # # # # # # # # # # # # # # # # # # # # # #
       
                #Find Fixations and Make fixations.txt file
                fixationdatagap, gazestart, gazeend, fixationstart, fixationend, gap_data = fixationfungap(gazedata, roistart, roibounds)
                MakeFixationsTxt(subs[i], exams[i], text, pageno, roistart, fixationdatagap, roibounds)
                MakePageFixationsGap(subs[i], exams[i], text, pageno, gazestart, gazeend, fixationstart, fixationend, gap_data)
                
                # # # # # # # # # # # # # # # # # # # # # # End Gap Process # # # # # # # # # # # # # # # # # # # # # # 
                
                #Draw fixations(pane_number).png images
                drawFixations(subs[i], exams[i], text, fixationdatagap, pageno, "yes", NULL)

                # Draw fixations(pane_number).png colored arrows
                drawEyeMovements(subs[i], exams[i], text, fixationdatagap, pageno, NULL)
         
                #Draw cutgazes(pane_number).png images
                drawROIbounds(subs[i], exams[i], text, pageno, roibounds, cgdata[1], cgdata[2], "cutgazes", fixationdatagap, NULL, "close") 



            concatdata_v2Fix(subs[i], exams[i], text, 'fixations')


findfixationsonly()