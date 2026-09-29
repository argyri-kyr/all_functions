

import pandas as pd
import os

from getGazesFolder import getGazesFolder


def create_birth_txt_from_db(start, end, output_basepath, dob_value, id_birth_dataframe):

    for subno in range(start, end + 1):
        subjectpath = output_basepath + 'subject_' + str(subno) + '/'
        if not os.path.exists(subjectpath):
            continue
        
        if( id_birth_dataframe is None ):
            dob = dob_value
        else:
            sub_id_birth = id_birth_dataframe[id_birth_dataframe['ID'] == subno]
            if sub_id_birth.empty:
                print(f"No DOB found for subject {subno}.")
                continue
            dob = sub_id_birth['DOB'].values[0]
        
        dob = pd.to_datetime(dob)
        dob_str = dob.strftime('%Y-%m-%d')
        
        gazesfolders = getGazesFolder(subno, subjectpath)
        
        birth_txt_path = subjectpath + gazesfolders[0] + '/' + dob_str + '.txt'
        
        with open(birth_txt_path, 'w', encoding='utf-8') as f:
            pass
        print(f"Created {dob_str}.txt for subject {subno} with DOB {dob_str}.")

