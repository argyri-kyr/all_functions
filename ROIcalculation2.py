
import pandas as pd
from globalVars import folder1, fixed_nullspace
import cv2
from matplotlib import patches, pyplot as plt
import numpy as np
import time
from statistics import mean
import xlsxwriter
from os.path import exists


#Sinarthsh opou upologizei ta ROI bounds tou keimenou
def drawROI(text, pageno):

    if( exists(folder1 + 'texts/' + text +'/py/ROIbounds/mytext.page_' + str(pageno) + '.ROIbounds.xlsx') ):
        print("ROI has calculated for text %s,  page %d\n" %(text, pageno))
        return
    

    f, ax = plt.subplots(1)
    f.set_figwidth(9)
    f.set_figheight(7)

    imagepath = folder1 + 'texts/'+ text + '/Slide' + str(pageno) + '.PNG'
    img = cv2.imread(imagepath,0)
    global numpydata
    numpydata = np.asarray(img)
    
    # plt.imshow(img)
    # plt.axis('off')
    # plt.show()   

    greektexts = ['visit', 'zoo', 'zebra', 'psaras', 'efeyreseis', 'island', 'morning', 'olympia']

    global firstlinewords, lastlinewords

    isvalid=False
    firstlinewords = []
    lastlinewords = []
    lines = 0
    yline = []
    ycorner = []
    rowROIstart = []
    

    if(pageno == 1):
        wordscounter = 0
        
    else:
        path = folder1 + 'texts/' + text + '/py/mytext/lastlinewords/lastlinewords(' + str(pageno-1) + ').xlsx'
        book = pd.read_excel(path)
        indexes = book.iloc[:,0].tolist()
        wordscounter = indexes[-1]



    #Find up and down limits in each line
    start = time.time()
    for y in range(len(numpydata)-3):
        if( mean(numpydata[y]) !=255 and isvalid==False ):
            isvalid=True                
            firstlinewords.append([1366/2,y-1])     # Thelw na apothikefsw to teleutaio aspro giafto apothikeyw to shmeio y-1 kathws sto y exw to prwto mavro
            continue       
        
            #elegxw ean h epomenh grammi einai olh asprh etsi wste na kserw oti apo thn trexon grammi tha prokipsi to teleftaio shmeio ayths ths seiras
        if(  WhiteNext2Row(y+1,numpydata)==True and isvalid==True ):
            isvalid = False                   #Thetw isvalid=false wste na kserw oti tha psaxnw pali gia to prwto stoixeio ths epomenhw seiras
            lastlinewords.append([1366/2,y+1])  # Thelw na apothikefsw to prwto aspro giafto apothikeyw to shmeio y+1 kathws sto y exw to teleftaio mavro
            lines += 1
            continue

    end = time.time()
    t1 = end - start
    # print("Time1 = ", t1)


    # #Draw up and down limits in each line

    # for i in range(len(firstlinewords)):
    #        plt.scatter(firstlinewords[i][0], firstlinewords[i][1], 14, 'magenta')
    #        plt.scatter(lastlinewords[i][0], lastlinewords[i][1], 14, 'orange' )
    

    
    
    #Find (and Plot(if i want)) end of Words
    start = time.time()

    wordend = FindWordEnd()
    letterend = FindLetterEnd()
    letterstart = FindLetterStart()
    letterstartx, letterendx = SplitConnectedLetters(letterstart, letterend)

    end = time.time()
    t2 = end - start
    # print("Time2 = ",t2)


    #Find and Drow middle(line) in each line
    start = time.time()
    rows = len(firstlinewords)  

    for i in range(rows):
        x_start = 125
        x_end = wordend[i][-1][0]
        y_up = firstlinewords[i][1]
        y_down = lastlinewords[i][1]

        yline.append( midLine(x_start, x_end, y_up, y_down) ) 

    # # draw letter starts
    # for i in range(len(letterstartx)):
    #     for j in range(len(letterstartx[i])):
    #         plt.plot(letterstartx[i][j], yline[i], 'ro', markersize=2)
    #     for j in range(len(letterstart[i])):
    #         plt.plot(letterstart[i][j][0], letterstart[i][j][1],'ro', markersize=2 )
    #     for j in range(len(letterstart[i])):
    #         plt.plot(letterend[i][j][0], letterend[i][j][1],'bo', markersize=2 )

    # # draw letter ends
    # for i in range(len(letterendx)):
    #     for j in range(len(letterendx[i])):
    #         plt.plot(letterendx[i][j], yline[i], 'bo', markersize=2)



    end = time.time()
    t3 = end - start
    # print("Time3 = ",t3)

    #Find whiteSpaces between words
    whitespace = WhiteSpace(wordend)


    # Calculate ycorner

    ydifflist = []

    for i in range(len(firstlinewords)-1):
        ydifflist.append( - lastlinewords[i][1] + firstlinewords[i+1][1] )

    meanydiff = round(mean(ydifflist))
    ylineoffset = round(meanydiff/4)

    x = firstlinewords[0][1]
    ycorner.append(firstlinewords[0][1] - round(meanydiff/2)-ylineoffset)
    for i in range(1, len(firstlinewords)):
        ycorner.append( firstlinewords[i][1] + round(lastlinewords[i-1][1] - firstlinewords[i][1])/2 )


    # Calculate and Store  fixed_x, fixed_y, xdiff, offsetx, wordnumber, trueletter
    xdiff, wordnumber ,trueletter, letterstartx = StoreLetterInfo(text, pageno, letterstartx, letterendx, firstlinewords, lastlinewords)

    # Store meanletter, meanworddist, offsetx, wordbound
    offsetx, wordbound = Letterdist_Worddist_Offsetx_WordBound(text, pageno, xdiff)

    # Store word struct
    wordstartx = StoreWordInfo(text, pageno, firstlinewords, lastlinewords, letterstartx, letterendx, xdiff, wordnumber, trueletter)


    ROIstartx_0 =  letterstartx[0][0] - offsetx 
    
    fixed_x = ROIstartx_0
    fixed_y = ycorner[0]


    # Smirnakis data
    ROIstartx, ROIendx = FindROIstartxendx(letterendx, xdiff, wordbound, offsetx, wordend)
    # StoreROIstartend(text, pageno, "ROIstartx", wordstartx, [], [], offsetx)
    



    # Calculate and Store ygap
    ygap = StoreYgap(text, pageno, "ygap", ycorner, ydifflist)


    #Some fixed points in texts
    if(text in greektexts):
        # fixed_x = 97  
        # fixed_y = 29
        right_margin = 40
        down_margin = 60
    else:
        # fixed_x = 92
        # fixed_y = 30
        right_margin = 60
        down_margin = 60


    # FIND and DRAW ROI bounds between Words


    # Find middle distance between two words
    middistw = []    # middle space between words(only x indexes, because we don't need y, we only need x for declare width of rectangle)  
    for i in range(rows):
        row=[]
        for j in range(len(wordend[i])-1):
            mid_x = wordend[i][j][0] + whitespace[i][j]/2
            row.append( mid_x )
            
        middistw.append(row)

    # Find word's width in rectangle
    width = []
    for i in range(rows):
        row=[]
        for j in range(len(middistw[i])+1):
            if(j==0 and middistw[i]!=[]): #Ean eimai sthn 1h lexi ths kathe grammis tote exw fixed arxh kai elegxw ean exw kai mono mia lexi sth grammi tote tha exw diaforetiko width kathws to middistw[i] tha einai keno ara den mporw na to xrhsimopoihsw
               w = middistw[i][j] - fixed_x 
               row.append(w)
            elif(j==0 and middistw[i]==[]):  #Ean exw mono mia lexi se kapoia grammi
                w = (wordend[i][j][0] - fixed_x) + right_margin 
                row.append(w)
            elif( j==len(middistw[i]) ):
                w = (wordend[i][j][0] - middistw[i][j-1]) + right_margin 
                row.append(w)
            elif(0 < j < len(middistw[i])):
                w = middistw[i][j] - middistw[i][j-1] 
                row.append(w)       
        
        width.append(row) 


    # Middle distance between two rows
    middistr = []
    for i in range(rows-1):
        yup = lastlinewords[i][1]
        ydown = firstlinewords[i+1][1]
        middistr.append( yup + (ydown-yup)/2 )
    

    # Draw Rectangle
    final_x = []
    final_y = []
    final_width = []
    final_height = []
    
    for row in range(len(wordend)):
        rowROIstart = []

        if(row==0):
            y = fixed_y
        else:
            y = middistr[row-1]
        

        for i in range(len(wordend[row])):
            wordscounter += 1    

            if(i==0):    #Ean eimai sthn 1h lexi kathe grammis
                x = fixed_x
            elif(i!=0):
                x = middistw[row][i-1]
         
            final_x.append(x)
            final_y.append(y)
            final_width.append(width[row][i])
            final_height.append(ygap[row])

            
            rect = patches.Rectangle((x,y), width[row][i], ygap[row], edgecolor='r', facecolor="none")
            ax.add_patch(rect)
            rowROIstart.append( [x,y] ) 



    # Store ROIbounds
    StoreRois(text, pageno, final_x, final_y , final_width, final_height)

    # Store firstlinewords, lastlinewords, ycorner
    StoreLineWords(text, pageno, "firstlinewords" )
    StoreLineWords(text, pageno, "lastlinewords")
    StoreLineWords(text, pageno, "ycorner", ycorner)
    
    # Store linestarty, lineendy
    StoreLineEdges(text, pageno, "linestarty", firstlinewords)
    StoreLineEdges(text, pageno, "lineendy", lastlinewords)



    # Store ROIstart, ROIend
    StoreROIstartend(text, pageno, "ROIstart", [], [], offsetx)
    StoreROIstartend(text, pageno, "ROIend", [], [], offsetx)

    # Store ROIstartx, ROIendx
    ROIendx = StoreROIstartend(text, pageno, "ROIendx", wordend, width, offsetx)

    # Store ROIgapx
    StoreROIstartend(text, pageno, "ROIgapx", ROIstartx, ROIendx, width, offsetx)


    img = plt.imread(imagepath)
    plt.imshow(img)
    plt.axis('off')

    
    plt.savefig(folder1+ '/texts/' + text + '/Slidegraph' + str(pageno) + 'py.jpg')
    # plt.show()

    return firstlinewords , lastlinewords, wordend, t1, lines, yline



