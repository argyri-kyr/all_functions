


import os
import time
from asyncio.windows_events import NULL
import psutil
import subprocess, threading


from globalVars import folder1, folder2, guiflag
from basic_function_gui import basic_function_gui
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass


def discard():
    
    from_runcrashes = False
    
    if( guiflag ):
        textcheckedflag = 0
        subs = NULL
        while( subs==NULL ):
            subs, texts, firstchoices = basic_function_gui(textcheckedflag)
            bypass, hardcases, onlylefteye, onlyrighteye = firstchoices[0], firstchoices[1], firstchoices[2], firstchoices[3]

    else:
        # texts = [ 'visit', 'zoo', 'visitloud', 'psaras', 'morning', 'island', 'efeyreseis', 'zebra', 'armyjet', 'enemypie', 'gasmask', 'jockey', 'midfred', 'midfredloud', 'sunny', 'sunnyloud' ]
        # texts = ['visit', 'zoo']
        # texts = ['sunny']
        # texts = ['visit', 'visitloud', 'zoo', 'psaras', 'efeyreseis', 'sunny', 'midfred', 'midfredloud', 'armyjet', 'gasmask']
        texts = ['efivk5k6part2']

        #Orizw poia einai ta subjects pou thelw na treksw
        # subs = [696, 729, 11512, 11514, 11520, 11521, 11522, 11523, 11524, 11525, 11526, 11527, 11528, 11529, 11530, 11531, 11532, 11533, 11534, 11535, 11536, 11537, 11538, 11539, 11540, 11548]   #subject id
        # subs = [11513, 11514, 11521, 11522, 11523, 11525, 11526, 11529, 11530, 11532, 11533, 11534, 11536, 11538, 11540, 11544, 11545, 11548, 11549, 11550, 11551, 11553]
        # subs = [5007, 5025, 5032, 5037, 5038, 5044, 5045, 5051, 5053, 5064, 5068, 5069, 5077, 5082, 5085, 5089, 5094, 5098, 5122, 5123, 5140, 5144]
        # subs = [1455, 1461, 1488, 1523, 1527, 1533]
        # subs = [1455, 1456, 1459, 1460, 1461]
        # subs = [ person  for person  in range(908, 920) ]
        # subs = [x for x in range(13100, 13103)]
        subs = [1938]
        
        bypass = 0
        hardcases = 0
        onlylefteye = 0
        onlyrighteye = 0
        firstchoices = [bypass, hardcases, onlylefteye, onlyrighteye]
        

    # Orizw se poia exam einai to kathe subject
    exam = 1
    



    # Kuria while loop gia na trexoun ola ta subject pou thelw ( trexw 1h loop gia ta subject kai 2h eswterikh loop gia ta texts tou subject )
    for i in range(len(subs)): 
        search1 = getGazesFoldersandClass(subs[i])   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/

        
        if( search1 == NULL ):
            print("Subject %s doesn't exist" %subs[i])
            time.sleep(5)
            continue
        
        else:
            gazesfolders, sub1class, subexam = search1[0], search1[1], search1[2]
        
        
        # Briskw apo ta keimena pou exw epilexei gia poia apo afta exw dedomena wste na kanw thn analysh mono se afta    
        discard_texts = []
        discardtextfiles = []
        for text in texts:
            file = getGazesFolderbyText(subs[i], exam, text, gazesfolders, sub1class, from_runcrashes)

            if( file != NULL ):
                discard_texts.append(text)
                discardtextfiles.append(file)
        
        print("Sub = ", subs[i])     
        print("Discard texts:")   
        print(*discard_texts)
        for j in range (len(discard_texts)):
            text = discard_texts[j]
            file = discardtextfiles[j]

            fileparts = file.split("_")
            fileparts[3] = fileparts[3][:2] + "_" + fileparts[3][2:]
            newfilename = "_".join(fileparts)
            
            # Rename first folder
            old_path1 = folder1 + folder2 + 'subject_' + str(subs[i]) + '/' + file
            new_path1 = folder1 + folder2 + 'subject_' + str(subs[i]) + '/' + newfilename
            try:
                # Your code that may raise WinError 5
                os.replace(old_path1, new_path1)  # vasilis: if error, it gives me a "PermissionError: [WinError 5] Access is denied" error
            except PermissionError as e:
                # Handle the specific exception for WinError 5 (Access is denied)
                print(f"Error: {e}")
                print("Access is denied. Please check permissions or run the script as an administrator.")
                warning_thread = threading.Thread(target=show_warning)
                warning_thread.start()
            except Exception as e:
                # Handle other exceptions if needed
                print(f"An error occurred: {e}")
                warning_thread = threading.Thread(target=show_warning)
                warning_thread.start()
            
            ##### Nothing else is change past here ############


            # Rename second
            if  os.path.exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_data/' + text + str(exam)):
                newtextname = text[:2] + "_" + text[2:]
                old_path2 = folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_data/' + text + str(exam)
                new_path2 = folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_data/' + newtextname + str(exam)
                os.replace(old_path2, new_path2)
            
            # Rename third
            if  os.path.exists(folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam)):
                newtextname = text[:2] + "_" + text[2:]
                old_path3 = folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + text + str(exam)
                new_path3 = folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/' + newtextname + str(exam)
                os.replace(old_path3, new_path3)
            
            
            # If something went wrong show me a Warning
            if( ('old_path1' in locals() and os.path.exists(old_path1)) or('old_path2' in locals() and os.path.exists(old_path2)) or ('old_path3' in locals() and os.path.exists(old_path3)) ):
                warning_thread = threading.Thread(target=show_warning)
                warning_thread.start()
                
    return


def show_warning():
    batch_file_path = r'discard_subs_batch.bat'
    subprocess.run(['start', '/WAIT', 'cmd', '/C', batch_file_path], check=True, shell=True)


def is_cmd_window_open():
    if( "chrome.exe" in (i.name() for i in psutil.process_iter()) ):
        return True
    return False


if __name__ == "__main__":
    discard()
