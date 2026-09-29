

import pandas as pd


from globalVars import folder1, folder2, textends
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass
from loaduncutfiltereddata import loaduncutfiltereddata
from GetAndDrawROIS import getROIbounds
from calcROI import calcROI

##################################################################################################
#
# This function replaces the non valid gazes of gazes.txt with valid gazes from gazes_filtered.txt 
#
##################################################################################################


def filteredfixation(sub, exam, text, pageno, gazedata, cgdata):
    from_runcrashes = False

    search1 = getGazesFoldersandClass(sub)
    gazesfolders, sub1class, subexam = search1[0], search1[1], search1[2]
    file = getGazesFolderbyText(sub, exam, text, gazesfolders, sub1class, from_runcrashes)

    roibounds = getROIbounds(text, pageno)
    roistartpath = folder1 + 'texts/' + text + textends + '/py/mytext/page(' + str(pageno) + ')/ROIstart/ROIstart.xlsx'
    roistart = pd.read_excel(roistartpath, header=None).values[0][0]


    gazesfiltered = loaduncutfiltereddata(text, exam, file, sub)
    counter = 0

    for i in range(len(cgdata[0])):
        if(cgdata[5][i]==0):
            while(counter<len(gazesfiltered[0])):
                if(int(cgdata[3][i]) == int(gazesfiltered[3][counter]) or int(cgdata[3][i])-1 == int(gazesfiltered[3][counter])):
                    gazedata[i][1] = gazesfiltered[1][counter]
                    gazedata[i][2] = gazesfiltered[2][counter]
                    gazedata[i][4] = calcROI(roistart, gazesfiltered[1][counter], gazesfiltered[2][counter], roibounds[0], roibounds[1], roibounds[2], roibounds[3])

                    if(gazesfiltered[1][counter]>0 and gazesfiltered[2][counter]>0):
                        gazedata[i][5] = 1

                    break

                counter += 1


    return gazedata