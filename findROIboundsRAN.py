
import xlsxwriter

import os,sys,inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,currentdir)

from globalVars import folder1, textpos
from drawROIRAN import drawROIRAN

def findROIboundsRAN(text):
    if not os.path.exists(folder1 + textpos + text + '/py'):
        lines = []
        ylines = []

        # Ftiaxnw arxika ton fakelo 'py' opoy mesa tha exei olh thn plhroforia tou keimenoy
        os.makedirs(folder1 + textpos + text + '/py')

        # # # Ftiaxnw olous tous ipofakelous poy tha exei mesa toy o fakelos 'py'

        # Arxika tha exei mesa enan fakelo 'pages' opou tha exei mesa ena .txt arxeio me ton arithmo twn selidwn tou keimenou
        os.makedirs(folder1 + textpos + text + '/py/pages')
        pagestxt = folder1 + textpos + text + '/py/pages/pages.txt'
        pagesfile = open(pagestxt, 'w')
        pages = findPagesROIS(text)
        pagesfile.write(str(pages))
        pagesfile.close()


        print("%s ROI analysis begins..." %text)
        os.makedirs(folder1 + textpos + text + '/py/ROIbounds')

        for pageno in range(1, 3):
            rois = drawROIRAN(text, pageno)  
            lines.append( rois[4] )
            ylines.append( rois[5] )
        
        print("%s ROI analysis is over..." %text)


        # Epishs tha exei mesa enan fakelo 'lines' opou tha exei mesa .xlsx arxeia opou tha periexoun ton arithmo twn grammwn kathe selidas tou keimenou
        os.makedirs(folder1 + textpos + text + '/py/lines')
        for pageno in range(1, 3):
            path = folder1 + textpos + text +'/py/lines/mytext.page(' + str(pageno) + ').lines.xlsx'
            workbook = xlsxwriter.Workbook(path)
            worksheet = workbook.add_worksheet()
            worksheet.write(0, 0, 'lines')
            worksheet.write(1, 0, lines[pageno-1])
            workbook.close()


        # Epishs tha exei mesa enan fakelo 'Yline' opou tha exei mesa .xlsx arxeia opou tha periexei thn plhroforia gia thn yline kathe grammis
        os.makedirs(folder1 + textpos + text + '/py/Yline')
        for pageno in range(1, 3):
            path = folder1 + textpos + text +'/py/Yline/mytext.page(' + str(pageno) + ').line.yline.xlsx'
            workbook = xlsxwriter.Workbook(path)
            worksheet = workbook.add_worksheet()
            worksheet.write(0, 0, 'yline')

            for lineno in range(1,lines[pageno-1]+1):
                worksheet.write(lineno, 0, ylines[pageno-1][lineno-1])
            
            workbook.close()



def findPagesROIS(text):
    pages = 1
    
    while(True):
        if( os.path.exists(folder1 + textpos + text + '/Slide' + str(pages) + '.PNG') ):
            pages += 1
        else:
            break
    
    return pages-1


text = "RAN_1920"
findROIboundsRAN(text)