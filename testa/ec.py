


import pandas as pd

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2


def ec(sub, scorelist):
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

    equivallent_class_data = pd.read_excel(folder1 + folder2 + 'Equivalent_Class_Grade_de.xlsx')
    
    ec_data = equivallent_class_data.iloc[1:,0].tolist()
    decoding_data = equivallent_class_data.iloc[1:,final_decoding].tolist()
    fluency_data = equivallent_class_data.iloc[1:,final_fluency].tolist()
    morphology_data = equivallent_class_data.iloc[1:,final_morphology].tolist()
    comprehension_data = equivallent_class_data.iloc[1:,final_comprehension].tolist()

    decoding_ec = find_ec(s1, ec_data, decoding_data)
    fluency_ec = find_ec(s2, ec_data, fluency_data)
    morphology_ec = find_ec(s3, ec_data, morphology_data)
    comprehension_ec = find_ec(s4, ec_data, comprehension_data)

    return decoding_ec, fluency_ec, morphology_ec, comprehension_ec
            
            

def find_ec(score, ec_data, list_data):
    ec = -1
    if( score > list_data[0] ):
        ec = ec_data[0]

    if( score < list_data[-1] ):
        ec = ec_data[len(list_data)-1]

    for i in range(len(list_data)-1):
        if( list_data[i] == score ):
            ec = ec_data[i]
            break

        if( i==len(list_data)-2 and list_data[i+1] == score ):
            ec = ec_data[i+1]
            break

        if( list_data[i] > score > list_data[i+1] ):
            if( abs(list_data[i]-score) == abs(list_data[i+1]-score) ):
                ec = ec_data[i+1] + (ec_data[i]-ec_data[i+1])/2
                break
            
            if( abs(list_data[i]-score) > abs(list_data[i+1]-score) ):
                ec = ec_data[i+1]
                break
            
            if( abs(list_data[i]-score) < abs(list_data[i+1]-score) ):
                ec = ec_data[i]
                break
            
    
    # print("EC = ", EC)

    return ec







# sub = 13043
# ec(sub)