
import pandas as pd
from globalVars import folder1, dim, textpos
import cv2
# matplotlib.use('Agg')
from matplotlib import patches, pyplot as plt
import numpy as np
import time
from statistics import mean
import xlsxwriter
from os.path import exists
from decimal import Decimal, ROUND_HALF_UP


#Sinarthsh opou upologizei ta ROI bounds tou keimenou
def drawROI(text, pageno):

    if( exists(folder1 + textpos + text +'/py/ROIbounds/mytext.page_' + str(pageno) + '.ROIbounds.xlsx') ):
        print("ROI has calculated for text %s,  page %d\n" %(text, pageno))
        return
    
   
    f, ax = plt.subplots(1)
    f.set_figwidth(9)
    f.set_figheight(7)

    imagepath = folder1 + textpos + text + '/Slide' + str(pageno) + '.PNG'
    img = cv2.imread(imagepath,0)
    global numpydata
    numpydata = np.asarray(img)


    global firstlinewords, lastlinewords

    isvalid=False
    firstlinewords = []
    lastlinewords = []
    lines = 0
    yline = []
    wordnumberfirstlinewords = []
    wordnumberlastlinewords = []
    ycorner = []
    ROIstartpoint = []
    rowROIstart = []
    

    list1 = ['zoo', 'morning', 'zebra', 'psaras', 'treno', 'sunny', 'sunnyloud', 'sunnyus']
    list2 = ['zoo_1920', 'morning_1920', 'zebra_1920', 'psaras_1920', 'treno_1920', 'sunny_1920', 'sunnyloud_1920', 'sunnyus_1920']

    list3 = ['visit', 'efeyreseis', 'olympia', 'island', 'doro', 'visitloud', 'midfred', 'armyjet', 'midfredloud', 'midfredus', 'armyjetus', 'midfredloudus', 'enemypie', 'gasmask', 'horse', 'jockey']
    list4 = ['visit_1920', 'efeyreseis_1920', 'olympia_1920', 'island_1920', 'doro_1920', 'visitloud_1920', 'midfred_1920', 'armyjet_1920', 'midfredloud_1920', 'midfredus_1920', 'armyjetus_1920', 'midfredloudus_1920', 'enemypie_1920', 'gasmask_1920', 'horse_1920', 'jockey_1920'] 

    list5 = [ "cbmparta_1920", "cbmpartb_1920", "cbmpartc_1920", 'testapartf_1920' ]
    

    # minimum white space between words in texts, it depends from the text font
    global fixed_spaces
    if(text in list1 or text in list2 or text in list3 or text in list4):
        fixed_spaces = 24
    elif(text in list5):
        fixed_spaces = 8



    if(pageno == 1):
        wordscounter = 0
        
    else:
        path = folder1 + textpos + text + '/py/mytext/lastlinewords/lastlinewords(' + str(pageno-1) + ').xlsx'
        book = pd.read_excel(path)
        indexes = book.iloc[:,0].tolist()
        wordscounter = indexes[-1]


    #Find up and down limits in each line
    start = time.time()
    for y in range(len(numpydata)-10):
        if( mean(numpydata[y]) !=255 and isvalid==False ):
            isvalid=True                
            firstlinewords.append([dim[0]/2,y])     # Thelw na apothikefsw to teleutaio aspro giafto apothikeyw to shmeio y-1 kathws sto y exw to prwto mavro
            continue       
        
            #elegxw ean h epomenh grammi einai olh asprh etsi wste na kserw oti apo thn trexon grammi tha prokipsi to teleftaio shmeio ayths ths seiras
        if(  WhiteNext5Row(y,numpydata)==True and isvalid==True ):
            isvalid = False                   #Thetw isvalid=false wste na kserw oti tha psaxnw pali gia to prwto stoixeio ths epomenhw seiras
            lastlinewords.append([dim[0]/2,y])  # Thelw na apothikefsw to prwto aspro giafto apothikeyw to shmeio y+1 kathws sto y exw to teleftaio mavro
            lines += 1
            continue


    # # Draw up and down limits in each line
    # plt.imshow(img)
    # plt.axis('off')
    # for i in range(len(firstlinewords)):
    #        plt.scatter(firstlinewords[i][0], firstlinewords[i][1], 14, 'magenta')
    #        plt.scatter(lastlinewords[i][0], lastlinewords[i][1], 14, 'orange' )
    # plt.show()

    # end = time.time()
    # t1 = end - start
    # print("Time1 = ", t1) 



    # # # # Find Word Informations ( i.e word-start  and  word-end ) # # # #

    wordend = FindWordEnd()
    # plt.imshow(img)
    # plt.axis('off')
    # for i in range(len(wordend)):
    #         for j in range(len(wordend[i])):
    #             plt.scatter(wordend[i][j][0], wordend[i][j][1], 14, 'magenta')
    # plt.show()


    wordstart = FindWordStart()
    # plt.imshow(img)
    # plt.axis('off')
    # for i in range(len(wordstart)):
    #         for j in range(len(wordstart[i])):
    #             plt.scatter(wordstart[i][j][0], wordstart[i][j][1], 14, 'magenta')
    # plt.show()

    # # # # End of Find Word Informations # # # # 


    # # # offset for first words in each line # # # 
    offsetx = offsetxfirstwords(wordstart, wordend)
    # # # # # # # # # # # # # # # # # # # # # # # #


    #Find middle(line) in each line
    rows = len(firstlinewords)  

    for i in range(rows):
        x_start = wordstart[i][0][0]
        x_end = wordend[i][-1][0]
        
        y_up = firstlinewords[i][1]
        y_down = lastlinewords[i][1]

        yline.append( midLine(x_start, x_end, y_up, y_down) ) 


    #Find whiteSpaces between words
    whitespace = WhiteSpace(wordend)


    # Calculate ycorner

    ydifflist = []
    for i in range(len(firstlinewords)-1):
        ydifflist.append( - lastlinewords[i][1] + firstlinewords[i+1][1] )

    meanydiff = round(mean(ydifflist))
    ylineoffset = round(meanydiff/4)


    ycorner.append(firstlinewords[0][1] - round(meanydiff/2) - ylineoffset)
    for i in range(1, len(firstlinewords)):
        ycorner.append( firstlinewords[i][1] + round(lastlinewords[i-1][1] - firstlinewords[i][1])/2 )



    # Calculate and Store ygap
    ygap = StoreYgap(text, pageno, "ygap", ycorner, ydifflist)


    # FIND and DRAW ROI bounds between Words


    # # Find middle distance between two words
    # middistw = []    # middle space between words(only x indexes, because we don't need y, we only need x for declare width of rectangle)  
    # for i in range(rows):
    #     row=[]
    #     for j in range(len(wordend[i])-1):
    #         mid_x = wordend[i][j][0] + whitespace[i][j]/2
    #         row.append( mid_x )
            
    #     middistw.append(row)
    



    # alternative way to find middle distance between two words
    middistw = []
    for i in range(rows):
        row = []
        for j in range(len(wordend[i])-1):
            middist = (wordstart[i][j+1][0] - wordend[i][j][0])/2
            row.append( wordend[i][j][0] + middist)
        middistw.append(row)


    # Find word's width in rectangle
    width = []
    for i in range(rows):
        row=[]
        for j in range(len(middistw[i])+1):
            if(j==0 and middistw[i]!=[]): #Ean eimai sthn 1h lexi ths kathe grammis tote exw fixed arxh kai elegxw ean exw kai mono mia lexi sth grammi tote tha exw diaforetiko width kathws to middistw[i] tha einai keno ara den mporw na to xrhsimopoihsw
               w = middistw[i][j] - (wordstart[i][j][0]-offsetx[i])
               row.append(w)
            elif(j==0 and middistw[i]==[]):  #Ean exw mono mia lexi se kapoia grammi
                w = (wordend[i][j][0] + offsetx[i]) - (wordstart[i][j][0] - offsetx[i])   
                row.append(w)
            elif( j==len(middistw[i]) ):
                w = (wordend[i][j][0] + offsetx[i]) - middistw[i][j-1]
                row.append(w)
            elif(0 < j < len(middistw[i])):
                w = middistw[i][j] - middistw[i][j-1] 
                row.append(w)       
        
        width.append(row) 


    # Middle distance between two rows
    middistr = []
    rowspaces = []
    for i in range(rows-1):
        yup = lastlinewords[i][1]
        ydown = firstlinewords[i+1][1]
        rowspaces.append( (ydown-yup)/2 )
        middistr.append( yup + (ydown-yup)/2 )


    # Find wordnumberfirstlinewords, wordnumberlastlinewords, ROIstartpoint
    for row in range(len(wordend)):
        rowROIstart = []

        if(row==0):
            y = ycorner[0]
        else:
            y = middistr[row-1]

        for i in range(len(wordend[row])):
            wordscounter += 1    

            if(i==0):    #Ean eimai sthn 1h lexi kathe grammis
                x = wordstart[row][i][0] - offsetx[row]
            elif( middistw[row]==[] ): # eimai se grammi me mia mono leksi ara den exw middle distance between words
                x = wordstart[row][0][0] - offsetx[row]
            else:
                x = middistw[row][i-1]

            rowROIstart.append( [x,y] )

        wordnumberfirstlinewords.append(wordscounter-len(wordend[row])+1)   # list for firstlinewords
        wordnumberlastlinewords.append(wordscounter)   # list for lastlinewords
        ROIstartpoint.append( rowROIstart )  


    # Store firstlinewords, lastlinewords, ycorner
    StoreLineWords(text, pageno, "firstlinewords", wordnumberfirstlinewords)
    StoreLineWords(text, pageno, "lastlinewords", wordnumberlastlinewords)
    StoreLineWords(text, pageno, "ycorner", ycorner)
    
    # Store linestarty, lineendy
    StoreLineEdges(text, pageno, "linestarty", firstlinewords)
    StoreLineEdges(text, pageno, "lineendy", lastlinewords)

    #  Store ROIstart, ROIend
    ROIstart = StoreROIstartend(text, pageno, "ROIstart", wordnumberfirstlinewords, [], [], offsetx)
    ROIend = StoreROIstartend(text, pageno, "ROIend", wordnumberlastlinewords, [], [], offsetx)
    wordnumberpage = StorePageWordnumber(text, pageno, "wordnumber", ROIstart, ROIend)

    #  Store ROIstartx, ROIendx
    ROIstartx = StoreROIstartend(text, pageno, "ROIstartx", ROIstartpoint, [], [], offsetx)
    ROIendx = StoreROIstartend(text, pageno, "ROIendx", ROIstartpoint, wordend, width, offsetx)

    # Store ROIgapx
    StoreROIstartend(text, pageno, "ROIgapx", ROIstartx, ROIendx, width, offsetx)


    
    # # fix width[-1] per line
    # for i in range(len(width)):
    #     width[i][-1] = ROIendx[i][-1] + offsetx - ROIstartx[i][-1]


    # Draw Rectangle
    final_x = []
    final_y = []
    final_width = []
    final_height = []
    
    for row in range(len(wordend)):
        rowROIstart = []

        if(row==0):
            y = ycorner[0]
        else:
            y = middistr[row-1]
        

        for i in range(len(wordend[row])):
            wordscounter += 1    

            if(i==0):    #Ean eimai sthn 1h lexi kathe grammis
                x = wordstart[row][i][0] - offsetx[row]
            elif(i!=0):
                x = middistw[row][i-1]
         
            final_x.append(x)
            final_y.append(y)
            final_width.append(width[row][i])
            final_height.append(ygap[row])

            
            rect = patches.Rectangle((x,y), width[row][i], ygap[row], edgecolor='r', facecolor="none")
            ax.add_patch(rect)

    
    # Store ROIbounds
    StoreRois(text, pageno, final_x, final_y , final_width, final_height)


    img = plt.imread(imagepath)
    plt.imshow(img)
    plt.axis('off')

    
    plt.savefig(folder1+ textpos + text + '/Slidegraph' + str(pageno) + 'py.jpg')
    # plt.show()
    plt.close('all')

    return firstlinewords , lastlinewords, wordend, lines, yline, wordnumberfirstlinewords, wordnumberlastlinewords




