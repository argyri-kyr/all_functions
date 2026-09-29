
from scipy.io import loadmat
import xlsxwriter
import os

folder1 = 'C:/_Iro_Analysis/'
folder2 = 'population_GRE/'

def mat2csv(sub1):
    workbook = xlsxwriter.Workbook(folder1 + folder2 + 'subject_' +str(sub1) + '/info.xlsx')
    worksheet = workbook.add_worksheet()

    file = loadmat(folder1 + folder2 + 'subject_' +str(sub1) + '/info.mat', simplify_cells=True)
    dict = file['info']
    texts = list( dict.keys() )
    info = list( dict.values() )

    #Write first column with texts
    j=0
    for i in range(len(texts)):
        worksheet.write(i, j, texts[i])


    #Write second column with infos
    j=1
    for i in range(len(info)):
        worksheet.write(i, j, info[i])
    
    workbook.close()


def main():
    subs = [i for i in range(100, 10800)]
    
    for sub1 in subs:

        #Check if subject exist
        subjectpath = folder1 + folder2 + 'subject_' + str(sub1) + '/'
        if not os.path.exists(subjectpath):
            continue
        
        #check in info.mat exists
        infopath = folder1 + folder2 + 'subject_' +str(sub1) + '/info.mat'
        if not os.path.exists(infopath):
            continue 


        mat2csv(sub1)

main()