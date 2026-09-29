

import numpy as np
import matplotlib.pyplot as plt


from globalVars import folder1, folder2, pyimagepath



def disparitywindow(sub1, exam, text, pageno, windowlen, disparity):
    start = 0
    end = windowlen
    result = []
    
    while(end<len(disparity)):
        tempdisp = disparity[start:end]
        clear_disparity = [ x for x in tempdisp if x!=None ]
        
        window_mean = np.mean(clear_disparity)
        result.append(window_mean)
        
        start+=1
        end+=1


    # right plot
    f1, ax1 = plt.subplots()
    f1.set_figwidth(18)
    f1.set_figheight(4)
    ax1.plot(result)
    # title and labels, setting initial sizes
    f1.suptitle(str(sub1) + '  ' + 'Moving Window Disparity Mean', fontsize=11, fontweight ="bold")
    ax1.set_xlabel('Time', fontsize=11)
    ax1.set_ylabel('X position(pixels)', fontsize=11)
    ax1.margins(x=0.005)
    ax1.grid() 
    f1.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/extra_plots/window_disparity_mean' + str(pageno) + '.png', dpi=100)
    
    
        
    return result