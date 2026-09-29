
from scipy.io import loadmat
import xlsxwriter
import os
from asyncio.windows_events import NULL

folder1 = 'C:/_Iro_Analysis/'
folder2 = 'population_GRE/'

def mat2csv(sub1, text, filename):
    workbook = xlsxwriter.Workbook(folder1 + folder2 + 'subject_' +str(sub1) + '/all_data/' + text + '1/' + filename + '.xlsx')
    worksheet = workbook.add_worksheet()

    file = loadmat(folder1 + folder2 + 'subject_' +str(sub1) + '/all_data/' + text + '1/' + filename + '.mat',simplify_cells=True)
    data = file[filename].tolist()
    for i in range(len(data)):
        for j in range(len(data[0])):
            data[i][j] = round(data[i][j],2)
            
            worksheet.write(i, j, data[i][j] )
    
    workbook.close()

def main():
    subs = [i for i in range(100, 10800)]
    for sub1 in subs:
        #Check if subject exist
        subjectpath = folder1 + folder2 + 'subject_' + str(sub1) + '/'
        if not os.path.exists(subjectpath):
            continue
        
        #check whick texts this subject has read
        texts = ['visit', 'zoo', 'island', 'olympia', 'efeyreseis', 'psaras', 'zebra', 'morning']
        for  text in texts:
            textpath = folder1 + folder2 + 'subject_' +str(sub1) + '/all_data/' + text + '1/'
            if not os.path.exists(textpath):
                continue 
            

            mat2csv(sub1, text, "cutgazesFF")
            mat2csv(sub1, text, "fixationsFF")

main()