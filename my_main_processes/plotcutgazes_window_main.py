

from asyncio.windows_events import NULL

import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)


from globalVars import guiflag
from basic_plot_gui import basic_plot_gui
from procedures.plotcutgazes_window_Procedure import plotcutgazes_window_Procedure


def plotcutgazes_window_main():
    if( guiflag ):
        subs = NULL
        while( subs==NULL ):
            subs, texts, pages = basic_plot_gui()

    else:
        # subs = [13332, 13348, 13354, 13369]
        subs = [13702]
        texts=['decodesentences2v']
        pages = [1]
        
    
    plotcutgazes_window_Procedure(subs, texts, pages)
    


plotcutgazes_window_main()