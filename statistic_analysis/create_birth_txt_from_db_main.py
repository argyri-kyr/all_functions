

from create_birth_txt_from_db import create_birth_txt_from_db
import pandas as pd

def create_birth_txt_from_db_main():
    input_basepath = 'I:/'
    input_db_name = 'IERAPETRA DB_v1.xlsx'
    input_dof_filepath = input_basepath + input_db_name
    dof_df = pd.read_excel(input_dof_filepath)
    id_birth_dataframe = dof_df[['ID', 'DOB']]
    
    start = 14601
    end = 14712
    
    # output_basepath = 'M:/population/'
    output_basepath = 'I:/'

    dob_value = None
    create_birth_txt_from_db(start, end, output_basepath, dob_value, id_birth_dataframe)

# create_birth_txt_from_db_main()