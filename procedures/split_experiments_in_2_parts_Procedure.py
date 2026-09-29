


import time
from asyncio.windows_events import NULL
import os
import shutil


import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2
from GetSomeInitialData import createextra, getGazesFolderbyText, getGazesFoldersandClass



def split_experiments_in_2_parts_Procedure(subs, exam, texts):
    global from_runcrashes
    from_runcrashes = False


    # subs = [subno for subno in range(14301, 14302)]
    # subs = [14301]
    # exam = 1
    

    # # TESTA PART A
    # text = "testapartav2"
    # target1 = "testapartav2part1"
    # target2 = "testapartav2part2"
    # pages_for_target1 = [2,3,4,5]
    # pages_for_target2 = [7,8,9,10,11,12,13,14,15]  

    # # TESTA PART B
    # text = "testapartb"
    # target1 = "testapartb1"
    # target2 = "testapartb2"
    # pages_for_target1 = [2,3,4]
    # pages_for_target2 = [6,7,8]  

    # # TESTA PART D
    # text = "testapartd"
    # target1 = "testapartd1"
    # target2 = "testapartd2"
    # pages_for_target1 = [2,3,4]
    # pages_for_target2 = [6,7,8]  

    # # TESTA PART E
    # text = "testaparte"
    # target1 = "testaparte1"
    # target2 = "testaparte2"
    # pages_for_target1 = [2,3]
    # pages_for_target2 = [5,6,7,8]  

    # # TESTA PART F
    # text = "testapartf"
    # target1 = "testapartf1"
    # target2 = "testapartftemp"
    # pages_for_target1 = [2]
    # pages_for_target2 = [5,8]

    # text = "testapartftemp"
    # target1 = "testapartf2"
    # target2 = "testapartf3"
    # pages_for_target1 = [1]
    # pages_for_target2 = [2]
    
    
    # text = "adk1k2"
    # target1 = "adk1k2part1"
    # target2 = "adk1k2part2"
    # pages_for_target1 = [2,3]
    # pages_for_target2 = [5,6]       

    # text = "adk3k4"
    # target1 = "adk3k4part1"
    # target2 = "adk3k4part2"
    # pages_for_target1 = [2,3]
    # pages_for_target2 = [5,6]  

    # text = "adk5k6"
    # target1 = "adk5k6part1"
    # target2 = "adk5k6part2"
    # pages_for_target1 = [2,3]
    # pages_for_target2 = [5,6]   
    
    # text = "testapartb"
    # target1 = "testapartb1"
    # target2 = "testapartb2"
    # pages_for_target1 = [2,3,4]
    # pages_for_target2 = [6,7,8]   

    # text = "testapartd"
    # target1 = "testapartd1"
    # target2 = "testapartd2"
    # pages_for_target1 = [2,3,4]
    # pages_for_target2 = [6,7,8]

    # text = "testaparte"
    # target1 = "testaparte1"
    # target2 = "testaparte2"
    # pages_for_target1 = [2,3]
    # pages_for_target2 = [5,6,7,8]

    # text = "testapartf"
    # target1 = "testapartf1"
    # target2 = "testapartftemp"
    # pages_for_target1 = [1]
    # pages_for_target2 = [4,7]

    # text = "testapartftemp"
    # target1 = "testapartf2"
    # target2 = "testapartf3"
    # pages_for_target1 = [1]
    # pages_for_target2 = [2]

    for text in texts:
        if( text == "raven" ):
            # # RAVEN
            target1 = "toDelete"
            target2 = "raven2v"
            pages_for_target1 = [1]
            pages_for_target2 = [i for i in range(2,38)]
        elif( text == "decodesentences" ):   
            # # DECODE SENTENCES
            target1 = "toDelete"
            target2 = "decodesentences3v"
            pages_for_target1 = [1]
            pages_for_target2 = [2,3,4,5,6,7,8,9,10,11]
        elif( text == "decodewordspseudo" ):
            # # DECODE REALWORDS / PSEUDOWORDS
            target1 = 'decoderealwords2v'
            target2 = 'decodepseudowords2v'
            pages_for_target1 = [2,3,4,5]
            pages_for_target2 = [7,8,9,10]
        elif( text == "visualorthogrecogn" ):
            # # VISUALORTHOGRECOGN
            target1 = 'visualrecogn3v'
            target2 = 'visualortho3v'
            pages_for_target1 = [2,3,4,5,6,7,8,9,10,11]
            pages_for_target2 = [13,14,15,16,17,18,19,20,21,22]
        elif( text == "phonolrhymes" ):
            # # PHONOLRHYMES
            target1 = "toDelete"
            target2 = 'phonolrhymes2v'
            pages_for_target1 = [1]
            pages_for_target2 = [2,3,4,5,6,7,8,9,10,11]
        elif( text == "rantwo" ):
            target1 = 'rantwopart1'
            target2 = 'rantwopart2'
            pages_for_target1 = [2]
            pages_for_target2 = [4]
        elif ( text == "efivk1k2" ):
            target1 = 'efivk1k2part1'
            target2 = 'efivk1k2part2'
            pages_for_target1 = [2]
            pages_for_target2 = [4]
        elif ( text == "efivk3k4" ):
            target1 = 'efivk3k4part1'
            target2 = 'efivk3k4part2'
            pages_for_target1 = [2]
            pages_for_target2 = [4]
        elif ( text == "efivk5k6" ):
            target1 = 'efivk5k6part1'
            target2 = 'efivk5k6part2'
            pages_for_target1 = [2,3]
            pages_for_target2 = [5,6]
        elif( text == 'decodewordsv2' ):
            target1 = 'toDelete'
            target2 = 'decoderealwords2v'
            pages_for_target1 = [1]
            pages_for_target2 = [2, 3, 4, 5]
        elif( text == 'decodepseudov2' ):
            target1 = 'toDelete'
            target2 = 'decodepseudowords2v'
            pages_for_target1 = [1]
            pages_for_target2 = [2, 3, 4, 5]
        elif(text=='visualorthov2'):
            target1 = 'toDelete'
            target2 = 'visualortho3v'
            pages_for_target1 = [1]
            pages_for_target2 = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        elif(text=='visualrecognv2'):
            target1 = 'toDelete'
            target2 = 'visualrecogn3v'
            pages_for_target1 = [1]
            pages_for_target2 = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


        for i in range(len(subs)): 
            # time.sleep(20)
            search1 = getGazesFoldersandClass(subs[i])   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/
            
            if( search1 == NULL ):
                print("Subject %s doesn't exist" %subs[i])
                time.sleep(5)
                continue

            else:
                gazesfolders, sub1class, subexam = search1[0], search1[1], search1[2]                           
                                
            
            # Briskw apo ta keimena pou exw epilexei gia poia apo afta exw dedomena wste na kanw thn analysh mono se afta    
            analysis_texts = []
            textanalysisfiles = []

            file = getGazesFolderbyText(subs[i], exam, text, gazesfolders, sub1class, from_runcrashes)
        
            if( file != NULL ):
                gazesfilepath = folder1 + folder2 + 'subject_' + str(subs[i]) + '/' + file + '/gazes.txt'  
                
                if not os.path.exists( gazesfilepath ):
                    # shutil.rmtree(folder1 + folder2 + 'subject_' + str(subs[i]) + '/' + file)
                    gazesfolders.remove(file)
                    continue
                
                createextra(subs[i], file)
                analysis_texts.append(text)
                textanalysisfiles.append(file)

            else:
                print("\n", text, " doesn't exist for sub =", subs[i])
                    
            
            print("\n", subs[i], "  ", *analysis_texts, "\n")
            for j in range (len(analysis_texts)):
                file = textanalysisfiles[j]            
                separate_procedure(file, subs[i], text, target1, target2, pages_for_target1, pages_for_target2)  # Main procedure of the programme for each text

                    

            

