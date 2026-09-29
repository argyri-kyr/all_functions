
from asyncio.windows_events import NULL

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2

def storefinalindexes(sub1, pageno, file, finalindexes):
    # # store finalindexes ( X coord )
    if(finalindexes != NULL):
        finalindexestxt = folder1 + folder2 + '/subject_' + str(sub1) + '/' + file + '/py/finalindexes_page' + str(pageno) + '.txt'
        finalindexesfile = open(finalindexestxt, 'w')
        for row in range(len(finalindexes)):
            finalindexesfile.write(str(finalindexes[row]))
            finalindexesfile.write("\n")
        finalindexesfile.close()  