def offsetxfirstwords(wordstart, wordend):
    offsetx = []
    multiplier = 4
    for row in range(len(wordstart)):
        xdiff = []
        if( len(wordstart[row])==1 ): # ean exw mono mia leksi se kapoia grammi
            offsetx.append(np.mean(offsetx))

        else:
            for i in range(len(wordstart[row])-1):
                xdiff.append( wordstart[row][i+1][0] - wordend[row][i][0])
            offsetx.append(multiplier * np.mean(xdiff))
    
    return offsetx



#Sinarthsh opou elegxei ean eimai sto telos mias grammis, elegxontas ean oi epomenes 2 grammes exoun mono aspra shmeia
def WhiteNext5Row(y,numpydata):
    for i in range(1,6):
        if( mean(numpydata[y+i])!=255 ):
            return False
    
    return True


#Sinarthsh opou briskei kai epistrefei to telos kathe leksis
def FindWordEnd():
    wordend = []
    row = []

    black = False

    for i in range(len(firstlinewords)):
        row = []
        
        for x in range(len(numpydata[0])-25):
            tempx = x
            sumword = 0
           
            for y in range(firstlinewords[i][1],lastlinewords[i][1]+1):  
                sumword = 0

                if(numpydata[y][tempx]==255):
                    black = False

                if(numpydata[y][tempx]!=255):
                    black = True

                while( numpydata[y][tempx+1]==255 and black==True and tempx<len(numpydata[0])-25 ):
                    sumword += 1
                    tempx += 1

                if(sumword>=48 and black==True and WhiteLeastsomeColumn(x+1, firstlinewords[i][1], lastlinewords[i][1])==True ):   # this is if i am at the end of the row, so the sum between the last word(black point) till the end is >=48
                    black=False
                    # plt.scatter(x, y, 14, 'green')
                    row.append( [x+1, y] )    # Thelw na apothikefsw to prwto aspro meta apo to teleftaio mavro, giafto apothikevw to x+1, alliws an ithela to teleftaiuo mavro tha apothikeva to x
                    break
                     

                elif(sumword>=fixed_spaces and black==True and WhiteLeastsomeColumn(x+1, firstlinewords[i][1], lastlinewords[i][1])==True ):    # this is if i am NOT at the end of the row, so the sum between words is >=24
                    black=False
                    # plt.scatter(x, y, 14, 'green')
                    row.append( [x+1, y] )   # Thelw na apothikefsw to prwto aspro meta apo to teleftaio mavro, giafto apothikevw to x+1, alliws an ithela to teleftaiuo mavro tha apothikeva to x
                    break


        wordend.append(row)
    
    return wordend



