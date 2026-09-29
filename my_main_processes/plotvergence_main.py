


import time


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import guiflag
from vergence_gui import vergence_gui
from procedures.plotvergence_Procedure import plotvergence_Procedure



#################################################
# INSTALL FFMPEG FIRST
"""
    You need to install ffmpeg first follow the instructions
    from extra_libraries folder.

"""
##################################################



def plotvergence_main():
    if( guiflag ):
        subs, texts, pages, startgazesgui, endgazesgui = vergence_gui()

    else:
        # subs = [1482, 1531, 1532, 1580, 1632]   #ofthalmos list, me exophoria oi 5 teleftaioi
        subs = [1678]
        texts=['visitloud', 'midfredloud']
        pages = [1,2,3,4,5]
        startgazesgui = ''
        endgazesgui = ''

    if(startgazesgui!='' and endgazesgui!='' and startgazesgui>=endgazesgui):
        print("\nGaze Start cannot be smaller than Gaze End. Try again.")
        time.sleep(3)
        return

    if( (startgazesgui!='' and startgazesgui<0) or  (endgazesgui!='' and endgazesgui<0) ):
        print("\nGaze Start and Gaze End must be positive numbers. Try again.")
        time.sleep(3)
        return    

    
    
    plotvergence_Procedure(subs, texts, pages, startgazesgui, endgazesgui)



plotvergence_main()