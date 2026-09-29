
from asyncio.windows_events import NULL
from scipy.io import loadmat


from globalVars import folder1, folder2, textends, guiflag
from basic_function_gui import basic_function_gui
from drawFixations import drawFixations


def fixations_procedure():
    
    exam = 1
    
    if( guiflag ):
        textcheckedflag = 1
        subs = NULL
        while( subs==NULL ):
            subs, texts, firstchoices = basic_function_gui(textcheckedflag)
            bypass, hardcases, onlylefteye, onlyrighteye = firstchoices[0], firstchoices[1], firstchoices[2], firstchoices[3]
    
    else:
        subs = [12105]
        texts = ['zoo']
        bypass = 0
        hardcases = 0
        onlylefteye = 0
        onlyrighteye = 0
        firstchoices = [bypass, hardcases, onlylefteye, onlyrighteye]
        
    
    for sub1 in subs:
        for text in texts:
            text_pages = int( open(folder1 + 'texts/' + text + textends + '/py/pages/pages.txt').readline() )
            for pageno in range(1, text_pages+1):
                fixationspath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/fixations.mat'
                fixationsmat = loadmat(fixationspath, simplify_cells=True)
                fixationdata = list(fixationsmat['fixations'][pageno-1]['values'])
                drawFixations(sub1, exam, text, fixationdata, pageno, "yes", NULL)

  

fixations_procedure()