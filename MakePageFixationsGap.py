

import xlsxwriter

from globalVars import folder1, folder2


def MakePageFixationsGap(sub1, exam, text, pageno, gazestart, gazeend, fixationstart, fixationend, gap_data):
    fixationsboundstxt = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/fixations_gap_data' + str(pageno) + '.xlsx' #Αυτο το αρχειο ειναι το αντιστοιχο του fixationsFF που δημιουργει το matlab με προσθετη στηλη στο τελος τη στηλη του timestampend
    fixationboundsbook  = xlsxwriter.Workbook(fixationsboundstxt)
    worksheetstartend = fixationboundsbook.add_worksheet("start_end")
    worksheetstartend.write(0, 0, 'gazestart')
    worksheetstartend.write_column(1, 0, gazestart)
    worksheetstartend.write(0, 1, 'gazeend')
    worksheetstartend.write_column(1, 1, gazeend)
    worksheetstartend.write(0, 2, 'fixationstart')
    worksheetstartend.write_column(1, 2, fixationstart)
    worksheetstartend.write(0, 3, 'fixationend')
    worksheetstartend.write_column(1, 3, fixationend)

    worksheetfixationgap = fixationboundsbook.add_worksheet("fixation_gap")
    worksheetfixationgap.write_row(0, 0, ["first_fixation", "last_fixation", "ROI_first", "ROI_last", "x_first", "y_first", "x_last", "y_last", "duration"])
    for fg in range(len(gap_data)):
        worksheetfixationgap.write_row(fg+1, 0, gap_data[fg])

    fixationboundsbook.close()