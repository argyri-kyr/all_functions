


import time
from asyncio.windows_events import NULL


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import guiflag
from basic_plot_gui import basic_plot_gui
from procedures.plotvergence_Procedure import plotvergence_Procedure
from procedures.plotfixations_Procedure import plotfixations_Procedure
from procedures.ploteyemovements_Procedure import ploteyemovements_Procedure
from procedures.plotcutgazes_window_Procedure import plotcutgazes_window_Procedure
from procedures.plotfixation_window_Procedure import plotfixation_window_Procedure
from procedures.eyeposition_optometrist_Procedure import eyeposition_optometrist_Procedure


#################################################
# INSTALL FFMPEG FIRST
"""
    You need to install ffmpeg first follow the instructions
    from extra_libraries folder.

"""
##################################################



def ofthalmos_multiple_options_main():
    if( guiflag ):
        subs = NULL
        while( subs==NULL ):
            subs, texts, pages = basic_plot_gui()

    else:
        subs = [1678]
        texts = ['midfredloud']
        pages = [1]



    startgazesgui = ''
    endgazesgui = ''
    plotvergence_Procedure(subs, texts, pages, startgazesgui, endgazesgui)
    
    
    plotfixations_Procedure(subs, texts, pages)
    
    
    ploteyemovements_Procedure(subs, texts, pages)
    
    
    plotcutgazes_window_Procedure(subs, texts, pages)
    
    
    plotfixation_window_Procedure(subs, texts, pages)
    
    
    firstchoices, bypass, hardcases, onlylefteye, onlyrighteye = 0, 0, 0, 0, 0
    eyeposition_optometrist_Procedure(subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye)
    
    return


ofthalmos_multiple_options_main()