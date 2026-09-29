   


import pandas as pd
   
   
from globalVars import folder1, textends



def syllabanalysisfortext1(text):
    
    data = pd.read_excel(folder1 + 'texts/' + text + textends + '/ΣΦ1 ' + text + '.xlsx', sheet_name="Sheet1", header=None)
    
    words = data.iloc[:,0].to_list()
    
    wordsroi = data.iloc[:,1].to_list()
    
    wordsandroi = {}
    for i in range(len(words)):
        wordsandroi[i+1] = words[i]
    
    wordsyllabnumber = data.iloc[:,2].to_list()
    
    wordsyllab = []
    for i in range(len(wordsyllabnumber)):
        tempwordsyllab = [ data.iloc[i,j+3] for j in range(wordsyllabnumber[i])]
        wordsyllab.append(tempwordsyllab)
    
    
    wordsinitialinfodict = {}
    for i in range(len(wordsroi)):
        wordsinitialinfodict[wordsroi[i]] = [wordsyllabnumber[i], wordsyllab[i]]
    
    # print(wordsinitialinfodict)
    
    return words, wordsroi, wordsandroi, wordsyllabnumber, wordsyllab, wordsinitialinfodict