#Procedure's args ={ (text : text i will analyze), (folder : main folder), (sub1 : subject's id), (sub1class : subject's class) }
def separate_procedure(file, sub1, text, target1, target2, pages_for_target1, pages_for_target2):

    gazesfilepath = folder1 + folder2 + 'subject_' + str(sub1) + '/' + file + '/gazes.txt' 
    gazesfile = open(gazesfilepath,"r")
    lines = gazesfile.readlines()
    
    # countones = 0
    # for i in range(len(lines)):
    #     splitgazes = lines[i].split(None)
    #     if( splitgazes[0] == '1' ):
    #         countones += 1
    
    
    oldpath = folder1 + folder2 + 'subject_' + str(sub1) + '/' + file
    
    textfullname = file.split('_')
    
    textfullname[3] = target1
    target1 = "_".join(textfullname)
    
    textfullname[3] = target2
    target2 = "_".join(textfullname)
    
    pt1 = folder1 + folder2 + 'subject_' + str(sub1) + '/' + target1
    if not os.path.exists( pt1 ):
        os.makedirs( pt1 )
        copy_files(oldpath, pt1)
        
    pt2 = folder1 + folder2 + 'subject_' + str(sub1) + '/' + target2
    if not os.path.exists( pt2 ):
        os.makedirs( pt2 )
        copy_files(oldpath, pt2)
    
    
    ft1 = open( pt1 + '/gazes.txt',  'w')
    ft2 = open (pt2 + '/gazes.txt',  'w')
    
    newcounter = 0
    for i in range(len(lines)):
        splitgazes = lines[i].split(None)
        if( splitgazes[0] == '1' ):
            newcounter += 1
        
        if( newcounter in pages_for_target1 ):
            ft1.write(lines[i])
        elif( newcounter in pages_for_target2 ):
            ft2.write(lines[i])
    
    
    
    gazesfile.close()
    ft1.close() 
    ft2.close()        
    

    notet1 = open( pt1 + '/from_' + text + '_EXTENDED.txt',  'w')
    notet2 = open( pt2 + '/from_' + text + '_EXTENDED.txt',  'w')
        
    notet1.close()
    notet2.close()
    
    
    
    # from testapartf, i want to delete ftemp folder that i have create
    filenamesplit = file.split("_")
    if( "testapartftemp" in filenamesplit ):
        shutil.rmtree(folder1 + folder2 + 'subject_' + str(sub1) + '/' + file)
    
    # for files like raven I want to delete the toDelete file, that is target1 file name
    if( "toDelete" in target1.split("_") ):
        shutil.rmtree(folder1 + folder2 + 'subject_' + str(sub1) + '/' + target1)
    
    if( "toDelete" in target2.split("_") ):
        shutil.rmtree(folder1 + folder2 + 'subject_' + str(sub1) + '/' + target2)




def copy_files(src, dest):
    copiedlist = ['validation.png', 'validationEnd.png', 'Tobii_4L.txt']
    files = os.listdir(src)
    for fname in files:
        if fname in copiedlist:
            full_file_name = os.path.join(src, fname)
            if os.path.isfile(full_file_name):
                new_full_file_name = os.path.join(dest, fname)
                shutil.copy(full_file_name, new_full_file_name)