#Sinarthsh opou elegxei ean eimai sto telos mias grammis, elegxontas ean oi epomenes 2 grammes exoun mono aspra shmeia
def WhiteNext2Row(y,numpydata):
    if( mean(numpydata[y])==255 and mean(numpydata[y+1])==255):
        return True
    
    return False


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
           
            for y in range(firstlinewords[i][1], lastlinewords[i][1]+1):  
                sumword = 0

                if(numpydata[y][tempx]==255):
                    black = False

                if(numpydata[y][tempx]!=255):
                    black = True

                while( numpydata[y][tempx+1]==255 and black==True and tempx<len(numpydata[0])-25 ):
                    sumword += 1
                    tempx += 1

                if(sumword>=48 and black==True and WhiteLeast24Column(x+1, firstlinewords[i][1], lastlinewords[i][1])==True ):   # this is if i am at the end of the row, so the sum between the last word(black point) till the end is >=48
                    black=False
                    # plt.scatter(x, y, 14, 'green')
                    row.append( [x+1, y] )    # Thelw na apothikefsw to prwto aspro meta apo to teleftaio mavro, giafto apothikevw to x+1, alliws an ithela to teleftaiuo mavro tha apothikeva to x
                    break
                     

                elif(sumword>=24 and black==True and WhiteLeast24Column(x+1, firstlinewords[i][1], lastlinewords[i][1])==True ):    # this is if i am NOT at the end of the row, so the sum between words is >=24
                    black=False
                    # plt.scatter(x, y, 14, 'green')
                    row.append( [x+1, y] )   # Thelw na apothikefsw to prwto aspro meta apo to teleftaio mavro, giafto apothikevw to x+1, alliws an ithela to teleftaiuo mavro tha apothikeva to x
                    break


        wordend.append(row)
    
    return wordend



