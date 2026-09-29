import os
import shutil

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2

def screenconvert(textgazefile, subject_no):

    #  From 1920 to 1366 
    # screen data
    dxorig=34.5353 
    dyorig=19.4261
    dxfinal=34.5353
    dyfinal=19.4261
    origanal=[1920,1080]
    finalanal=[1366,768]  
    origcenter=[i/2 for i in origanal]
    finalcenter=[i/2 for i in finalanal]

    #  text data
    #  text='visit' #text name
    #  text='zoo'   #for all popul

    fullpath = folder1 + folder2 + 'subject_' + str(subject_no) + '/' + textgazefile + '/'

    folders = []
    for f in os.listdir(fullpath):
        if os.path.isdir(fullpath):
            folders.append(f)

    if 'gazes-orignal-1920.txt' in folders:
        print("Gazes already converted, Returning...\n")
        return
    
    
    #Don't overwrite original data, rename and save them
    source1 = fullpath + 'gazes.txt'
    source2 = fullpath + 'gazes-orignal-1920.txt'
    shutil.copyfile(source1, source2)

    #Convert gaze data 
    newgazestxt = fullpath + 'newgazes.txt'
    newgazesfile = open(newgazestxt, "w")

    wordsperline = []
    with open(source1,'r') as file:
    
        for line in file:
            wordsperline = [] 
            
            for word in line.split():
                wordsperline.append(word)

            for i in range(len(wordsperline)):
                if(i==0):
                    index = wordsperline[i]
                    newgazesfile.write(index + "\t")

                if(i==1):
                    xorig = int(wordsperline[i]) - origcenter[0]
                    xfinal = round((dxorig/dxfinal)*(finalanal[0]/origanal[0])*xorig)
                    xgaze = int( finalcenter[0] + xfinal )
                    newgazesfile.write( str(xgaze) + "\t")

                if(i==2):
                    yorig = int(wordsperline[i]) - origcenter[1]
                    yfinal=round((dyorig/dyfinal)*(finalanal[1]/origanal[1])*yorig)
                    ygaze = int( finalcenter[1] + yfinal )
                    newgazesfile.write( str(ygaze) + "\t")

                if(i==3):
                    timestamp = wordsperline[i]
                    newgazesfile.write( timestamp + "\t")
                
                if(i==4):
                    roi = wordsperline[i]
                    newgazesfile.write( roi + "\t")
                

            newgazesfile.write("\n")

    newgazesfile.close()

    shutil.copyfile(newgazestxt, source1)
    os.remove(newgazestxt)

    print("Conversion completed...\n")


# folder1 = '/Radar_Iro_copy/'
# folder2 = 'individual/'
# subject_no = 11516
# text = 'visit'
# textgazefile= 'be_11516_1_visit_wa_1_2_2022-03-11-01.15.29'

# screenconvert(folder1, folder2, textgazefile, subject_no)