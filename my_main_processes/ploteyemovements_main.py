

from asyncio.windows_events import NULL


import os,sys,inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import guiflag
from basic_plot_gui import basic_plot_gui
from procedures.ploteyemovements_Procedure import ploteyemovements_Procedure


def ploteyemovements_main():
    if( guiflag ):
        subs = NULL
        while( subs==NULL ):
            subs, texts, pages = basic_plot_gui()

    else:
        subs = [8888]
        texts=['zoo']
        pages = [1]
    
    ploteyemovements_Procedure(subs, texts, pages)


ploteyemovements_main()