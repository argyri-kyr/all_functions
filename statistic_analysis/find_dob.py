



import os
import re
from datetime import datetime


from getGazesFolder import getGazesFolder


# Sinarthsh opou elegxei ean o fakelos pou diavasa einai ontws ths morfhs be_11622_1_morning_wa_8_2_2022-04-07-09.07.31, elegxontas ean mesa sta orismata(ean o fakelos ginei split me basei to xarakthra '_') tou fakelou brethei kapou to id tou subject
def textFolder(subno, folder):
    l = folder.split("_")
    
    if( len(l) > 1 ):
        if( str(subno) == l[1] ):
            return True
    
    return False

def find_dob(subno, filepath):
    gazesfolders = getGazesFolder(subno, filepath)
    
    dob = ''
    dob_found = False
    
    for folder in gazesfolders:
        # Define folderpath
        folder_path = os.path.join(filepath, folder)
        
        # pattern for YYYY-MM-DD.txt
        pattern = re.compile(r"^(\d{4})-(\d{2})-(\d{2})\.txt$")

        for filename in os.listdir(folder_path):
            match = pattern.match(filename)
            if match:
                year, month, day = match.groups()

                # convert to date format you want: 25/2/2005
                date_obj = datetime(int(year), int(month), int(day))
                dob = date_obj.strftime("%d/%m/%Y")
                dob_found = True
                break
        
        if dob_found:
            break

    return dob