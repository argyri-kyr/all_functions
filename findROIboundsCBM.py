import xlsxwriter

import os,sys,inspect
from SplitWords import mainSplit
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,currentdir)

from globalVars import folder1, textpos
from ROIcalculationCBM import drawROI
from SplitWords import mainSplit


#Sinarthsh opou dhmiourgei ton py fakelo enos kainourgiou keimenou, dhladh kanei thn analish sta kainourgia keimena
def create_pyfile(text):    
    print("\ntext = ",text)

    if not os.path.exists(folder1 + textpos + text + '/py'):
        lines = []
        ylines = []

        #Ftiaxnw arxika ton fakelo 'py' opoy mesa tha exei olh thn plhroforia tou keimenoy
        os.makedirs(folder1 + textpos + text + '/py')
       

        #Ftiaxnw olous tous ipofakelous poy tha exei mesa toy o fakelos 'py'

        #Arxika tha exei mesa enan fakelo 'pages' opou tha exei mesa ena .txt arxeio me ton arithmo twn selidwn tou keimenou
        os.makedirs(folder1 + textpos + text + '/py/pages')
        pagestxt = folder1 + textpos + text + '/py/pages/pages.txt'
        pagesfile = open(pagestxt, 'w')
        pages = findPagesROIS(text)
        pagesfile.write(str(pages))
        pagesfile.close()
    

        # Ftiaxnw tous bohthikikous fakelous tou mytext
        os.makedirs(folder1 + textpos + text + '/py/mytext/firstlinewords')
        os.makedirs(folder1 + textpos + text + '/py/mytext/lastlinewords')

        for pageno in range(1, pages+1):
            os.makedirs(folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/linestarty')
            os.makedirs(folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/lineendy')
            os.makedirs(folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/ycorner')
            os.makedirs(folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/ygap')
            os.makedirs(folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/ROIstart')
            os.makedirs(folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/ROIend')
            os.makedirs(folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/letter_word_offset_bound')
            os.makedirs(folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/wordnumber')
     
            os.makedirs(folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/line/ROIstartx')
            os.makedirs(folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/line/ROIendx')
            os.makedirs(folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/line/ROIgapx')
            os.makedirs(folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/line/word')
            os.makedirs(folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/line/letter')


        #Epishs tha exei mesa enan fakelo 'ROIbounds' opou tha exei mesa .xlsx arxeia opou tha periexoun thn analish ROI twn selidwn tou keimenou
        print("%s ROI analysis begins..." %text)
        os.makedirs(folder1 + textpos + text + '/py/ROIbounds')
        for pageno in range(1, pages+1):
            rois = drawROI(text, pageno)     # into function drawROI is stored all ..../py/ROIbounds/.... files  &  ..../py/firstlinewords/.... files  &  ..../py/lastlinewords/.... files , see lines:215,217,218 into drawROI() function
            lines.append( rois[3] )
            ylines.append( rois[4] )
        print("%s ROI analysis is over..." %text)
        

        #Epishs tha exei mesa enan fakelo 'lines' opou tha exei mesa .xlsx arxeia opou tha periexoun ton arithmo twn grammwn kathe selidas tou keimenou
        os.makedirs(folder1 + textpos + text + '/py/lines')
        for pageno in range(1,pages+1):
            path = folder1 + textpos + text +'/py/lines/mytext.page(' + str(pageno) + ').lines.xlsx'
            workbook = xlsxwriter.Workbook(path)
            worksheet = workbook.add_worksheet()
            worksheet.write(0, 0, 'lines')
            worksheet.write(1, 0, lines[pageno-1])
            workbook.close()

    
        #Epishs tha exei mesa enan fakelo 'Yline' opou tha exei mesa .xlsx arxeia opou tha periexei thn plhroforia gia thn yline kathe grammis
        os.makedirs(folder1 + textpos + text + '/py/Yline')
        for pageno in range(1,pages+1):
            path = folder1 + textpos + text +'/py/Yline/mytext.page(' + str(pageno) + ').line.yline.xlsx'
            workbook = xlsxwriter.Workbook(path)
            worksheet = workbook.add_worksheet()
            worksheet.write(0, 0, 'yline')

            for lineno in range(1,lines[pageno-1]+1):
                worksheet.write(lineno, 0, ylines[pageno-1][lineno-1])
            
            workbook.close()
        
    else:
        print("Text %s has been analyzed" % text)


def findPagesROIS(text):
    pages = 1
    
    while(True):
        if( os.path.exists(folder1 + textpos + text + '/Slide' + str(pages) + '.PNG') ):
            pages += 1
        else:
            break
    
    return pages-1
        


def main(text):
    # text = str( sys.argv[1] )  #Take text information from command line as argument
    # text = "zoo_1920_hover"
    
    create_pyfile(text)

    list1 = ['zoo', 'morning', 'zebra', 'psaras', 'treno', 'sunny', 'sunnyloud', 'sunnyus']
    list2 = ['zoo_1920', 'morning_1920', 'zebra_1920', 'psaras_1920', 'treno_1920', 'sunny_1920', 'sunnyloud_1920', 'sunnyus_1920']

    list3 = ['visit', 'efeyreseis', 'olympia', 'island', 'doro', 'visitloud', 'midfred', 'armyjet', 'midfredloud', 'midfredus', 'armyjetus', 'midfredloudus', 'enemypie', 'gasmask', 'horse', 'jockey']
    list4 = ["testapartf_1920", "cbmparta_1920", "cbmpartb_1920", "cbmpartc_1920", 'visit_1920', 'efeyreseis_1920', 'olympia_1920', 'island_1920', 'doro_1920', 'visitloud_1920', 'midfred_1920', 'armyjet_1920', 'midfredloud_1920', 'midfredus_1920', 'armyjetus_1920', 'midfredloudus_1920', 'enemypie_1920', 'gasmask_1920', 'horse_1920', 'jockey_1920'] 

    hover_list_5 = []
    for x in list2:
        hover_list_5.append(x + "_hover")

    hover_list_6 = []
    for x in list4:
        hover_list_6.append(x + "_hover")


    if( text in list1  or text in list2 or text in hover_list_5):
        astr = '\leq 3' ; bstr = '4' ; cstr = '5' ; dstr = '\geq 6'


    if( text in list3 or text in list4 or text in hover_list_6):
        astr = '\leq 3' ; bstr = '4 and 5' ; cstr = '6 and 7' ; dstr = '\geq 8'
    
    
    mainSplit(text, astr, bstr, cstr, dstr)


# text = "cbmparta_1920"
# main(text)


def textloop():
    texts = ['testapartf_1920']
    for text in texts:
        main(text)

textloop()



    


