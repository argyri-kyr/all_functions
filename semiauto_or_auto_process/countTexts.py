
from asyncio.windows_events import NULL

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass


#Sinarthsh opou epistrefei posa keimena 'visit', 'zoo', ..... exw sinolika mesa sto fakelo individual.
#Th sinarthsh auth thn eixa xrhsimopoihsei gia na brw apodosh algorithmou(posa crush eixa apo ta posa sinolika keimena)
def countTexts():
    from_runcrashes = False
    c1 = 0
    c2 = 0
    c3 = 0
    c4 = 0

    exam = 1
    texts = [ 'visit', 'zoo', 'visitloud', 'psaras', 'morning', 'island', 'efeyreseis', 'zebra', 'armyjet', 'armyjetus', 'enemypie', 'enemypieus', 'gasmask', 'jockey', 'midfred', 'midfredloud', 'sunny', 'sunnyloud' ]
    subs = [i for i in range(11601, 11728)]
    for sub1 in subs:
        #Texts Data
        array = getGazesFoldersandClass(sub1)  #Sunarthsh opoy epistrefei thn taxi toy subject kai oloys tous fakelous pou periexoun gazes.txt arxeia 
        
        if( array==NULL ):
            print("Subject %d does't exist" %sub1)
            continue
        
        gazesfolders, sub1class, subexam = array[0], array[1], array[2]

        for text in texts:
            file = getGazesFolderbyText(sub1, exam, text, gazesfolders, sub1class, from_runcrashes)

            if( file != NULL ):
                if(text=='visit'):
                    c1 += 1
                if(text=='zoo'):
                    c2 += 1
                if(text=='morning' or text=='efeyreseis' or text=='psaras' or text=='zebra'):
                    c3 += 1
                if(text=='visitloud'):
                    c4 += 1    

    return c1, c2, c3, c4


results = countTexts()
print("\nvisit = ", results[0])
print("zoo = ", results[1])
print("morning + zebra + psaras + efeyreseis = ", results[2])
print("visitloud = ", results[3])