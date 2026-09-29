
import pandas as pd
import ctypes

from globalVars import folder1, textends


def checkValidNotes(text, getParam):
    end_index = getParam("text_box").index("end linestart")
    mynotes = getParam("text_box").get("1.0", end_index)
    print("\nNotes: \n", mynotes)
    mynotes = mynotes.split("\n")
    
    data1 = []  # roi
    data2 = []  # kathgoria lathous
    data3 = []  # sxolio
    
    # valid lista gia ta input ths defterhs sthlhs
    validcategories = [1,2,3,4,5,6,7]

    # valid lista gia ta input ths prwths sthlhs
    data = pd.read_excel (folder1 + 'texts/' + text + textends + '/py/mytext/allwordspure.xlsx', header=None)
    allwords = []
    allwords = data.iloc[:,0]
    allwords = allwords.to_list()
    allwords_numbers = [i+1 for i in range(len(allwords))]
    
    # check if "\n" exist in the end, if so, delete it
    mynotesfinal = []
    for i in range(len(mynotes)):
        if(mynotes[i]!=''):
           mynotesfinal.append(mynotes[i])
    
    # check if text entry is valid
    wrongNotes = False
    collectwronglines = []
    for j in range(len(mynotesfinal)):
        linenotes = mynotesfinal[j].split(" ")
              
        if( len(linenotes)==0 or len(linenotes)==1 ):
            wrongNotes = True
            collectwronglines.append(j+1) 
            continue
        elif( ((linenotes[0].isdigit()) and (int(linenotes[0]) not in allwords_numbers)) or ((linenotes[1].isdigit()) and (int(linenotes[1]) not in validcategories)) ):
            wrongNotes = True
            collectwronglines.append(j+1) 
            continue 
        elif( ((linenotes[0].isdigit()) and (int(linenotes[0]) in allwords_numbers)) and ((linenotes[1].isdigit()) and (int(linenotes[1]) in validcategories)) ): 
            continue 
        else:
            wrongNotes = True
            collectwronglines.append(j+1)
    
    if(wrongNotes):
        ctypes.windll.user32.MessageBoxW(0, "Wrong Notes!\nCheck lines " + str(collectwronglines), "Warning!", 16)
    
    # if text entry is valid collect the data
    else:
        collectwronglines = []
        for j in range(len(mynotesfinal)):
            linenotes = mynotesfinal[j].split(" ")
            if( len(linenotes)==2 ):
                data1.append(int(linenotes[0]))
                data2.append(int(linenotes[1])) 
                data3.append([''])
            if( len(linenotes)>=3 ):
                data1.append(int(linenotes[0]))
                data2.append(int(linenotes[1]))
                data3.append(linenotes[2:]) 
            
    
    return wrongNotes, data1, data2, data3