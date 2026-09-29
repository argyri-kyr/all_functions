

import os,sys,inspect
from asyncio.windows_events import NULL

from modify_gazes_timestamp_for_ivan import modify_gazes_timestamp_for_ivan

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from load_Initial_Data_basic_gui_for_ivan import Load_Initial_Data_basic_gui_for_ivan

parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from load_subs_initial_data import load_subs_initial_data



def make_gazes_for_ivan_main():
    textcheckedflag = 1
    subs, operation_var, texts= Load_Initial_Data_basic_gui_for_ivan(textcheckedflag)
    
    exam = 1
    from_runcrashes = False

    for i in range(len(subs)): 
        gazesfolders, analysis_texts, textanalysisfiles = load_subs_initial_data(subs[i], exam, texts, from_runcrashes)      
        if( gazesfolders == NULL ):
            continue        
        
        for j in range (len(analysis_texts)):
            text = analysis_texts[j]
            file = textanalysisfiles[j]
            # Load Gazes Data 
            gazesfilepath, new_lines_length = modify_gazes_timestamp_for_ivan(subs[i], file, text, operation_var)
            

make_gazes_for_ivan_main()