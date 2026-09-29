

import os

from globalVars import folder1, folder2, pyimagepath


def make_textfolder_struct(sub, exam, text):
    # Make the folders (if not exist) that i will use to store graphs and data for my texts
    if not os.path.exists(folder1 + folder2 + 'subject_' + str(sub) + '/all_data/' + text + str(exam)):
        os.makedirs(folder1 + folder2 + 'subject_' + str(sub) + '/all_data/' + text + str(exam))

    if not os.path.exists(folder1 + folder2 + 'subject_' + str(sub) + '/all_graphs/' + text + str(exam)):
        os.makedirs(folder1 + folder2 + 'subject_' + str(sub) + '/all_graphs/' + text + str(exam))
                
    if not os.path.exists(folder1 + folder2 + 'subject_' + str(sub) + '/all_graphs/' + text + str(exam) + pyimagepath):
        os.makedirs(folder1 + folder2 + 'subject_' + str(sub) + '/all_graphs/' + text + str(exam) + pyimagepath)

    if not os.path.exists(folder1 + folder2 + 'subject_' + str(sub) + '/all_data/' + text + str(exam) + pyimagepath):
        os.makedirs(folder1 + folder2 + 'subject_' + str(sub) + '/all_data/' + text + str(exam) + pyimagepath)
    
    if not os.path.exists(folder1 + folder2 + 'subject_' + str(sub) + '/all_graphs/' + text + str(exam) + '/py/extra_plots'):
        os.makedirs(folder1 + folder2 + 'subject_' + str(sub) + '/all_graphs/' + text + str(exam) + '/py/extra_plots')