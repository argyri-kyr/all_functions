import xlsxwriter

import os,sys,inspect
from SplitWords import mainSplit
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,currentdir)

from globalVars import folder1, textpos
from ROIcalculation import drawROI
from SplitWords import mainSplit
from findroiperline import findroiperline

#Sinarthsh opou dhmiourgei ton py fakelo enos kainourgiou keimenou, dhladh kanei thn analish sta kainourgia keimena
def create_pyfile(text):    
    print("text = ",text)

    if not os.path.exists(folder1 + textpos + text + '/py'):
        lines = []
        ylines = []

        #Ftiaxnw arxika ton fakelo 'py' opoy mesa tha exei olh thn plhroforia tou keimenoy
        os.makedirs(folder1 + textpos + text + '/py')
       

        # Ftiaxnw olous tous ipofakelous poy tha exei mesa toy o fakelos 'py'

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
            lines.append( rois[4] )
            ylines.append( rois[5] )
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
        
        # Telos ftiaxnw thn antistoixia twn ROI me tis grammes, dhladh kathe rois se poia grammi anhkei
        for pageno in range(1,pages+1):
            findroiperline(text, pageno)
        
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
    list2 = ['testapartav2part2_1920', 'decodepseudowords2v_1920', 'decoderealwords2v_1920', 'phonolrhymes_1920', 'raven_1920', 'zoo_1920', 'morning_1920', 'zebra_1920', 'psaras_1920', 'treno_1920', 'sunny_1920', 'sunnyloud_1920', 'sunnyus_1920']

    list3 = ['visitloudext', 'visitloudthree','visit', 'efeyreseis', 'olympia', 'island', 'doro', 'visitloud', 'midfred', 'armyjet', 'midfredloud', 'midfredus', 'armyjetus', 'midfredloudus', 'enemypie', 'gasmask', 'horse', 'jockey']
    list4 = ['RAN_1920','visitloudext_1920', 'visitloudthree_1920','testapartc_1920', 'visit_1920', 'efeyreseis_1920', 'olympia_1920', 'island_1920', 'doro_1920', 'visitloud_1920', 'midfred_1920', 'armyjet_1920', 'midfredloud_1920', 'midfredus_1920', 'armyjetus_1920', 'midfredloudus_1920', 'enemypie_1920', 'gasmask_1920', 'horse_1920', 'jockey_1920'] 
    
    list5 = ['testattention_1920', 'testaparta_1920', 'testaparta1_1920', 'testaparta2_1920', 'testapartb_1920', 'testapartb1_1920', 'testapartb2_1920', 'testapartc_1920', 'testapartd_1920', 'testapartd1_1920' , 'testapartd2_1920', 'testaparte_1920', 'testaparte1_1920']
    list6 = ['testaparte2_1920', 'testapartf_1920', 'testapartf1_1920', 'testapartf2_1920', 'testapartf3_1920', 'testapartfp1_1920', 'testapartfp2_1920', 'testapartfp3_1920']
    
    hover_list_5 = []
    for x in list2:
        hover_list_5.append(x + "_hover")

    hover_list_6 = []
    for x in list4:
        hover_list_6.append(x + "_hover")


    if( (text in list1)  or (text in list2) or (text in list6) or (text in hover_list_5) ):
        astr = '\leq 3' ; bstr = '4' ; cstr = '5' ; dstr = '\geq 6'


    if( (text in list3) or (text in list4) or (text in list5) or (text in hover_list_6) ):
        astr = '\leq 3' ; bstr = '4 and 5' ; cstr = '6 and 7' ; dstr = '\geq 8'
    
    
    mainSplit(text, astr, bstr, cstr, dstr)


# texts = ['testaparte2_1920', 'testapartf_1920', 'testapartf1_1920', 'testapartf2_1920', 'testapartf3_1920', 'testapartfp1_1920', 'testapartfp2_1920', 'testapartfp3_1920']
# texts = ['RAN_1920']
texts = ["testapartav2part2_1920"]
for text in texts:
    main(text)



    


