

import xlsxwriter
import pandas as pd
import os

general_path = "//MREYE2/Shared folder/_IRO/Σχ. Πόλεων VS Υπαίθρου/"
text = 'zoo'

def classify_school_param(worksheet, merge_format, param):
    totaldata = pd.ExcelFile( general_path + text + '.xlsx' )
    
    # collect data for my parameter
    data1 = pd.read_excel(totaldata, param)
    data1_ids = data1.iloc[:,0].tolist()
    data1_param = data1.iloc[:,1].tolist()
    data1_school = data1.iloc[:,2].tolist()


    totalsubs = len([x for x in data1_ids if x==x])
    p1 = int( 0.25 * totalsubs )
    p2 = int( 0.50 * totalsubs )
    p3 = int( 0.75 * totalsubs )
    p4 = totalsubs


    # count total occurences of each school
    schools_dict = {}
    for sc in data1_school:
        if sc in schools_dict:
            schools_dict[sc] += 1
        else:
            schools_dict[sc] = 1
    

    # count occurences of each school in percentile p1
    school_classification1 = {}
    for no in range(p1):
        school = data1_school[no]
        if( school in school_classification1 ):
            school_classification1[school] += 1
        else:
            school_classification1[school] = 1
    
    school_classification1 = dict(sorted(school_classification1.items()))


    # count occurences of each school in percentile p2 
    school_classification2 = {}
    for no in range(p1, p2):
        school = data1_school[no]
        if( school in school_classification2 ):
            school_classification2[school] += 1
        else:
            school_classification2[school] = 1
    
    school_classification2 = dict(sorted(school_classification2.items()))



    # count occurences of each school in percentile p3   
    school_classification3 = {}
    for no in range(p2, p3):
        school = data1_school[no]
        if( school in school_classification3 ):
            school_classification3[school] += 1
        else:
            school_classification3[school] = 1

    school_classification3 = dict(sorted(school_classification3.items()))




    # count occurences of each school in percentile p4 
    school_classification4 = {}
    for no in range(p3, p4):
        school = data1_school[no]
        if( school in school_classification4 ):
            school_classification4[school] += 1
        else:
            school_classification4[school] = 1
    
    school_classification4 = dict(sorted(school_classification4.items()))



    # extra for every parameter, add in excel the schools that doesnt exist in a percentile as zero population
    for no in range(len(data1_school)):
        school = data1_school[no]

        if( school not in school_classification1 ):   # check for p1 percentile
            school_classification1[school] = 0
            
        if( school not in school_classification2 ):   # check for p2 percentile
            school_classification2[school] = 0

        if( school not in school_classification3 ):   # check for p3 percentile
            school_classification3[school] = 0

        if( school not in school_classification4 ):   # check for p4 percentile
            school_classification4[school] = 0


   
    # TOTAL SUM per row
    totalrowsum = []
    res1 = list(school_classification1.values())
    res2 = list(school_classification2.values())
    res3 = list(school_classification3.values())
    res4 = list(school_classification4.values())
    for i in range(len(school_classification2)):
        totalrowsum.append( res1[i] + res2[i] + res3[i] + res4[i])
    


    # # # # #  write in excel  # # # # #

    worksheet.merge_range('A1:B1', '25%', merge_format) 
    worksheet.write_column(1, 0, list(school_classification1.keys()))
    worksheet.write_column(1, 1, list(school_classification1.values()))


    worksheet.merge_range('D1:E1', '50%', merge_format) 
    worksheet.write_column(1, 3, list(school_classification2.keys()))
    worksheet.write_column(1, 4, list(school_classification2.values()))


    worksheet.merge_range('G1:H1', '75%', merge_format)
    worksheet.write_column(1, 6, list(school_classification3.keys()))
    worksheet.write_column(1, 7, list(school_classification3.values()))


    worksheet.merge_range('J1:K1', '100%', merge_format)
    worksheet.write_column(1, 9, list(school_classification4.keys()))
    worksheet.write_column(1, 10, list(school_classification4.values()))



    worksheet.write('M1', 'TOTAL', merge_format)
    worksheet.write_column(1, 12, totalrowsum)
    worksheet.write(18, 1, '= ' + str(sum(list(school_classification1.values()))))
    worksheet.write(18, 4, '= ' + str(sum(list(school_classification2.values()))))
    worksheet.write(18, 7, '= ' + str(sum(list(school_classification3.values()))))
    worksheet.write(18, 10, '= ' + str(sum(list(school_classification4.values()))))
    worksheet.write(18, 12, '= ' + str(sum(totalrowsum)))



    return




def main():
    folder_name = general_path + 'school_classification2_' + text + '.xlsx'
    if(os.path.exists(folder_name)):
        os.remove(folder_name)

    workbook = xlsxwriter.Workbook(folder_name)

    merge_format = workbook.add_format({
        'bold':     True,
        'border':   1,
        'align':    'center',
        'valign':   'vcenter',
        'fg_color': '#C4D79B',
    })

    params = ['fluency', 'anticip', 'proc speed', 'long pauses']

    for param in params:
        worksheet = workbook.add_worksheet(param)
        classify_school_param(worksheet, merge_format, param)

    workbook.close()


main()