#Sinarthsh opou briskei kai epistrefei thn arxh kathe leksis
def FindWordStart(letterstartx, letternumber):
    wordstart = []
    rowwordstart = []
    count = 0
    index = 0

    for i in range(len(letterstartx)):
        count = 0
        index = 0
        rowwordstart = []
        for j in range(len(letterstartx[i])):
            if(count == 0):
                rowwordstart.append(letterstartx[i][j])
                count += 1
            
            elif(count==letternumber[i][index]):
                count = 0
                index += 1
            
            else:
                count += 1
            
        wordstart.append(rowwordstart)

    return wordstart


def FindLetterEnd():
    letterend = []
    row = []

    black = False

    for i in range(len(firstlinewords)):
        black = False
        row = []

        for x in range(len(numpydata[0])-25):
            for y in range(firstlinewords[i][1],lastlinewords[i][1]+1):  
                if(numpydata[y][x]!=255):
                    tempy = y
                    black = True
                    break
            
            if( black==True ):
                if( Meanlinecontr(x, firstlinewords[i][1], lastlinewords[i][1]+1)==True  and  Meanlinecontr(x-1, firstlinewords[i][1], lastlinewords[i][1]+1)==False ):
                    black = False
                    row.append( [x ,tempy] ) 
        
        letterend.append( row )
    
    return letterend
                

