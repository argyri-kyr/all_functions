

def colorRightplot(event, indexes, plines, gtempx, gtempy, g, g_ax, mycolor, from_multilines):
    # # # # # # # # # # # # # # # # # # # #   Right Plot ( - g, g_ax - figure )   # # # # # # # # # # # # # # # # # # # # # 

    # # # redefine and color in right plot the cut i've made
    if( (from_multilines==False and len(indexes)>=2 and len(indexes)<=plines+1)  or  (from_multilines==True and len(indexes)>=2) ):
        selectedx = []
        selectedy = []
        for i in range( int(indexes[-2]) , int(indexes[-1]) ):
            selectedx.append(gtempx[i])
            selectedy.append(gtempy[i])


        g_ax.plot(selectedx, selectedy, 'x', color = mycolor, markeredgewidth=0.5)
        g.set_size_inches(5, 4)
        g_ax.set_xlim(-5, 1920)      # sizes for preview plot not for cuts plot
        g_ax.set_ylim(1080, -5)      # sizes for preview plot not for cuts plot
        
        g.canvas.draw_idle()
        # # # #

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    return