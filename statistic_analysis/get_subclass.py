

from asyncio.windows_events import NULL
import os



# Sinarthsh opou elegxei ean o fakelos pou diavasa einai ontws ths morfhs be_11622_1_morning_wa_8_2_2022-04-07-09.07.31, elegxontas ean mesa sta orismata(ean o fakelos ginei split me basei to xarakthra '_') tou fakelou brethei kapou to id tou subject
def textFolder(subno, folder):
    l = folder.split("_")
    
    if( len(l) > 1 ):
        if( str(subno) == l[1] ):
            return True
    
    return False


# Get subject's class
def get_subclass(subno, filepath):
    #create list of files
    folders = []

    if not os.path.exists(filepath):
        print("Individual Path %s doesn't exist" % filepath)
        return NULL

    for f in os.listdir(filepath):
        if ( os.path.isdir(filepath) and (not f.endswith(".pdf")) ):
            folders.append(f)
    
    idclass = ""
    pavla = False
    pavlacounter = 0
    gazesfolders = []
    exam = 0

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
                        if( pavlacounter == 2 ):
                            exam = folder[i+1]
    
    #print(idclass)
    return gazesfolders, idclass, exam