def FindLetterStart():
    letterstart = []
    row = []

    black = False

    for i in range(len(firstlinewords)):
        black = False
        row = []

        for x in range(len(numpydata[0])-25):
            for y in range(firstlinewords[i][1],lastlinewords[i][1]+1):  
                if(numpydata[y][x]!=255):
                    black = True
                    break

            if( black==True ):
                black = False
                if( Meanlinecontr(x-1, firstlinewords[i][1], lastlinewords[i][1]+1)==True  and  Meanlinecontr(x, firstlinewords[i][1], lastlinewords[i][1]+1)==False ):
                    if( len(row) == 0 ):
                        row.append( [x-1, y] )     # Thelw na apothikefsw to teleftaio aspro prin to prwto mavro, giafto apothikevw to x-1, alliws an ithela to prwto mavro tha apothikeva to x
                    elif( len(row) > 0 ):
                        if( abs( row[-1][0] - x ) > 7 ):
                            row.append( [x-1, y] )     

                        if( abs( row[-1][0] - x ) <= 7 ):
                            del row[-1]
                            row.append( [x-1, y] )
        
        letterstart.append( row )
    
    return letterstart


def SplitConnectedLetters(letterstart, letterend):
    lettersize = []
    letterstartx = []
    letterendx = []
    logic2 = []
    meanlettersizelist = []

    # make letterstartx
    for i in range(len(letterstart)):
        row = []
        for j in range(len(letterstart[i])):
            row.append(letterstart[i][j][0])
        letterstartx.append(row)

    # make letterendx
    for i in range(len(letterend)):
        row = []
        for j in range(len(letterend[i])):
            row.append(letterend[i][j][0])
        letterendx.append(row)


    # start split process
    for i in range(len(letterstartx)):
        rowlettersize = []
        rowlogic = []
        for j in range(len(letterstartx[i])):
            rowlettersize.append( letterendx[i][j] - letterstartx[i][j] )
        
        lettersize.append(rowlettersize)
        meanlettersize = mean(lettersize[i])
        rowlogic = [ lettersize[i][j] > round(1.5*meanlettersize) for j in range(len(letterstartx[i])) ]
        logic2.append(rowlogic)
        meanlettersizelist.append(meanlettersize)
    
    
    count = 0
    for i in range(len(letterstartx)):
        count = 0
        missingletters = []
        for letterno in range(len(logic2[i])):
            if(logic2[i][letterno]):

                # while(logic2[i][letterno] > round(1.5*meanlettersizelist[i]) ):
                #     missingletters.append( letterstartx[i][letterno+count]+round(lettersize[i][letterno]/2))
                #     logic2[i][letterno] = logic2[i][letterno]+round(lettersize[i][letterno]/2)

                letterstartx[i] = letterstartx[i][:letterno+count+1] + [ letterstartx[i][letterno+count]+round(lettersize[i][letterno]/2) ] + letterstartx[i][letterno+count+1:]
                letterendx[i] = letterendx[i][:letterno+count] + [ letterendx[i][letterno+count]-round(lettersize[i][letterno]/2) ] + letterendx[i][letterno+count:]
                count = count + 1

    return letterstartx, letterendx