#Sinarthsh opou briskei kai epistrefei to telos kathe leksis
def FindWordStart():
    wordstart = []
    row = []

    black = False

    for i in range(len(firstlinewords)):
        row = []
        
        for x in range(len(numpydata[0])-25):
            tempx = x
            sumword = 0
           
            for y in range(firstlinewords[i][1],lastlinewords[i][1]+1):  
                sumword = 0

                if(numpydata[y][tempx]==255):
                    black = False

                if(numpydata[y][tempx]!=255):
                    black = True

                while( numpydata[y][tempx-1]==255 and black==True and tempx<len(numpydata[0])-25 ):
                    sumword += 1
                    tempx -= 1

                if(sumword>=48 and black==True and WhiteLeastsomeColumn(x-fixed_spaces, firstlinewords[i][1], lastlinewords[i][1])==True ):   # this is if i am at the start of the row, so the sum between the last word(black point) till the end is >=48
                    black=False
                    # plt.scatter(x, y, 14, 'green')
                    row.append( [x+1, y] )    # Thelw na apothikefsw to prwto aspro meta apo to teleftaio mavro, giafto apothikevw to x+1, alliws an ithela to teleftaiuo mavro tha apothikeva to x
                    break
                     

                elif(sumword>=fixed_spaces and black==True and WhiteLeastsomeColumn(x-fixed_spaces, firstlinewords[i][1], lastlinewords[i][1])==True ):    # this is if i am NOT at the end of the row, so the sum between words is >=24
                    black=False
                    # plt.scatter(x, y, 14, 'green')
                    row.append( [x+1, y] )   # Thelw na apothikefsw to prwto aspro meta apo to teleftaio mavro, giafto apothikevw to x+1, alliws an ithela to teleftaiuo mavro tha apothikeva to x
                    break


        wordstart.append(row)
    
    return wordstart

            


