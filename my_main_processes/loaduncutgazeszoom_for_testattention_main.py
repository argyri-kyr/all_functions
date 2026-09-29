


import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from load_Initial_Data_basic_gui import Load_Initial_Data_basic_gui
from procedures.loaduncutgazeszoom_for_testattention_Procedure import  loaduncutgazeszoom_for_testattention_Procedure


def loaduncutgazeszoom_for_testattention_main():
    textcheckedflag = 1
    subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye = Load_Initial_Data_basic_gui(textcheckedflag)
    
    extra_flag_shift_gazes = 1
    loaduncutgazeszoom_for_testattention_Procedure(subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye, extra_flag_shift_gazes)

loaduncutgazeszoom_for_testattention_main()