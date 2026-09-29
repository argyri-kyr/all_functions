

import matplotlib.pyplot as plt


from globalVars import folder1, folder2, pyimagepath
from movefigure import movefigure
        

def plot_one_eye(sub1, exam, text, pageno, oneeyeindexes, referred_eye, movefigsizes):
    p1 = plt.figure()
    p1.set_figwidth(5)
    p1.set_figheight(2)
    axp = plt.subplot(1,1,1)
    axp.margins(x=0)
    # plt.subplots_adjust(left = 0.15)
    
    axp.plot(oneeyeindexes[0],'yellow')
    axp.plot(oneeyeindexes[1],'bo', markersize=0.1)
    # plt.plot(negativetempy, 'ro', markersize=1)
    # plt.plot(ygazesmedian, 'r')

    axp.set_title( referred_eye )

    plt.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/linesteps_' + referred_eye + str(pageno) + '.png')
    
    movefigure(p1, movefigsizes[0], movefigsizes[1])

    return 