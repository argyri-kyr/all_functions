


import matplotlib
matplotlib.use("Agg")  # non-interactive backend

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def plot_hist(exercise, exercise_title, plotspath, x_dict, indiv_score, title_x, title_y, bins):
    x = list(x_dict.values())    

    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))

    # histogram
    axs.hist(x, bins=bins, align='left', rwidth=0.8)
    axs.yaxis.set_major_locator(MaxNLocator(integer=True))
    axs.set_xlabel(title_x)
    axs.set_ylabel(title_y)
    axs.axvline(indiv_score, color='red', linewidth=2)
    
    # Show bins
    # show all bin numbers
    if(len(bins)<30):
        axs.set_xticks(bins[:-1]) 
    else:
        # show every 10th value on x-axis
        tick_step = max(1, len(bins) // 15)
        axs.set_xticks(bins[::tick_step])


    # fig.tight_layout()
    axs.set_title(exercise_title)
    
    figurepath = plotspath + '/' + exercise_title + '.png'
    fig.savefig(figurepath)
    # BLOCK until window is closed
    # plt.show()

    # ✅ release memory & avoid overlapping figures
    plt.close(fig)
    
    return figurepath
    
    
def plot_results_hist(subno, exercises, exercise, results_collection1, results_collection2, plotspath):
    title_x, title_y = "number of correct answers", "population"
    figurepath1, figurepath2 = '', ''
    
    if( (results_collection1!={}) and (subno in results_collection1.keys()) ):
        part = 1
        exercise_title = exercise + ' pt' + str(part)
        
        indiv_score1 = results_collection1[subno]
        
        
        if(exercise=='Memory Short Audit Verb'):
            bins1 = range(0, exercises[exercise][1] + 2)
        else:
            bins1 = range(0, exercises[exercise] + 2)
            
        figurepath1 = plot_hist(exercise, exercise_title, plotspath, results_collection1, indiv_score1, title_x, title_y, bins1)
    
    
    
    if( (results_collection2!={}) and (subno in results_collection2.keys()) ):
        part = 2
        exercise_title = exercise + ' pt' + str(part)
        
        indiv_score2 = results_collection2[subno]
        
        if(exercise=='Memory Short Audit Verb'):
            bins2 = range(0, exercises[exercise][2] + 2)
        else:
            bins2 = range(0, exercises[exercise] + 2)
            
        figurepath2 = plot_hist(exercise, exercise_title, plotspath, results_collection2, indiv_score2, title_x, title_y, bins2) 
            
    return figurepath1, figurepath2