#                                             (x,yup)     _ _ _ _  (x+24,yup)
#Boithitiki sunarthsh opou elegxei katheta    (x,ydown)  |_|_|_|_|  (x+24,ydown)  ean oi epomenes 24 sthles exoun mono aspra shmeia(to xrhsimopoiw sthn parapanw sinartisi gia na brw to telos kathe leksis )
def WhiteLeastsomeColumn(x, yup, ydown):
    for i in range(fixed_spaces):
        for y in range(yup,ydown+1):
            if(numpydata[y][x+i] != 255):
                return False
    
    return True

        


# Find middle of a line (yline)
def midLine(xstart, xend, yup, ydown):
    midy = yup + (ydown-yup)/2

    x =[xstart, xend]
    y=[midy, midy]
    plt.plot(x, y ,linewidth=1.5)

    return midy


#Sinarthsh opou ipologizei tis aspres sthles apo mia leksi se mia allh, prokeimenou na brw pou tha xwrisw duo lekseis
def SumWhiteColumn(i, j, wordend, yup, ydown):
    space = 0
    for x in range( wordend[i][j][0]+1, wordend[i][j+1][0] ):
        for y in range(yup, ydown+1):
            if(numpydata[y][x] != 255):
                return space
        space+=1
    
    return space


#Sinarthsh opou epistrefei mia lista me stoixeia listes, opou oi eswterikes listes periexoun ta kena diasthmata apo leksi se leksi ana grammi
def WhiteSpace(wordend):
    whitespaces = []
    for i in range(len(wordend)):
        whitelistperrow=[]
        for j in range(len(wordend[i])-1):
            whitelistperrow.append(SumWhiteColumn(i, j, wordend, firstlinewords[i][1], lastlinewords[i][1]))
        
        whitespaces.append(whitelistperrow)
    
    return whitespaces


