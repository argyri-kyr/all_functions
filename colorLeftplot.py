

def colorLeftplot(event, indexes, plines, gtempy, hardcases, mycolor, f, ax, gmin_ylim, gmax_ylim, gmin_xlim, gmax_xlim, from_multilines):
    # # # # # # # # # # # # # # # # # # # #   Left Plot ( - f, ax - figure )   # # # # # # # # # # # # # # # # # # # # # # 
    
    # # # redefine and color in left plot the cut i've made
    if( (from_multilines==False and len(indexes)>=2 and len(indexes)<=plines+1)  or  (from_multilines==True and len(indexes)>=2) ):
        cuty = []
        for i in range(int(indexes[-2])):
            cuty.append(None)
        for i in range( int(indexes[-2]) , int(indexes[-1]) ):
            cuty.append(gtempy[i])

        if( hardcases ):
            ax.plot(cuty, 'o', color = mycolor, markersize = 1)
        else:
            ax.plot(cuty, color = mycolor, markersize = 1)
        
        # ax.set_ylim(gmin_ylim, gmax_ylim)     # sizes for cuts plot, not for cuts plot ( these two its different)
    
    
    ax.set_ylim(gmin_ylim, gmax_ylim) 
    ax.set_xlim(gmin_xlim, gmax_xlim) 
    f.canvas.draw_idle()   
    # # # # # # # #    
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    return