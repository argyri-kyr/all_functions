
import pandas as pd

from globalVars import folder1, textends

#Βρισκω ποσες γραμμες εχει η σελιδα που βρισκομαι
def findpagelines(text, pageno):
    data = pd.read_excel (folder1 + 'texts/' + text + textends + '/py/lines/mytext.page(' + str(pageno) + ').lines.xlsx')
    x = data.iloc[:,0]
    return x[0]
