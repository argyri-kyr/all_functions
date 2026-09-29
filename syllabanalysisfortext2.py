   


import pandas as pd
   
   
from globalVars import folder1, textends



def syllabanalysisfortext2(text): 
    
    data = pd.read_excel(folder1 + 'texts/' + text + textends + '/ΣΦ2 ' + text + '.xlsx', sheet_name="Sheet1")
    
    words = data.iloc[:,0].to_list()
    
    wordsroi = data.iloc[:,1].to_list()

    wordsandroi = {}
    for i in range(len(words)):
        wordsandroi[i+1] = words[i]
    
    wordsyllabnumber = data.iloc[:,2].to_list()
    
    wordsyllab = data.iloc[:,3].to_list()
    
    wordsinitialinfodict = {}
    for i in range(len(wordsroi)):
        wordsinitialinfodict[wordsroi[i]] = [wordsyllabnumber[i], wordsyllab[i]]
    
    # print(wordsinitialinfodict)
    
    return words, wordsroi, wordsandroi, wordsyllabnumber, wordsyllab, wordsinitialinfodict