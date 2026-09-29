


from asyncio.windows_events import NULL


from globalVars import folder1
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass


def testscoring():
    subs = [x for x in range(13369, 13373)]

    for sub in subs:
        allsubtexts = []
        search1 = getGazesFoldersandClass(sub)   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/
        if( search1 == NULL ):
            print("\nSubject= ", sub, "doesn't exist")
            continue
        
        print("\nSubject = ", sub)
        for text in texts:
            from_runcrashes = False

            gazesfolders1, subclass, subexam = search1[0], search1[1], search1[2]   # gazesfolders1 : ta keimena pou brethikan mesa sto individual
            gazesfolders = gazesfolders1 
            gazesfolders = list(dict.fromkeys(gazesfolders))               

            file = getGazesFolderbyText(sub, subexam, text, gazesfolders, subclass, from_runcrashes)
            if(file==NULL):
                # print("There is no data for this text")
                continue
            
            allsubtexts.append(file)
            
        wav_durations, allin_seconds = totalreadingtime(sub, allsubtexts)






def main():
    