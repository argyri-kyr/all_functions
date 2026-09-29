

from globalVars import folder1, fixed_nullspace, dim, textpos
import cv2
from matplotlib import patches, pyplot as plt
import numpy as np
import time
from statistics import mean
import xlsxwriter
from os.path import exists



def drawROIRAN(text, pageno):

    if( exists(folder1 + textpos + text + '/Slide' + str(pageno) + '_ROIS.png')):
        print("ROI has calculated for Slide%d\n" %(pageno))
        return
    
   
    f, ax = plt.subplots(1)
    f.set_figwidth(9)
    f.set_figheight(7)

    imagepath = folder1 + textpos + text + '/Slide' + str(pageno) + '.png'
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
    
    if(pageno == 1 or pageno==2):
        wordscounter = 0
        



    #Find up and down limits in each line
    start = time.time()
    for y in range(len(numpydata)-10):
        if( mean(numpydata[y]) <253 and isvalid==False ):
            isvalid=True                
            firstlinewords.append([dim[0]/2,y])     # Thelw na apothikefsw to teleutaio aspro giafto apothikeyw to shmeio y-1 kathws sto y exw to prwto mavro
            continue       
        
            #elegxw ean h epomenh grammi einai olh asprh etsi wste na kserw oti apo thn trexon grammi tha prokipsi to teleftaio shmeio ayths ths seiras
        if(  WhiteNext10Row(y,numpydata)==True and isvalid==True ):
            isvalid = False                   #Thetw isvalid=false wste na kserw oti tha psaxnw pali gia to prwto stoixeio ths epomenhw seiras
            lastlinewords.append([dim[0]/2,y])  # Thelw na apothikefsw to prwto aspro giafto apothikeyw to shmeio y+1 kathws sto y exw to teleftaio mavro
            lines += 1
            continue

    end = time.time()
    t1 = end - start
    # print("Time1 = ", t1)


    # Draw up and down limits in each line
    # for i in range(len(firstlinewords)):
    #        plt.scatter(firstlinewords[i][0], firstlinewords[i][1], 14, 'magenta')
    #        plt.scatter(lastlinewords[i][0], lastlinewords[i][1], 14, 'orange' )
    
    
    #Find (and Plot(if i want)) end of Words
    start = time.time()

    letterendx = FindLetterEnd()
    letterstartx = FindLetterStart()


    end = time.time()
    t2 = end - start
    # print("Time2 = ",t2)


    #Find and Drow middle(line) in each line
    start = time.time()
    rows = len(firstlinewords)  

    for i in range(rows):
        x_start = 110
        x_end = letterendx[i][-1]
        y_up = firstlinewords[i][1]
        y_down = lastlinewords[i][1]

        yline.append( midLine(x_start, x_end, y_up, y_down) ) 


    # # draw letter starts
    # for i in range(len(letterstartx)):
    #     for j in range(len(letterstartx[i])):
    #         plt.plot(letterstartx[i][j], yline[i],'ro', markersize=4 )
    #     for j in range(len(letterendx[i])):
    #         plt.plot(letterendx[i][j], yline[i],'bo', markersize=4 )


    end = time.time()
    t3 = end - start
    # print("Time3 = ",t3)

    #Find whiteSpaces between words
    whitespace = WhiteSpace(letterendx)


    # Calculate ycorner
    ydifflist = []

    for i in range(len(firstlinewords)-1):
        ydifflist.append( - lastlinewords[i][1] + firstlinewords[i+1][1] )

    meanydiff = round(mean(ydifflist))
    

    x = firstlinewords[0][1]
    if(pageno==1):
        ycorner.append(firstlinewords[0][1] - round(meanydiff/1.5))
    elif(pageno==2):
        ycorner.append(firstlinewords[0][1] - round(meanydiff/2))
    
    for i in range(1, len(firstlinewords)):
        ycorner.append( firstlinewords[i][1] + round(lastlinewords[i-1][1] - firstlinewords[i][1])/2 )


    # Calculate and Store  fixed_x, fixed_y, xdiff, offsetx, wordnumber, trueletter
    xdiff, wordnumber ,trueletter = StoreLetterInfo(pageno, letterstartx, letterendx, firstlinewords, lastlinewords)

    # Store meanletter, meanworddist, offsetx, wordbound
    offsetx = Letterdist_Worddist_Offsetx_WordBound(pageno, xdiff)


    ROIstartx_0 =  letterstartx[0][0] - offsetx 
    ROIendx_0 = letterendx[0][-1] + offsetx 
    
    fixed_x = ROIstartx_0
    fixed_y = ycorner[0]
    fixed_x_end = ROIendx_0


    # Calculate and Store ygap
    ygap = StoreYgap(pageno, ycorner, ydifflist)


    # FIND and DRAW ROI bounds between Words


    # Find middle distance between two words
    middistw = []    # middle space between words(only x indexes, because we don't need y, we only need x for declare width of rectangle)  
    for i in range(rows):
        row=[]
        for j in range(len(letterendx[i])-1):
            mid_x = letterendx[i][j] + whitespace[i][j]/2
            row.append( mid_x )
            
        middistw.append(row)


    # Find word's width in rectangle
    width = []
    for i in range(rows):
        row=[]
        for j in range(len(middistw[i])+1):
            if(j==0 and middistw[i]!=[]): #Ean eimai sthn 1h lexi ths kathe grammis tote exw fixed arxh kai elegxw oti den exw mono mia lexi sth grammi giati tote tha exw diaforetiko width kathws to middistw[i] tha einai keno ara den mporw na to xrhsimopoihsw
               w = middistw[i][j] - fixed_x 
               row.append(w)
            elif(j==0 and middistw[i]==[]):  #Ean exw mono mia lexi se kapoia grammi
                w = (letterendx[i][j] - fixed_x)   
                row.append(w)
            elif( j==len(middistw[i]) ):
                w = fixed_x_end - middistw[i][j-1]
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
    

    # Find wordnumberfirstlinewords, wordnumberlastlinewords, ROIstartpoint
    for row in range(len(letterendx)):
        rowROIstart = []

        if(row==0):
            y = fixed_y
        else:
            y = middistr[row-1]

        for i in range(len(letterendx[row])):
            wordscounter += 1    

            if(i==0):    #Ean eimai sthn 1h lexi kathe grammis
                x = fixed_x
            else:
                x = middistw[row][i-1]

            rowROIstart.append( [x,y] )

        wordnumberfirstlinewords.append(wordscounter-len(letterendx[row])+1)   # list for firstlinewords
        wordnumberlastlinewords.append(wordscounter)   # list for lastlinewords
        ROIstartpoint.append( rowROIstart )  



    # Store ROIstart, ROIend
    ROIstart = StoreROIstartend(pageno, "ROIstart", wordnumberfirstlinewords, [], [], offsetx)
    ROIend = StoreROIstartend(pageno, "ROIend", wordnumberlastlinewords, [], [], offsetx)


    # Store ROIstartx, ROIendx
    ROIstartx = StoreROIstartend(pageno, "ROIstartx", ROIstartpoint, [], [], offsetx)
    ROIendx = StoreROIstartend(pageno, "ROIendx", ROIstartpoint, letterendx, width, offsetx)

    # Store ROIgapx
    StoreROIstartend(pageno, "ROIgapx", ROIstartx, ROIendx, width, offsetx)

    
    # # fix width[-1] per line
    # for i in range(len(letterstartx)):
    #     width[i][-1] = fixed_x_end - middistw[i][-1]


    # Draw Rectangle
    final_x = []
    final_y = []
    final_width = []
    final_height = []
    
    for row in range(len(letterendx)):
        rowROIstart = []

        if(row==0):
            y = fixed_y
        else:
            y = middistr[row-1]
        

        for i in range(len(letterendx[row])):
            wordscounter += 1    

            if(i==0):    #Ean eimai sthn 1h lexi kathe grammis
                x = fixed_x
            else:
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

    
    plt.savefig(folder1 + textpos + text +'/Slide' + str(pageno) + '_ROIS.png')
    # plt.show()
    plt.close('all')

    return firstlinewords , lastlinewords, letterendx, t1, lines, yline, wordnumberfirstlinewords, wordnumberlastlinewords



