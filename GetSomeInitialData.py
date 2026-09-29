
from asyncio.windows_events import NULL
import fnmatch
import os
from globalVars import folder1, folder2

#Sinarthsh opou epistrefei tous fakelous pou periexoun dedomena gia ta keimena pou exei diavasei to subject, dhladh epistrefei tous fakelous:
# be_11622_1_morning_wa_8_2_2022-04-07-09.07.31, 
# be_11622_1_visit_wa_1_2_2022-04-07-09.01.06, 
# be_11622_1_visitloud_wa_4_2_2022-04-07-09.11.43, ......

#Kai epishs epistrefei thn taxi tou subject

def getGazesFoldersandClass(sub1):
    #create list of files
    mypath = folder1 + folder2 + 'subject_' + str(sub1) + '/'
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
    exam = 0

    for folder in folders:
        if( (folder != "all_data") and (folder != "all_graphs") ):
            gazesfolders.append(folder)
            if( textFolder(sub1, folder)==True ):
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


#sinarthsh opou elegxei ean o fakelos pou diavasa einai ontws ths morfhs be_11622_1_morning_wa_8_2_2022-04-07-09.07.31, elegxontas ean mesa sta orismata(ean o fakelos ginei split me basei to xarakthra '_') tou fakelou brethei kapou to id tou subject
def textFolder(sub1, folder):
    l = folder.split("_")
    
    if( len(l) > 1 ):
        if( str(sub1) == l[1] ):
            return True
    
    return False

#Sinarthsh opou apo olous tous fakelous tou gazesfolders = [be_11622_1_morning_wa_8_2_2022-04-07-09.07.31, be_11622_1_visit_wa_1_2_2022-04-07-09.01.06, be_11622_1_visitloud_wa_4_2_2022-04-07-09.11.43, ......]
#epistrefei ekeinon pou afora to ekastote keimeno pou thelw na analysw
def getGazesFolderbyText(sub1, exam, text, gazesfolders, sub1class, from_runcrashes):
    folders = []
    
    for f in gazesfolders:
        if( fnmatch.fnmatch(f,sub1class + '_' + str(sub1) + '_' + str(exam) + '_' + text + '_' + '*')):
            checklist = f.split(".")
            if('zip' in checklist or 'rar' in checklist or 'avi' in checklist):
                continue
            if(from_runcrashes==False):
                return f
            else:
                folders.append(f)
    
    if( from_runcrashes==True and folders!=[] ):
        return folders
    
    return NULL
     

#sinarthsh opou dhmiourgei to fakelo py mesa se kathe fakelo ths morfhs " be_11622_1_morning_wa_8_2_2022-04-07-09.07.31 "
def createextra(sub1, file):
    if not os.path.exists(folder1 + folder2 + '/subject_' + str(sub1) + '/' + file + '/py'):
        os.makedirs(folder1 + folder2 + '/subject_' + str(sub1) + '/' + file + '/py')

                    