def FindROIstartxendx(letterendx, xdiff, wordbound, offsetx, wordend):
    ROIstartx = []
    ROIendx = []
    logic = []
    difflogic = []

    for i in range(len(xdiff)):
        rowlogic = [ xdiff[i][j] > wordbound for j in range(len(xdiff[i]))] 
        logic.append(rowlogic)
        
    logic.append([False])

    for i in range(len(logic)):
        rowdifflogic = []
        for j in range(len(logic[i])):
            if( logic[i][j] ):
                rowdifflogic.append(xdiff[i][j])
        difflogic.append(rowdifflogic)


    for i in range(len(difflogic)):
        rowROIstartx = []
        for j in range(len(difflogic[i])):
            if(logic[i]):
                rowROIstartx.append(letterendx[i][j] + np.ceil(0.5*difflogic[i][j]) - 1) 
        
        ROIstartx.append(rowROIstartx)


    for i in range(len(wordend)):
        rowROIendx= []
        for j in range(len(wordend[i])):
            rowROIendx.append(wordend[i][j][0] + np.ceil(0.5*difflogic[i][j]))
        
        rowROIendx.append(wordend[i][-1][0] + offsetx)
        
        ROIendx.append(rowROIendx)
    
    return ROIstartx, ROIendx
    

#                                             (x,yup)     _ _ _ _  (x+24,yup)
#Boithitiki sunarthsh opou elegxei katheta    (x,ydown)  |_|_|_|_|  (x+24,ydown)  ean oi epomenes 24 sthles exoun mono aspra shmeia(to xrhsimopoiw sthn parapanw sinartisi gia na brw to telos kathe leksis )
def WhiteLeast24Column(x, yup, ydown):
    for i in range(24):
        for y in range(yup,ydown+1):
            if(numpydata[y][x+i] != 255):
                return False
    
    return True


#Boithitiki sunarthsh opou elegxei katheta ean oi 2 prohgoumenes sthles exoun mono aspra shmeia(to xrhsimopoiw sthn FindLetterStart() sinartisi gia na brw thn arxh grmmatos mias leksis )
def Meanlinecontr(x, yup, ydown):
    meancontr = []
    for y in range(yup,ydown+1):
        meancontr.append(numpydata[y][x])
    
    meanlinecontr = mean(meancontr)

    almostwhite = [255, 254, 253]
    
    if(meanlinecontr in  almostwhite):
        return True
    else:
        return False
        


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
    path = folder1 + 'texts/' + text +'/py/ROIbounds/mytext.page_' + str(pageno) + '.ROIbounds.xlsx'
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
        worksheet.write(row, column1, x[i])
        worksheet.write(row, column2, y[i])
        worksheet.write(row, column3, width[i])
        worksheet.write(row, column4, height[i])
        
        row += 1
        
    workbook.close()


def StoreLineWords(text, pageno, paramname, list):
    if(paramname == "ycorner"):
        path = folder1 + 'texts/' + text + '/py/mytext/page(' + str(pageno) + ')/' + paramname + '/' + paramname + '.xlsx'
    else:
        path = folder1 + 'texts/' + text + '/py/mytext/' + paramname + '/' + paramname + '(' + str(pageno) + ').xlsx'
    
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()

    worksheet.write_column(0,0,list)

    workbook.close()


def StoreLineEdges(text, pageno, paramname, list):
    path = folder1 + 'texts/' + text + '/py/mytext/page(' + str(pageno) + ')/' + paramname + '/' + paramname + '.xlsx'
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()

    for i in range(len(list)):
        worksheet.write(i, 0, list[i][1])   
    
    workbook.close()


