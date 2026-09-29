



import time
from asyncio.windows_events import NULL
import os
import shutil


from globalVars import folder1, folder2
from GetSomeInitialData import getGazesFoldersandClass

def delete_sub_folders_files():
    global from_runcrashes
    from_runcrashes = False


    subs = [x for x in range(13001, 13260)]

    # Orizw se poia exam einai to kathe subject
    exam = 1

    text = "testapartb2"
    
    for i in range(len(subs)): 
        # time.sleep(20)
        search1 = getGazesFoldersandClass(subs[i])   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/
        
        if( search1 == NULL ):
            print("Subject %s doesn't exist" %subs[i])
            time.sleep(5)
            continue                         
        
        
        filename1 = folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_data/' + text + str(exam)
        filename2 = folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam)
        filename3 = folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam) + '_crash.txt'
        
        if os.path.exists(filename1): 
            shutil.rmtree(filename1) 
        

        if os.path.exists(filename2): 
            shutil.rmtree(filename2) 
            

        if os.path.exists(filename3): 
            os.remove(filename3)     




delete_sub_folders_files()