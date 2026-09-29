

import pandas as pd


from globalVars import folder1, textends


# Φτιαχνω τις λιστες με τα cutgazes(index, x, y, timestamp)
def calculateYline(text, pageno):
    data = pd.read_excel (folder1 + 'texts/' + text + textends + '/py/Yline/mytext.page(' + str(pageno) + ').line.yline.xlsx')
    yline = []
    yline = data.iloc[:,0]
    yline = yline.to_list()

    return yline