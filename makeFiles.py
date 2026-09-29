
                    
import shutil
from win32comext.shell import shell, shellcon
import os
from zipfile import ZipFile

def deltorecyclebin(filename):
    if not os.path.exists(filename):
        return True
    res= shell.SHFileOperation((0,shellcon.FO_DELETE,filename,None, shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,None,None))
    if not res[1]:
        os.system('del '+filename)
    

def makeFiles():
    files = []

    for f in next(os.walk('./'))[1]:
        if(f=='individual_zips'):
            filepath = os.listdir('./' + f)
            for file in filepath:
                files.append(file)
    # print("files = ",files)

    for f in files:
        list = f.split("_")
        sub1 = list[1]

                     
        if not os.path.exists('individual_temp/subject_' + sub1):
            os.makedirs('individual_temp/subject_' + sub1)
        

        if (f[-8:]=='.avi.zip'):
            if not os.path.exists('individual_temp/subject_' + sub1 + '/' + f[:-8]):
                os.makedirs('individual_temp/subject_' + sub1 + '/' + f[:-8])
            
            shutil.move('individual_zips/' + f, './individual_temp/subject_' + sub1 + '/' + f[:-8] + '/' + f)

        else:
            if not os.path.exists('individual_temp/subject_' + sub1 + '/' + f[:-4]):
                os.makedirs('individual_temp/subject_' + sub1 + '/' + f[:-4])
            
            with ZipFile('individual_zips/' + f, 'r') as zipObj:
                zipObj.extractall('individual_temp/subject_' + sub1 + '/' + f[:-4])

            deltorecyclebin('individual_zips/' + f)


        
  


makeFiles()