# find mid-distance among lines and form y of corner any gap of y
def StoreYgap(text, pageno, paramname, ycorner, ydifflist):
    path = folder1 + 'texts/' + text + '/py/mytext/page(' + str(pageno) + ')/' + paramname + '/' + paramname + '.xlsx'
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
        path1 = folder1 + 'texts/' + text + '/py/mytext/page(' + str(pageno) + ')/' + paramname + '/' + paramname + '.xlsx'
        workbook1 = xlsxwriter.Workbook(path1)
        worksheet1 = workbook1.add_worksheet() 
        worksheet1.write(0, 0, list1[0])
        workbook1.close()
    
    
    elif( paramname == "ROIend" ):
        path1 = folder1 + 'texts/' + text + '/py/mytext/page(' + str(pageno) + ')/' + paramname + '/' + paramname + '.xlsx'
        workbook1 = xlsxwriter.Workbook(path1)
        worksheet1 = workbook1.add_worksheet() 
        worksheet1.write(0, 0, list1[-1])
        workbook1.close()

    
    elif( paramname == "ROIstartx" ):
        ROIstartx = []
        path2 = folder1 + 'texts/' + text + '/py/mytext/page(' + str(pageno) + ')/line/' + paramname + '/' + paramname + '.xlsx'
        workbook2 = xlsxwriter.Workbook(path2)
        worksheet2 = workbook2.add_worksheet()
        for i in range(len(list1)):
            rowROIstartx = list1[i][0][0] - offsetx
            for j in range(len(list1[i])):
                worksheet2.write(j, i, list1[i][j])
                rowROIstartx.append(list1[i][j])
            
            ROIstartx.append(rowROIstartx)
            worksheet2.write_column(0, i, rowROIstartx)

        workbook2.close()
        return ROIstartx
    
    
    elif( paramname == "ROIendx" ):
        ROIendx = []
        wordend = list2
        path2 = folder1 + 'texts/' + text + '/py/mytext/page(' + str(pageno) + ')/line/' + paramname + '/' + paramname + '.xlsx'
        workbook2 = xlsxwriter.Workbook(path2)
        worksheet2 = workbook2.add_worksheet()

        for i in range(len(list1)):
            rowROIendx = []
            for j in range(len(list1[i])):        
                rowROIendx.append(list1[i][j][0] + width[i][j])
            
            rowROIendx[-1] = wordend[i][-1][0] + offsetx
            ROIendx.append(rowROIendx)
            worksheet2.write_column(0, i, rowROIendx)
        
        workbook2.close()
        return ROIendx


    elif( paramname == "ROIgapx" ):
        path2 = folder1 + 'texts/' + text + '/py/mytext/page(' + str(pageno) + ')/line/' + paramname + '/' + paramname + '.xlsx'
        workbook2 = xlsxwriter.Workbook(path2)
        worksheet2 = workbook2.add_worksheet()

        for i in range(len(width)):
            roistartxdiff = [j-i for i, j in zip(list1[i][:-1], list1[i][1:])]
            roistartxdiff.append( list2[i][-1] + offsetx - list1[i][-1] )
            worksheet2.write_column(0, i, roistartxdiff) 
        workbook2.close()
        
    