#Sinarthsh opou elegxei ean eimai sto telos mias grammis, elegxontas ean oi epomenes 2 grammes exoun mono aspra shmeia
def WhiteNext10Row(y,numpydata):
    for i in range(1,11):
        if( mean(numpydata[y+i])<253 ):
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

                if(numpydata[y][tempx]>253):
                    black = False

                if(numpydata[y][tempx]<253):
                    black = True

                while( numpydata[y][tempx+1]>253 and black==True and tempx<len(numpydata[0])-25 ):
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



def FindLetterEnd():
    letterendx = []
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
                    row.append( x ) 
        
        letterendx.append( row )
    
    return letterendx
                

def FindLetterStart():
    letterstartx = []
    row = []

    black = False

    for i in range(len(firstlinewords)):
        black = False
        row = []

        for x in range(len(numpydata[0])-25):
            for y in range(firstlinewords[i][1],lastlinewords[i][1]+1):  
                if(numpydata[y][x]<253):
                    black = True
                    break

            if( black==True ):
                black = False
                if( Meanlinecontr(x-1, firstlinewords[i][1], lastlinewords[i][1]+1)==True  and  Meanlinecontr(x, firstlinewords[i][1], lastlinewords[i][1]+1)==False ):
                    row.append( x-1 )     # Thelw na apothikefsw to teleftaio aspro prin to prwto mavro, giafto apothikevw to x-1, alliws an ithela to prwto mavro tha apothikeva to x

        
        letterstartx.append( row )

    return letterstartx


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

    # plt.plot(x, y ,linewidth=1.5)

    return midy


#Sinarthsh opou ipologizei tis aspres sthles apo mia leksi se mia allh, prokeimenou na brw pou tha xwrisw duo lekseis
def SumWhiteColumn(i, j, letterendx, yup, ydown):
    space = 0
    for x in range( letterendx[i][j]+1, letterendx[i][j+1] ):
        for y in range(yup, ydown+1):
            if(numpydata[y][x] < 253):
                return space
        space+=1
    
    return space


