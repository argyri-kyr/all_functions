

import pandas as pd

from globalVars import folder1, textends


def decodingErrors(text, wordsselectedpath, data1, data2, data3):
    data = pd.read_excel (folder1 + 'texts/' + text + textends + '/py/mytext/allwordspure.xlsx', header=None)
    allwords = []
    allwords = data.iloc[:,0]
    allwords = allwords.to_list()
    allwords_numbers = [i+1 for i in range(len(allwords))]
    
    selectedwords = []
    for i in range(len(data1)):
        if(data1[i] in allwords_numbers):
            selectedwords.append(allwords[data1[i]-1])
    
    errorcategories = {1:"Παραποίηση: ", 2:"Παράλειψη: ", 3:"Προσθήκη μετά από: ", 4:"Παρατονισμός: ", 5:"Αυτοδιόρθωση: ", 6:"Επανάληψη: ", 7:"Γενική κατηγορία: "}
    finalreport = []
    for i in range(len(data1)):
        finalreport.append(errorcategories[data2[i]] + selectedwords[i] + " , Σχόλια: " + " ".join(data3[i]))
    
    with open(wordsselectedpath, 'w') as wordsfile:
        wordsfile.write('\n'.join(result for result in finalreport))
        wordsfile.write("\n")