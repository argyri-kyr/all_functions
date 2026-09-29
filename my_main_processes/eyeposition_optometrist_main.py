

import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from load_Initial_Data_basic_gui import Load_Initial_Data_basic_gui
from procedures.eyeposition_optometrist_Procedure import eyeposition_optometrist_Procedure


def eyeposition_optometrist_main():
    textcheckedflag = 1
    subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye = Load_Initial_Data_basic_gui(textcheckedflag)
    eyeposition_optometrist_Procedure(subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye)


eyeposition_optometrist_main()