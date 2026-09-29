


import matplotlib.pyplot as plt
import statistics


from globalVars import folder1, folder2, pyimagepath


def horizontal_eyeposition_vergencex(sub1, exam, text, pageno, vergenceleftx, vergencerightx):
    # left plot
    f1, ax1 = plt.subplots()
    f1.set_figwidth(18)
    f1.set_figheight(4)
    ax1.plot(vergenceleftx)
    # title and labels, setting initial sizes
    f1.suptitle(str(sub1) + '  ' + 'Horizontal left eye position', fontsize=11, fontweight ="bold")
    ax1.set_xlabel('Time', fontsize=11)
    ax1.set_ylabel('X position(pixels)', fontsize=11) 
    ax1.margins(x=0.005)
    ax1.grid()
    f1.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/horizontal_left_eyeposition_vergencex' + str(pageno) + '.png', dpi=100)



    # right plot
    f2, ax2 = plt.subplots()
    f2.set_figwidth(18)
    f2.set_figheight(4)
    ax2.plot(vergencerightx)
    # title and labels, setting initial sizes
    f2.suptitle(str(sub1) + '  ' + 'Horizontal right eye position', fontsize=11, fontweight ="bold")
    ax2.set_xlabel('Time', fontsize=11)
    ax2.set_ylabel('X position(pixels)', fontsize=11)
    ax2.margins(x=0.005)
    ax2.grid() 
    f2.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/horizontal_right_eyeposition_vergencex' + str(pageno) + '.png', dpi=100)
    


    # both plot
    f3, ax3 = plt.subplots()
    f3.set_figwidth(18)
    f3.set_figheight(4)
    ax3.plot(vergenceleftx, 'r')
    ax3.plot(vergencerightx)
    # title and labels, setting initial sizes
    f3.suptitle(str(sub1) + '  ' + 'Horizontal eye position', fontsize=11, fontweight ="bold")
    ax3.set_xlabel('Time', fontsize=11)
    ax3.set_ylabel('X position(pixels)', fontsize=11)
    ax3.margins(x=0.005) 
    ax3.grid()
    f3.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/horizontal_eyeposition_vergencex' + str(pageno) + '.png', dpi=100)



    # disparity plot
    f4, ax4 = plt.subplots()
    f4.set_figwidth(18)
    f4.set_figheight(4)
    
    # find no zeros vergence data
    vergenceleftx_nozeros = []
    vergencerightx_nozeros = []
    for i in range(len(vergenceleftx)):
        if( vergenceleftx[i]!=0 and vergencerightx[i]!=0 ):
            vergenceleftx_nozeros.append(vergenceleftx[i])
            vergencerightx_nozeros.append(vergencerightx[i])
    
    # calculate disprity
    disparity = []
    for i in range(len(vergenceleftx_nozeros)):
        disparity.append( vergenceleftx_nozeros[i] - vergencerightx_nozeros[i] )
    
    # calculate max value
    absdisparity = [abs(disparity[i]) for i in range(len(disparity))]
    max_X = max(absdisparity)
    
    # disparity Info (stdev, mean)
    standar_deviation = statistics.stdev(disparity)
    mean = statistics.mean(disparity)

    disparityinfopath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + '/py/disparityInfo' + str(pageno) + '.txt' 
    disparityinfofile = open(disparityinfopath, 'w')
    disparityinfofile.write(str(standar_deviation))
    disparityinfofile.write("\n")
    disparityinfofile.write(str(mean))

    # spikes Info
    spikescounter = 0
    spikex1 = []
    spikex2 = []
    spikespath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + '/py/spikesdisparity' + str(pageno) + '.txt' 
    spikesfile = open(spikespath, 'w')
    for i in range(len(disparity)):
        if( abs(disparity[i])> abs(mean)+3*standar_deviation ):
            spikescounter+=1
            spikesfile.write(str(vergenceleftx_nozeros[i]) + "\n")
            spikesfile.write(str(vergencerightx_nozeros[i]) + "\n")
            spikesfile.write(str(disparity[i]) + "\n\n")
            spikex1.append(disparity[i])
            spikex2.append(i)
            
    
    # plot disparity (disparity-mean)
    # disparity = [disparity[x]-mean for x in range(len(disparity))]
    ax4.plot(disparity)
    ax4.plot(spikex2, spikex1, 'ro', markersize=3)
    
    # title and labels, setting initial sizes, limits
    f4.suptitle(str(sub1) + '  ' + 'Horizontal disparity panel', fontsize=11, fontweight ="bold")
    ax4.set_xlabel('Time', fontsize=11)
    ax4.set_ylabel('Phoria', fontsize=11)
    ax4.margins(x=0.005) 
    
    ax4.set_xlim([0, 1500])
    ax4.set_ylim([-500, 500])
    
    ax4.grid()
    f4.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/horizontal_disparity_panel' + str(pageno) + '.png', dpi=100)

    return standar_deviation, mean, spikescounter