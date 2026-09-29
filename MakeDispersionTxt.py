

import os

from globalVars import folder1, folder2, dispersion, dispersion2

def MakeDispersionTxt(sub1, exam, text):
    dispersiopath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/dispersion_' + str(dispersion) + '_' + str(dispersion2) + '.txt'
    if not os.path.exists(dispersiopath):
        dispersiontxt = open(dispersiopath, "w")
        dispersiontxt.close()