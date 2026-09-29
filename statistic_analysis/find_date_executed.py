


from asyncio.windows_events import NULL
import re
from datetime import datetime

from asyncio.windows_events import NULL
import os
import sys


# Sinarthsh opou elegxei ean o fakelos pou diavasa einai ontws ths morfhs be_11622_1_morning_wa_8_2_2022-04-07-09.07.31, elegxontas ean mesa sta orismata(ean o fakelos ginei split me basei to xarakthra '_') tou fakelou brethei kapou to id tou subject
def textFolder(subno, folder):
    l = folder.split("_")
    
    if( len(l) > 1 ):
        if( str(subno) == l[1] ):
            return True
    
    return False


# Get subject's class
def getAppropriateDateFolder(subno, filepath):
    #create list of files
    folders = []

    if not os.path.exists(filepath):
        print("Individual Path %s doesn't exist" % filepath)
        return NULL

    for f in os.listdir(filepath):
        full_path = os.path.join(filepath, f)
        if ( os.path.isdir(full_path) and (not f.endswith(".pdf")) and (not f.endswith("rar")) ):
            folders.append(f)
    
    idclass = ""
    pavla = False
    pavlacounter = 0
    gazesfolders = []

    # Find all folders inside the path
    for folder in folders:
        if( (folder != "all_data") and (folder != "all_graphs") ):
            gazesfolders.append(folder)
            if( textFolder(subno, folder)==True ):
                for i in range(len(folder)):
                    if(folder[i]!="_" and pavla==False):
                        idclass+=(folder[i])
                    if(folder[i]=="_"):
                        pavla=True
                        pavlacounter += 1
    
    # Find a folder with struct like: de_13504_1_decodewordspseudo_wa_163_4_2025-12-01-17.41.30,
    # I want this as I want to be able to extract the date from it    
    if(gazesfolders==[]):
        print("No folder with data defined into subject's folder, for subject %d" % subno)
        sys.exit()    
    
    datefolder = ""
    for folder in gazesfolders:
        if( folder.split("_")[1] == str(subno) ):
            datefolder = folder
            break
    
    if(datefolder == ""):
        print("No folder with data defined into subject's folder, for subject %d" % subno)
        sys.exit()
    
    return datefolder



def find_date_executed(subno, filepath):
    datefolder = getAppropriateDateFolder(subno, filepath)
    
    # Extract date pattern YYYY-MM-DD
    match = re.search(r"\d{4}-\d{2}-\d{2}", datefolder)
    if not match:
        return None

    date_obj = datetime.strptime(match.group(), "%Y-%m-%d")
    return f"{date_obj.day}/{date_obj.month}/{date_obj.year}"