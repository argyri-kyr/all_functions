


import os
from os.path import exists
import zipfile

from globalVars import folder1, folder2
from convertavitowav import avi_to_wav


def audio_define(sub, file):
    # # # # # Arxikopoihsh Hxhtikou # # # # #
    audiopath = folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/AudioRecording.wav'
    avipath = folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/exam.avi'
    newavi = folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/' + file + '.avi'
    videozippath = folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/'
    if not exists(audiopath):
        if exists(avipath):
            print("\nFound exam.avi\n") 
            avi_to_wav(avipath, audiopath)       
        elif exists(newavi):
            print("\nFound exam.avi\n") 
            avi_to_wav(newavi, audiopath)             
        else:
            # print("\nΝo audio file found for Subject = %d " % subs[i])
            # return
            for fname1 in os.listdir(videozippath):
                if fname1.endswith('.avi.zip'):
                    print("\nFound zipped avi file. Extracting...\n")  
                    with zipfile.ZipFile(videozippath+fname1, 'r') as zip_ref:
                        zip_ref.extractall(path=videozippath,pwd=b'2020r@d@r')
                        for fname2 in os.listdir(videozippath):
                            if fname2.endswith('.avi'):
                                # Convert .avi yo .wav
                                print("\nFound extracted avi file. Converting to wav...\n")   
                                newavipath = folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/' + fname2 
                                avi_to_wav(newavipath, audiopath)
                                
                                # Delete .avi
                                os.remove(videozippath+fname2)  
                                print("\nAvi file is deleted. Proceed to analysis...\n")
    
    return audiopath