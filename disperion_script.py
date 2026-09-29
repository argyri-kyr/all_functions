

import os

from globalVars import folder1, folder2, dispersion, dispersion2

def MakeDispersionTxt():
    subs = [ i for i in range(13000, 13276)]
    texts = ['cbmpartc']
    exam = 1

    for sub1 in subs:
        for text in texts:
            textpath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/'
            if os.path.exists( textpath ):
                dispersiopath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/dispersion_' + str(dispersion) + '_' + str(dispersion2) + '.txt'
                if not os.path.exists(dispersiopath):
                    dispersiontxt = open(dispersiopath, "w")
                    dispersiontxt.close()

MakeDispersionTxt()