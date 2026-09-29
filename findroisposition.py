

import pandas as pd

from globalVars import folder1, textends

def findroisposition(text, pageno):
    position = 0
    if( pageno == 1 ):
        position = 0

    else:
        for index in range(1, pageno):
            prevpath = folder1 + 'texts/' + text + textends + '/py/ROIbounds/mytext.page_' + str(index) + '.ROIbounds.xlsx'
            prevdata = pd.read_excel (prevpath)
            position += len(prevdata)
    
    return position