#Sinarthsh opou epistrefei mia lista me stoixeia listes, opou oi eswterikes listes periexoun ta kena diasthmata apo leksi se leksi ana grammi
def WhiteSpace(letterendx):
    whitespaces = []
    for i in range(len(letterendx)):
        whitelistperrow=[]
        for j in range(len(letterendx[i])-1):
            whitelistperrow.append(SumWhiteColumn(i, j, letterendx, firstlinewords[i][1], lastlinewords[i][1]))
        
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
        worksheet.write(row, column1, x[i])
        worksheet.write(row, column2, y[i])
        worksheet.write(row, column3, width[i])
        worksheet.write(row, column4, height[i])
        
        row += 1
        
    workbook.close()


# find mid-distance among lines and form y of corner any gap of y
def StoreYgap(pageno, ycorner, ydifflist):

    ygap = [i+1 for i in np.diff(ycorner).tolist()]

    # find ygap on the last line
    meanydiff = round(mean(ydifflist))
    if(pageno==1):
        ylineoffset = round(meanydiff/4)
    elif(pageno==2):
         ylineoffset = round(meanydiff/6)
    ygap.append( round(mean(ygap)) + ylineoffset )

    return ygap


def StoreROIstartend(pageno, paramname, list1, list2, width, offsetx):
    if( paramname == "ROIstart" ):
        return  list1[0]
    
    
    elif( paramname == "ROIend" ):
        return list1[-1]

    
    elif( paramname == "ROIstartx" ):
        ROIstartx = []

        for i in range(len(list1)):
            rowROIstartx = []
            for j in range(len(list1[i])):
                rowROIstartx.append(list1[i][j][0])
            
            ROIstartx.append(rowROIstartx)

    
        return ROIstartx
    
    
    elif( paramname == "ROIendx" ):
        ROIendx = []
        wordend = list2

        for i in range(len(list1)):
            rowROIendx = []
            for j in range(len(list1[i])):        
                rowROIendx.append(list1[i][j][0] + width[i][j])
            
            rowROIendx[-1] = wordend[i][-1] + offsetx
            ROIendx.append(rowROIendx)
         
        return ROIendx


    elif( paramname == "ROIgapx" ):
        for i in range(len(width)):
            roistartxdiff = [j-i for i, j in zip(list1[i][:-1], list1[i][1:])]
            roistartxdiff.append( list2[i][-1] + offsetx - list1[i][-1] )

        

def StoreLetterInfo(pageno, liststartx, listendx, firstlinewords, lastlinewords):
    xdiff = FindXdiff(liststartx, listendx)
    xcorner = []
    xgap = []
    spacenumber = 0
    wordnumber = 0
    wordnumberlist = []
    trueletterlist = []
    rowtrueletter = []
    
    for i in range(len(liststartx)):
        rowtrueletter = []

        for j in range(len(liststartx[i])):
            trueletter = FindTrueLetter(liststartx[i][j],  listendx[i][j],  firstlinewords[i][1], lastlinewords[i][1])
            rowtrueletter.append(trueletter)

        trueletterlist.append(rowtrueletter)


        # make meanletterdist
        meanletterdist = round(np.median(xdiff[i]))


        # make xcorner
        xcorner = []
        for j in range(len(liststartx[i])):
            if( j == 0 ):
                xc = liststartx[i][j] - round(meanletterdist/2)
                xcorner.append( xc )
            else:
                xc = liststartx[i][j] - round(meanletterdist/2)
                xcorner.append( xc )



        # make xgap
        xgap = []
        for j in range( len(liststartx[i]) - 1 ) :
            xg = liststartx[i][j+1] - liststartx[i][j]
            xgap.append(xg)


        # make wordnumber
        wordnumber = 0
        spacenumber = 0
        for j in range(len(xdiff[i])):
            if( xdiff[i][j] > fixed_nullspace ):
                spacenumber += 1
        wordnumber = spacenumber + 1
                     
        wordnumberlist.append(wordnumber)

    
    
    return xdiff, wordnumberlist, trueletterlist


def LineLetterNumber(text, pageno, line):
    if(pageno==1):
        return 5
    else:
        return 6


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
            difference = letterstartx[line][i+1] - letterendx[line][i]
            rowxdiff.append( difference )
        
        xdiff.append( rowxdiff )
    
    return xdiff




# Store meanletter, meanworddist, offsetx, wordbound
def Letterdist_Worddist_Offsetx_WordBound(pageno, xdiff):
    xdiffvectall = []

    for i in range(len(xdiff)):
        xdiffvectall +=  xdiff[i]

    # make meanletterdist
    meanletterdist = round(np.median(xdiffvectall))

    # make meanworddist
    meanworddist = round(np.percentile(xdiffvectall, 95))

    # make offsetx
    offsetx = min(meanworddist, 8*meanletterdist)

    
    # make wordbound
    wordbound = round(0.6 * meanworddist)

    return offsetx

