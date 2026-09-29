
import os
from globalVars import folder1, textpos, textends

#Sinarthsh opou briskei poses selides exei to sigkekrimeno keimeno
def findPages(text):
    pages = 1
    
    while(True):
        if( os.path.exists(folder1 + textpos + text + textends + '/Slide' + str(pages) + '.PNG') ):
            pages += 1
        else:
            break
    
    return pages-1
        