#Save calculated ROIS
def StoreRois(text, pageno, x, y , width, height):
    path = folder1 + textpos + text +'/py/ROIbounds/mytext.page_' + str(pageno) + '.ROIbounds.xlsx'
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    
    # Start from the first cell.
    # Rows and columns are zero indexed.
    row = 0
    column1 = 0
    column2 = 1
    column3 = 2
    column4 = 3
    

    worksheet.write(row, column1, 'X')
    worksheet.write(row, column2, 'Y')
    worksheet.write(row, column3, 'WIDTH')
    worksheet.write(row, column4, 'HEIGHT')
    row+=1

    for i in range(len(x)) :
        worksheet.write(row, column1, Decimal(x[i]).quantize(0, ROUND_HALF_UP))
        worksheet.write(row, column2, Decimal(y[i]).quantize(0, ROUND_HALF_UP))
        worksheet.write(row, column3, Decimal(width[i]).quantize(0, ROUND_HALF_UP))
        worksheet.write(row, column4, Decimal(height[i]).quantize(0, ROUND_HALF_UP))
        
        row += 1
        
    workbook.close()


def StoreLineWords(text, pageno, paramname, list):
    if(paramname == "ycorner"):
        path = folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/' + paramname + '/' + paramname + '.xlsx'
    else:
        path = folder1 + textpos + text + '/py/mytext/' + paramname + '/' + paramname + '(' + str(pageno) + ').xlsx'
    
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()

    worksheet.write_column(0,0,list)

    workbook.close()


