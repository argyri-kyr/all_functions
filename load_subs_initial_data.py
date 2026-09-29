

from asyncio.windows_events import NULL
import time
import shutil
import os

from globalVars import folder1, folder2
from GetSomeInitialData import createextra, getGazesFolderbyText, getGazesFoldersandClass
from createSubfile import createSubfile


def load_subs_initial_data(sub, exam, texts, from_runcrashes):
    search1 = getGazesFoldersandClass(sub)   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/
    search2 = createSubfile(sub)             # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Users/RADAR/Documents/Optotech/
    
    if( search1 == NULL ):
        if(search2==NULL):
            print("Subject %s doesn't exist" %sub)
            print("Path to subject: ", folder1 + folder2 + 'subject_' + str(sub) + '/')
            time.sleep(5)
            return NULL, NULL, NULL
        else:
            gazesfolders, sub1class, subexam = search2[0], search2[1], search2[2]
    
    else:
        if(search2==NULL):
            gazesfolders, sub1class, subexam = search1[0], search1[1], search1[2]
        else:
            gazesfolders1, sub1class, subexam = search1[0], search1[1], search1[2]   # gazesfolders1 : ta keimena pou brethikan mesa sto individual
            gazesfolders2, sub1class, subexam = search2[0], search2[1], search2[2]   # gazesfolders2 : ta keimena pou brethikan mesa sto Documents/Optotech
            gazesfolders = gazesfolders1 + gazesfolders2   # sinolo keimenwn giafto to subject
            gazesfolders = list(dict.fromkeys(gazesfolders))
                            


    # Briskw apo ta keimena pou exw epilexei gia poia apo afta exw dedomena wste na kanw thn analysh mono se afta    
    analysis_texts = []
    textanalysisfiles = []
    for text in texts:
        file = getGazesFolderbyText(sub, exam, text, gazesfolders, sub1class, from_runcrashes)
        
        if( file != NULL ):
            gazesfilepath = folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/gazes.txt'  
            if not os.path.exists( gazesfilepath ):
                shutil.rmtree(folder1 + folder2 + 'subject_' + str(sub) + '/' + file)
                gazesfolders.remove(file)
                texts.append(text)
                continue

        if( file != NULL ):
            createextra(sub, file)
            analysis_texts.append(text)
            textanalysisfiles.append(file)
            
    print("\n",*analysis_texts)
    
    return gazesfolders, analysis_texts, textanalysisfiles