def StoreLetterInfo(text, pageno, liststartx, listendx, firstlinewords, lastlinewords):
    xdiff = FindXdiff(liststartx, listendx)
    xcorner = []
    xgap = []
    spacenumber = 0
    wordnumber = 0
    wordnumberlist = []
    trueletterlist = []
    rowtrueletter = []
    letterstartx = []
    rowletterstartx = []

    
    for i in range(len(liststartx)):
        letternumber = open(folder1 + 'texts/' + text + '/py/mytext/page(' + str(pageno) + ')/line/letter/letter_number_line(' + str(i+1) + ").txt", "w")
        letternumber.write(str(len(liststartx[i])))
        letternumber.close()

        path = folder1 + 'texts/' + text + '/py/mytext/page(' + str(pageno) + ')/line/letter/letter(' + str(i+1) + ').xlsx'
        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet()

        rowtrueletter = []
        rowletterstartx= []

        # make letternumber
        # make letterstartx
        # make letterendx
        # make letterstarty
        # make letterendy
        # make trueletter
        worksheet.write(0, 0, 'letternumber')
        worksheet.write(0, 1, 'letterstartx')
        worksheet.write(0, 2, 'letterendx')
        worksheet.write(0, 3, 'letterstarty')
        worksheet.write(0, 4, 'letterendy')

        for j in range(len(liststartx[i])):
            worksheet.write(j+1, 0, j+1)
            worksheet.write(j+1, 1, liststartx[i][j])
            worksheet.write(j+1, 2, listendx[i][j])
            worksheet.write(j+1, 3, firstlinewords[i][1])
            worksheet.write(j+1, 4, lastlinewords[i][1])
            
            trueletter = FindTrueLetter(liststartx[i][j],  listendx[i][j],  firstlinewords[i][1], lastlinewords[i][1])
            worksheet.write(0, 5, 'trueletter')
            worksheet.write(j+1, 5, trueletter)

            rowtrueletter.append(trueletter)
            rowletterstartx.append(liststartx[i][j])

        trueletterlist.append(rowtrueletter)
        letterstartx.append(rowletterstartx)


        # make xdiff
        worksheet.write(0, 6, 'xdiff')
        worksheet.write_column(1, 6, xdiff[i])


        # make meanletterdist
        meanletterdist = round(np.median(xdiff[i]))
            # write in .xlsx into /letter/  folder
        worksheet.write(0, 7, 'meanletterdist')
        worksheet.write(1, 7, meanletterdist)


        # # make meanworddist
        # meanworddist = round(np.percentile(xdiff[i], 95))
        #     # write in .xlsx into /letter/  folder
        # worksheet.write(0, 8, 'meanworddist')
        # worksheet.write(1, 8, meanworddist)


        # # make wordbound
        # wordbound = round(0.6*meanworddist)
        #     # write in .xlsx into /letter/  folder
        # worksheet.write(0, 9, 'wordbound')
        # worksheet.write(1, 9, wordbound)


        # make xcorner
        xcorner = []
        for j in range(len(liststartx[i])):
            if( j == 0 ):
                xc = liststartx[i][j] - round(meanletterdist/2)
                xcorner.append( xc )
            else:
                xc = liststartx[i][j] - round(meanletterdist/2)
                xcorner.append( xc )
        worksheet.write(0, 8, 'xcorner')
        worksheet.write_column(1, 8, xcorner)


        # make xgap
        xgap = []
        for j in range( len(liststartx[i]) - 1 ) :
            xg = liststartx[i][j+1] - liststartx[i][j]
            xgap.append(xg)
        worksheet.write(0, 9, 'xgap')
        worksheet.write_column(1, 9, xgap)


        # make wordnumber
        wordnumber = 0
        spacenumber = 0
        for j in range(len(xdiff[i])):
            if( xdiff[i][j] > fixed_nullspace ):
                spacenumber += 1
        wordnumber = spacenumber + 1
        worksheet.write(0, 10, 'wordnumber')
        worksheet.write(1, 10, wordnumber)                       
        wordnumberlist.append(wordnumber)

        workbook.close()
    
    
    return xdiff, wordnumberlist, trueletterlist, letterstartx


def LineLetterNumber(text, pageno, line):
    f = open(folder1 + 'texts/' + text + '/py/mytext/page(' + str(pageno) + ')/line/letter/letter_number_line(' + str(line) + ").txt", "r")
    letternumber = f.read()
    return letternumber


def FindTrueLetter(letterstartx, letterendx, letterstarty, letterendy) :
    meanhorlettercontr = []
    horlettercontr = []
    
    for y in range( letterstarty, letterendy):
        horlettercontr = []
        for x in range(letterstartx, letterendx+1):
            horlettercontr.append(numpydata[y][x])

        meanhorlettercontr.append( np.mean(horlettercontr) )

    
    lastcompiy = 0
    for iy in range(1, len(meanhorlettercontr)):
        if( meanhorlettercontr[iy]<255  and meanhorlettercontr[iy-1]==255 ):
            lastcompiy = iy

    
    if( lastcompiy >= len(meanhorlettercontr)/2 ):
        trueletter = 0
    else:
        trueletter = 1

    return trueletter
    

def FindXdiff(letterstartx, letterendx):
    xdiff = []
    for line in range(len(letterstartx)): 
        rowxdiff = []
        for i in range(len(letterstartx[line])-1):
            rowxdiff.append( letterstartx[line][i+1] - letterendx[line][i] )
        
        xdiff.append( rowxdiff )
    
    return xdiff



