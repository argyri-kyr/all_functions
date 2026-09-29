


import pandas as pd
import xlsxwriter


def find_worst_students():
    totaldata = pd.ExcelFile('Y:/the_worst_students_compared_to _greeks.xlsx')
    
    data1 = pd.read_excel(totaldata, 'maxvis')
    data1_ids = data1.iloc[:,0].tolist()

    data2 = pd.read_excel(totaldata, 'stopwatchtime')
    data2_ids = data2.iloc[:,0].tolist()

    data3 = pd.read_excel(totaldata, 'Saclen')
    data3_ids = data3.iloc[:,0].tolist()

    data4 = pd.read_excel(totaldata, 'total score')
    data4_ids = data4.iloc[:,0].tolist()

    compare = 70

    data1_ids = data1_ids[:compare]
    data2_ids = data2_ids[:compare]
    data3_ids = data3_ids[:compare]
    data4_ids = data4_ids[:compare]

    subs = UnionNoRepeat(data1_ids, data2_ids, data3_ids, data4_ids)

    where_appear_total = []
    count_appears_total = []

    for i in range(len(subs)):
        count = 0
        where_appear_sub = [ subs[i] ]

        if( subs[i] in data1_ids ):
            count += 1
            where_appear_sub.append("maxvis")
        
        if( subs[i] in data2_ids ):
            count += 1
            where_appear_sub.append("stopwatchtime")

        if( subs[i] in data3_ids ):
            count += 1
            where_appear_sub.append("Saclen")

        if( subs[i] in data4_ids ):
            count += 1
            where_appear_sub.append('total score')
        

        where_appear_total.append(where_appear_sub)
        count_appears_total.append( [subs[i], count] )

    write_results_in_excel(where_appear_total, 'Y:/where_appear_worst_students.xlsx')
    write_results_in_excel(count_appears_total, 'Y:/counts_appears_worst_students.xlsx')

    return where_appear_total, count_appears_total


def UnionNoRepeat(lst1, lst2, lst3, lst4): 
    final_list = list(set().union(lst1, lst2, lst3, lst4))
    return final_list


def write_results_in_excel(students_list, folder_name):
    with xlsxwriter.Workbook(folder_name) as workbook:
        worksheet = workbook.add_worksheet()

        for row_num, data in enumerate(students_list):
            worksheet.write_row(row_num, 0, data)



find_worst_students()