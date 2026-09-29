


import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from load_Initial_Data_splitexperiments_gui import Load_Initial_splitexperiments_gui
from procedures.split_experiments_in_2_parts_Procedure import split_experiments_in_2_parts_Procedure


def split_experiments_in_2_parts_main():
    subs, texts = Load_Initial_splitexperiments_gui()

    exam = 1
    
    split_experiments_in_2_parts_Procedure(subs, exam, texts)


split_experiments_in_2_parts_main()