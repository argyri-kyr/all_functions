


import os,sys,inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)



from load_Initial_Data_basic_gui import Load_Initial_Data_basic_gui
from procedures.loaduncutgazeszoom_2024_Procedure import loaduncutgazeszoom_2024_Procedure



def loaduncutgazeszoom_2024_main():
    textcheckedflag = 1
    subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye = Load_Initial_Data_basic_gui(textcheckedflag)
    loaduncutgazeszoom_2024_Procedure(subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye)

loaduncutgazeszoom_2024_main()

