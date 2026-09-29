


import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from load_Initial_Data_basic_gui import Load_Initial_Data_basic_gui
from procedures.rois_audio_Procedure import  rois_audio_Procedure


def rois_audio_main():
    textcheckedflag = 2
    subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye = Load_Initial_Data_basic_gui(textcheckedflag)
    rois_audio_Procedure(subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye)
    

rois_audio_main()



