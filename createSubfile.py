


from asyncio.windows_events import NULL
import os
import shutil
from tkinter.messagebox import askyesno

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from globalVars import folder1, folder2, folder3

#Sinarthsh opou epistrefei tous fakelous pou periexoun dedomena gia ta keimena pou exei diavasei to subject, dhladh epistrefei tous fakelous:
# be_11622_1_morning_wa_8_2_2022-04-07-09.07.31, 
# be_11622_1_visit_wa_1_2_2022-04-07-09.01.06, 
# be_11622_1_visitloud_wa_4_2_2022-04-07-09.11.43, ......

#Kai epishs epistrefei thn taxi tou subject

def getGazesFoldersandClass2(sub1):
    #create list of files
    mypath = folder3 
    folders = []

    if not os.path.exists(mypath):
        print("Individual Path %s doesn't exist" % mypath)
        return NULL

    for f in os.listdir(mypath):
        if os.path.isdir(mypath):
            folders.append(f)
    
    idclass = ""
    pavla = False
    pavlacounter = 0
    gazesfolders = []

    for folder in folders:
        if( textFolder2(sub1, folder)==True ):
            gazesfolders.append(folder)
            for i in range(len(folder)):
                if(folder[i]!="_" and pavla==False):
                    idclass+=(folder[i])
                if(folder[i]=="_"):
                    pavla=True
                    pavlacounter += 1
                    if( pavlacounter == 2 ):
                        exam = folder[i+1]
    
   
    if( gazesfolders == [] ):     # ean to subject den uparxei mesa sto fakelo /Documents/Optotech/
        return NULL
    
    return gazesfolders, idclass, exam


#sinarthsh opou elegxei ean o fakelos pou diavasa einai ontws ths morfhs be_11622_1_morning_wa_8_2_2022-04-07-09.07.31, elegxontas ean mesa sta orismata(ean o fakelos ginei split me basei to xarakthra '_') tou fakelou brethei kapou to id tou subject
def textFolder2(sub1, folder):
    
    d = folder.split(".")
    if( len(d) > 1 and (d[-1]=='zip' or d[-1]=='rar') ):
        return False
        
    l = folder.split("_")
    if( len(l) > 1 ):
        if( str(sub1) == l[1] ):
            return True
    
    return False



#Confirmation dialogue
def confirm(sub1):
    answer = askyesno(title='confirmation',
                    message='Subject %s exists in the analysis folder. Maybe is already analysed. Would you like to proceed with the analysis anyway?' % sub1)

    return answer



def createSubfile(sub1):
    array = getGazesFoldersandClass2(sub1)
    
    if( array == NULL ):
            return NULL
    
    gazesfolders, idclass, exam = array[0], array[1], array[2]

    answer = False
    if os.path.exists(folder1 + folder2 + 'subject_' + str(sub1)):
        answer = confirm(sub1)
        
    if( (answer==True) or ( not os.path.exists(folder1 + folder2 + 'subject_' + str(sub1)) ) ):
        
        if( not os.path.exists(folder1 + folder2 + 'subject_' + str(sub1)) ): 
            os.makedirs(folder1 + folder2 + 'subject_' + str(sub1))
        
        for i in range(len(gazesfolders)):
            src_path = folder3 + gazesfolders[i]
            dst_path = folder1 + folder2 + 'subject_' + str(sub1) + '/' + gazesfolders[i]
            if( os.path.isdir( src_path ) ):
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)

            for file in os.listdir(dst_path):
                if file.endswith('.zip'):
                    os.remove(folder1 + folder2 + 'subject_' + str(sub1) + '/' + gazesfolders[i] + "/" + file)
            
    
    elif( answer == False ):
        return NULL
            
    
    return gazesfolders, idclass, exam
