


import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from load_Initial_Data_basic_gui import Load_Initial_Data_basic_gui
from procedures.total_shift_Procedure import  total_shift_Procedure


def total_shift_main():
    textcheckedflag = 1
    subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye = Load_Initial_Data_basic_gui(textcheckedflag)
    total_shift_Procedure(subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye)

total_shift_main()