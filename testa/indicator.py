

import numpy as np
import pandas as pd


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2


def indicator(sub,ek):
    indicator_fm = 1
    indicator_m = 2

    final_indicator = -1

    if os.path.exists(folder1 + folder2 + 'subject_' + str(sub) + '/female.txt'):
        gender = "FEMALE"
        final_indicator = indicator_fm


    if os.path.exists(folder1 + folder2 + 'subject_' + str(sub) + '/male.txt'):
        gender = "MALE"
        final_indicator = indicator_m

    ek_mean = np.mean(ek)

    overall_performance_data = pd.read_excel(folder1 + folder2 + 'Overall_Performance_Grade_de.xlsx')
    
    ek_data = overall_performance_data.iloc[:,0].tolist()
    indicator_data = overall_performance_data.iloc[:,final_indicator].tolist()

    indicator = find_indicator(ek_mean, indicator_data, ek_data)

    return indicator, ek_mean




def find_indicator(ek, indicator_data, ek_data):
    indicator = -1
    if( ek > ek_data[0] ):
        indicator = indicator_data[0]

    if( ek < ek_data[-1] ):
        indicator = indicator_data[len(ek_data)-1]

    for i in range(len(ek_data)-1):
        if( ek_data[i] == ek ):
            indicator = indicator_data[i]
            break

        if( i==len(ek_data)-2 and ek_data[i+1] == ek ):
            indicator = indicator_data[i+1]
            break

        if( ek_data[i] > ek > ek_data[i+1] ):
            if( abs(ek_data[i]-ek) == abs(ek_data[i+1]-ek) ):
                indicator = indicator_data[i+1] + (indicator_data[i]-indicator_data[i+1])/2
                break
            
            if( abs(ek_data[i]-ek) > abs(ek_data[i+1]-ek) ):
                indicator = indicator_data[i+1]
                break
            
            if( abs(ek_data[i]-ek) < abs(ek_data[i+1]-ek) ):
                indicator = indicator_data[i]
                break

    
    # print("Indicator = ", Indicator)

    return indicator