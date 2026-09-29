


import pandas as pd

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2


def ek(sub, scorelist):
    decoding_fm = 1
    decoding_m = 2
    fluency_fm = 3
    fluency_m = 4
    morphology_fm = 5
    morphology_m = 6
    comprehension_fm = 7
    comprehension_m = 8

    final_decoding = -1
    final_fluency = -1
    final_morphology = -1
    final_comprehension = -1

    if os.path.exists(folder1 + folder2 + 'subject_' + str(sub) + '/female.txt'):
        gender = "FEMALE"
        final_decoding = decoding_fm
        final_fluency = fluency_fm
        final_morphology = morphology_fm
        final_comprehension = comprehension_fm

    if os.path.exists(folder1 + folder2 + 'subject_' + str(sub) + '/male.txt'):
        gender = "MALE"
        final_decoding = decoding_m
        final_fluency = fluency_m
        final_morphology = morphology_m
        final_comprehension = comprehension_m
    

    s1 = scorelist[0]
    s2 = scorelist[1]
    s3 = scorelist[2]
    s4 = scorelist[3]

    typical_score_data = pd.read_excel(folder1 + folder2 + 'Typical_Score_Grade_de.xlsx')
    
    ek_data = typical_score_data.iloc[1:,0].tolist()
    decoding_data = typical_score_data.iloc[1:,final_decoding].tolist()
    fluency_data = typical_score_data.iloc[1:,final_fluency].tolist()
    morphology_data = typical_score_data.iloc[1:,final_morphology].tolist()
    comprehension_data = typical_score_data.iloc[1:,final_comprehension].tolist()

    decoding_ek = find_ek(s1, ek_data, decoding_data)
    fluency_ek = find_ek(s2, ek_data, fluency_data)
    morphology_ek = find_ek(s3, ek_data, morphology_data)
    comprehension_ek = find_ek(s4, ek_data, comprehension_data)

    return decoding_ek, fluency_ek, morphology_ek, comprehension_ek
            
            

def find_ek(score, ek_data, list_data):
    ek = -1
    if( score > list_data[0] ):
        ek = ek_data[0]

    if( score < list_data[-1] ):
        ek = ek_data[len(list_data)-1]

    for i in range(len(list_data)-1):
        if( list_data[i] == score ):
            ek = ek_data[i]
            break

        if( i==len(list_data)-2 and list_data[i+1] == score ):
            ek = ek_data[i+1]
            break

        if( list_data[i] > score > list_data[i+1] ):
            if( abs(list_data[i]-score) == abs(list_data[i+1]-score) ):
                ek = ek_data[i+1] + (ek_data[i]-ek_data[i+1])/2
                break
            
            if( abs(list_data[i]-score) > abs(list_data[i+1]-score) ):
                ek = ek_data[i+1]
                break
            
            if( abs(list_data[i]-score) < abs(list_data[i+1]-score) ):
                ek = ek_data[i]
                break
            
    
    # print("EK = ", ek)

    return ek







# sub = 13043
# ek(sub)