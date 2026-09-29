

import os,sys,inspect
import shutil
from asyncio.windows_events import NULL


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2


def modify_gazes_timestamp_for_ivan(sub1, file, text, operation_var):

    gazesfilepath = os.path.join(folder1, folder2, 'subject_' + str(sub1), file, 'gazes.txt')
    
    if(operation_var.get() == 'division'):
        gazesfilepath_copied = os.path.join(folder1, folder2, 'subject_' + str(sub1), file, 'gazes_ivan.txt')
        shutil.copy(gazesfilepath, gazesfilepath_copied)
    
    elif(operation_var.get() == 'multiply'):
        gazesfilepath_copied = os.path.join(folder1, folder2, 'subject_' + str(sub1), file, 'gazes_legacy.txt')
        shutil.copy(gazesfilepath, gazesfilepath_copied)
    else:
        print('No change in gazes.py. No operation recognized.')
        return NULL, NULL
        
    with open(gazesfilepath, "r") as f:
        lines = f.readlines()

    # Check column count from first non-empty line
    size = 0
    for p in lines:
        cols = p.split()
        if cols:
            size = len(cols)
            break

    if size < 7:
        return None, None

    new_lines = []
    pageno = 0

    for p in lines:
        cols = p.split()
        if not cols:
            new_lines.append(p)
            continue

        pageno += 1

        if text == 'decodedecision' and pageno > 6:
            break

        original_ts = float(cols[9])

        if operation_var.get() == 'division':
            new_ts = str(int(original_ts / 1000))
        if operation_var.get() == 'multiply':
            new_ts = str(int(original_ts * 1000))


        # Replace only the 10th token in the original line, preserving all spacing
        new_line = p.replace(cols[9], new_ts, 1)
        new_lines.append(new_line)

    # Overwrite the original file with modified content
    with open(gazesfilepath, "w") as f:
        f.writelines(new_lines)

    return gazesfilepath, len(new_lines)