def StoreLineEdges(text, pageno, paramname, list):
    path = folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/' + paramname + '/' + paramname + '.xlsx'
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()

    for i in range(len(list)):
        worksheet.write(i, 0, list[i][1])   
    
    workbook.close()


# find mid-distance among lines and form y of corner any gap of y
def StoreYgap(text, pageno, paramname, ycorner, ydifflist):
    path = folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/' + paramname + '/' + paramname + '.xlsx'
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet() 

    ygap = [i+1 for i in np.diff(ycorner).tolist()]

    meanydiff = round(mean(ydifflist))
    ylineoffset = round(meanydiff/4)

    ygap.append( round(mean(ygap)) + ylineoffset )

    worksheet.write_column(0, 0, ygap)
    
    workbook.close()

    return ygap


def StoreROIstartend(text, pageno, paramname, list1, list2, width, offsetx):
    if( paramname == "ROIstart" ):
        path1 = folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/' + paramname + '/' + paramname + '.xlsx'
        workbook1 = xlsxwriter.Workbook(path1)
        worksheet1 = workbook1.add_worksheet() 
        worksheet1.write(0, 0, list1[0])
        workbook1.close()
        return  list1[0]
    
    
    elif( paramname == "ROIend" ):
        path1 = folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/' + paramname + '/' + paramname + '.xlsx'
        workbook1 = xlsxwriter.Workbook(path1)
        worksheet1 = workbook1.add_worksheet() 
        worksheet1.write(0, 0, list1[-1])
        workbook1.close()
        return list1[-1]

    
    elif( paramname == "ROIstartx" ):
        ROIstartx = []
        path2 = folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/line/' + paramname + '/' + paramname + '.xlsx'
        workbook2 = xlsxwriter.Workbook(path2)
        worksheet2 = workbook2.add_worksheet()
        for i in range(len(list1)):
            rowROIstartx = []
            for j in range(len(list1[i])):
                worksheet2.write(j, i, list1[i][j][0])
                rowROIstartx.append(list1[i][j][0])
            
            ROIstartx.append(rowROIstartx)
            worksheet2.write_column(0, i, rowROIstartx)

        workbook2.close()
        return ROIstartx
    
    
    elif( paramname == "ROIendx" ):
        ROIendx = []
        wordend = list2
        path2 = folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/line/' + paramname + '/' + paramname + '.xlsx'
        workbook2 = xlsxwriter.Workbook(path2)
        worksheet2 = workbook2.add_worksheet()

        for i in range(len(list1)):
            rowROIendx = []
            for j in range(len(list1[i])):        
                rowROIendx.append(list1[i][j][0] + width[i][j])
            
            rowROIendx[-1] = wordend[i][-1][0] + offsetx[i]
            ROIendx.append(rowROIendx)
            worksheet2.write_column(0, i, rowROIendx)
        
        workbook2.close()
        return ROIendx


    elif( paramname == "ROIgapx" ):
        path2 = folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/line/' + paramname + '/' + paramname + '.xlsx'
        workbook2 = xlsxwriter.Workbook(path2)
        worksheet2 = workbook2.add_worksheet()

        for i in range(len(width)):
            roistartxdiff = [j-i for i, j in zip(list1[i][:-1], list1[i][1:])]
            roistartxdiff.append( list2[i][-1] + offsetx[i] - list1[i][-1] )
            worksheet2.write_column(0, i, roistartxdiff) 
        workbook2.close()
        


def StorePageWordnumber(text, pageno, paramname, ROIstart, ROIend):
    path1 = folder1 + textpos + text + '/py/mytext/page(' + str(pageno) + ')/' + paramname + '/' + paramname + '.xlsx'
    workbook = xlsxwriter.Workbook(path1)
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, paramname) 
    worksheet.write(1, 0, str(ROIend-ROIstart+1) ) 

    workbook.close()