def StoreWordInfo(text, pageno, firstlinewords, lastlinewords, letterstartx, letterendx, xdiff, wordnumber, trueletter):
    wordstartxlist = []

    for i in range(len(letterstartx)):
        path = folder1 + 'texts/' + text + '/py/mytext/page(' + str(pageno) + ')/line/word/word(' + str(i+1) + ').xlsx'
        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet() 
        
        worksheet.write(0, 0, 'wordnumber')
        worksheet.write_column(1, 0, [k for k in range(1,wordnumber[i]+1)])

        lettercounter = 0


        # make wordstartx
        wordstartx = []
  
        for j in range(len(letterstartx[i])):
            if( j == 0 ):
                wordstartx.append(letterstartx[i][j])
            else:
                if(xdiff[i][j-1] > fixed_nullspace):
                    wordstartx.append(letterstartx[i][j])

        worksheet.write(0, 1, 'wordstartx')
        worksheet.write_column(1, 1, wordstartx)  
        wordstartxlist.append(wordstartx)

        # make wordendx
        wordendx = []

        for j in range(len(letterendx[i])):
            if( j == len(letterendx[i])-1 ):
                wordendx.append(letterendx[i][j])
            else:
                if(xdiff[i][j] > fixed_nullspace):
                    wordendx.append(letterendx[i][j])


        worksheet.write(0, 2, 'wordendx')
        worksheet.write_column(1, 2, wordendx) 


        # make wordstarty
        worksheet.write(0, 3, 'wordstarty')
        for j in range(wordnumber[i]):
            worksheet.write(j+1, 3, firstlinewords[i][1])


        # make wordstarty
        worksheet.write(0, 4, 'wordendy')
        for j in range(wordnumber[i]):
            worksheet.write(j+1, 4, lastlinewords[i][1])



        # make startletter
        # make endletter
        worksheet.write(0, 5, 'startletter')
        worksheet.write(0, 6, 'endletter')

        rowstart = 1
        rowend = 1

        startletter = []
        endletter = []

        for j in range(len(letterstartx[i])):
            lettercounter += 1
            
            if( j == 0 ):
                worksheet.write(rowstart, 5, lettercounter)
                startletter.append(lettercounter)
                rowstart += 1

            if( j == len(letterstartx[i])-1 ):
                worksheet.write(rowend, 6, lettercounter)
                endletter.append(lettercounter)
                rowend += 1

            if( j<len(letterstartx[i])-1  and  xdiff[i][j] > fixed_nullspace):
                worksheet.write(rowstart, 5, lettercounter+1)
                worksheet.write(rowend, 6, lettercounter) 
                startletter.append( lettercounter+1)
                endletter.append(lettercounter)
                rowstart += 1
                rowend += 1
        

        # make letternumber
        worksheet.write(0, 7, 'letternumber')
        for j in range(wordnumber[i]):
            letternumber = 0
            for letterno in range(startletter[j]-1, endletter[j]):
                letternumber += trueletter[i][letterno]

            worksheet.write(j+1, 7, letternumber)


        workbook.close()
    
    return wordstartxlist


# Store meanletter, meanworddist, offsetx, wordbound
def Letterdist_Worddist_Offsetx_WordBound(text, pageno, xdiff):
    xdiffvectall = []

    path = folder1 + 'texts/' + text + '/py/mytext/page(' + str(pageno) + ')/letter_word_offset_bound/letter_word_offset_bound.xlsx'
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet() 

    for i in range(len(xdiff)):
        xdiffvectall +=  xdiff[i]

    # make meanletterdist
    meanletterdist = round(np.median(xdiffvectall))
    worksheet.write(0, 0, 'meanletterdist')
    worksheet.write(1, 0, meanletterdist)

    # make meanworddist
    meanworddist = round(np.percentile(xdiffvectall, 95))
    worksheet.write(0, 1, 'meanworddist')
    worksheet.write(1, 1, meanworddist)

    # make offsetx
    offsetx = min(meanworddist, 8*meanletterdist)
    worksheet.write(0, 2, 'offsetx')
    worksheet.write(1, 2, offsetx)
    
    # make wordbound
    wordbound = round(0.6 * meanworddist)
    worksheet.write(0, 3, 'wordbound')
    worksheet.write(1, 3, wordbound)

    workbook.close()

    return offsetx, wordbound




# # Example 1
# 
#  for i in range(1,6):
#     text = "visit"
#     pageno = i
#     drawROI(text, pageno)


# Example 2

text = "visit"
pageno = 1
drawROI(text, pageno)
