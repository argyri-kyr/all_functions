

import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from load_Initial_Data_basic_gui import Load_Initial_Data_basic_gui
from autoloaduncutgazeszoom_Procedure import  autoloaduncutgazeszoom_Procedure


def autoloaduncutgazeszoom_main():
    textcheckedflag = 1
    subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye = Load_Initial_Data_basic_gui(textcheckedflag)
    
    autoloaduncutgazeszoom_Procedure(subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye)

autoloaduncutgazeszoom_main()

