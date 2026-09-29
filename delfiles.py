

from asyncio.windows_events import NULL
import shutil

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2, guiflag
from basic_function_gui import basic_function_gui
from GetSomeInitialData import getGazesFoldersandClass



def main():

    if( guiflag ):
        # Get Subject's Data from an Input Dialogue  
        textcheckedflag = 1
        subs = NULL
        while( subs==NULL ):
            subs, texts, firstchoices = basic_function_gui(textcheckedflag)
            bypass, hardcases, onlylefteye, onlyrighteye = firstchoices[0], firstchoices[1], firstchoices[2], firstchoices[3]

    else:
        # texts = [ 'visit', 'zoo', 'visitloud', 'psaras', 'morning', 'island', 'efeyreseis', 'zebra', 'armyjet', 'enemypie', 'gasmask', 'jockey', 'midfred', 'midfredloud', 'sunny', 'sunnyloud' ]
        # texts = ['morning', 'visit', 'zoo', 'efeyreseis']
        texts = ['todelete']

        #Orizw poia einai ta subjects pou thelw na treksw
        # subs = [696, 729, 11512, 11514, 11520, 11521, 11522, 11523, 11524, 11525, 11526, 11527, 11528, 11529, 11530, 11531, 11532, 11533, 11534, 11535, 11536, 11537, 11538, 11539, 11540, 11548]   #subject id
        # subs = [11513, 11514, 11521, 11522, 11523, 11525, 11526, 11529, 11530, 11532, 11533, 11534, 11536, 11538, 11540, 11544, 11545, 11548, 11549, 11550, 11551, 11553]
        # subs = [5007, 5025, 5032, 5037, 5038, 5044, 5045, 5051, 5053, 5064, 5068, 5069, 5077, 5082, 5085, 5089, 5094, 5098, 5122, 5123, 5140, 5144]
        subs = [14301]
        # subs = [1455, 1456, 1459, 1460, 1461]
        # subs = [ person  for person  in range(908, 920) ]

        bypass = 0
        hardcases = 0
        onlylefteye = 0
        onlyrighteye = 0
        firstchoices = [bypass, hardcases, onlylefteye, onlyrighteye]
        

    # Orizw se poia exam einai to kathe subject
    exam = []


    # Kuria while loop gia na trexoun ola ta subject pou thelw ( trexw 1h loop gia ta subject kai 2h eswterikh loop gia ta texts tou subject )
    for i in range(len(subs)): 
        array = getGazesFoldersandClass(subs[i])  #Sunarthsh opoy epistrefei thn taxi toy subject kai oloys tous fakelous pou periexoun gazes.txt arxeia,dhladh dedomena gia kapoio keimeno
        
        if( array==NULL ):
            # print("Subject %d does't exist" %subs[i])
            continue                    
                             
            
        # Make the folders (if not exist) that i will use to store graphs and data for my texts
        datapath = folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_data/'
        if os.path.exists( datapath ):
            shutil.rmtree( datapath )
            
        graphpath = folder1 + folder2 + 'subject_' + str(subs[i]) + '/all_graphs/'
        if os.path.exists( graphpath ):
            shutil.rmtree( graphpath )



main()