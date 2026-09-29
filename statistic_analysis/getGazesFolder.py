

import os
from asyncio.windows_events import NULL
import sys


# Get subject's gazesfolders
def getGazesFolder(subno, filepath):
    #create list of files
    folders = []
    
    if not os.path.exists(filepath):
        print("Individual Path %s doesn't exist" % filepath)
        return NULL

    for f in os.listdir(filepath):
        full_path = os.path.join(filepath, f)
        if ( os.path.isdir(full_path) and (not f.endswith(".pdf")) and (not f.endswith("rar")) ):
            folders.append(f)
    
    gazesfolders = []

    # Find all folders inside the path
    for folder in folders:
        if( len(folder.split("_")) > 1 and folder.split("_")[1] == str(subno) ):
            gazesfolders.append(folder)
    
    # Find a folder with struct like: de_13504_1_decodewordspseudo_wa_163_4_2025-12-01-17.41.30,
    # I want this as I want to be able to extract the date from it    
    if(gazesfolders==[]):
        print("Not even one gazesfolder available (folder like: de_13504_1_decodewordspseudo_wa_163_4_2025-12-01-17.41.30), for subject %d" % subno)
        sys.exit()    
    
    return gazesfolders