import statistics
import tkinter
from matplotlib import pyplot as plt
import matplotlib
import pandas as pd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, textends
from calcROI import calcROI
from Median import Median


#Βρισκω ποσες γραμμες εχει η σελιδα που βρισκομαι
def getpagelines(text, pageno):
    data = pd.read_excel(folder1 + 'texts/' + text + textends + '/py/lines/mytext.page(' + str(pageno) + ').lines.xlsx')
    x = data.iloc[:,0]
    return x[0]


#Υπολογιζω το yline καθε γραμμης
def CalculateYline(text, pageno):
    data = pd.read_excel(folder1 + 'texts/' + text + textends + '/py/Yline/mytext.page(' + str(pageno) + ').line.yline.xlsx')
    yline = []
    yline = data.iloc[:,0]
    yline = yline.to_list()

    return yline


#Φτιαχνω και Επιστρεφω τις λιστες με τα cutgazes(index, x, y, timestamp roi) ana selida
#args = { (text : text), (pageno : page_number), (tindex : temporary index list), (tx : temporary x list), (ty : temporary y list), (ttimestamp : temporary timestamp list) }\
#variables = { (cgi : cutgazes index list), (cgx : cutgazes x list), (cgy : cutgazes y list), (cgtimestamp : cutgazes timestamp list), (cgroi : cutgazes rois list), (start : index of first cut), (stop : index of last cut) }
def CutGazes(text, pageno, roistart, tindex, tx, ty, ttimestamp, finalindexes, roibounds, from_runcrashes):

    # Make data initializations
    global cgroi
    cgi, cgx, cgy, cgtimestamp, cgroi = [], [], [], [], []


    start = int( finalindexes[0] )
    stop = int( finalindexes[-1] )

    #Εδω θα φτιαξω τις cgi, cgx, cgtimestamp
    for i in range( start , stop ):
        cgi.append(tindex[i])
        cgx.append(tx[i])
        cgtimestamp.append(ttimestamp[i])


    #Εδω θα φτιαξω την cgy με τα shift
    shiftlist = []
    yline = CalculateYline(text, pageno)
    for i in range(len(finalindexes)-1):
        start = int( finalindexes[i] )
        stop = int( finalindexes[i+1] )
        tempcgy = []
        for j in range(start,stop):
            tempcgy.append(ty[j])  #tempcgy : λιστα που περιεχει τα cutgazes y χωρις το shift
        
        
        nonzerostempcgy = [ point for point in tempcgy if point!=0 ]
        nonzerostempcgy = [ point for point in nonzerostempcgy if point!=-1 ] # to nonzerocgy y exei ola ta gazes kai ta valid kai ta nonvalid. Gia na ipologisw omws th median ta -1 mou einaio axrista kai ta petaw.
        
        ymedian = Median(nonzerostempcgy, 0)
        
        
        #Εδω φτιαχνω τη λιστα οπου περιχει τα cutgazes y με το shift
        for j in range(start,stop): 
            cgy.append( ty[j] + (yline[i]-ymedian) )
        
        shiftlist.append(yline[i]-ymedian)
    
    #ftiaxnw kai th sthlh twn rois
    cgroi = CutGazesROIs(roistart, cgx, cgy, roibounds)  #Και αυτη η συναρτηση θα μου φτιαξει τη λιστα με τα rois των cutgazes 


    crashescutx = []
    crashescuty = []
    crashesindex = []
    crashestimestamp = []
    index = 0
    if(from_runcrashes==True):
        for i in range(len(cgx)):
            if( cgx[i]==0.0  and  cgy[i] in shiftlist ):
                continue
            else:
                index+=1
                crashescutx.append(cgx[i])
                crashescuty.append(cgy[i])
                crashesindex.append(index)
                crashestimestamp.append(cgtimestamp[i]) 

    
        cgroi = CutGazesROIs(roistart, crashescutx, crashescuty, roibounds)

        return crashesindex, crashescutx, crashescuty, crashestimestamp, cgroi
    


    return cgi, cgx, cgy, cgtimestamp, cgroi




#Sinartisi opou epistrefei to grafima me ta kopsimata pou exw kanei mazi me ta gazes, dhladh gazes kai cutgazes, gia na apofasisw an dexomai ta kopsimata pou ekana h oxi
def ShowGazesAndCutGazes(text, pageno, tempx, tempy, cgx, cgy, flag):
    
    if(flag!=-1):
        f = plt.figure(dpi=100)

    image = folder1 + 'texts/'+ text + textends + '/Slide' + str(pageno) + '.PNG'
    img = plt.imread(image)
   
    f, ax = plt.subplots(1,1,constrained_layout=True)
    f.set_size_inches(8, 7)

    if(flag!=-1):
        plt.plot(tempx,tempy, 'x', markerfacecolor='#000000', markeredgewidth=0.5)
        plt.plot(cgx, cgy, 'x', markerfacecolor='#000000', markeredgewidth=0.5)
    else:
        plt.plot(tempx,tempy, 'x', color = '#6685E9', markeredgewidth=0.5)
        plt.plot(cgx, cgy, 'x', color = '#E96F66', markeredgewidth=0.5)
        

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis('off')
    
    ax.imshow(img)
    
    if(flag==0 or flag==-1):
        global window

        window = tkinter.Tk()
        canvas = FigureCanvasTkAgg(f,master = window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
        return f, window
    
    if(flag==1):
        matplotlib.use('Agg')
        f.set_size_inches(13.66, 7.68)
        return



#Φτιαχνω και επιστρεφω μια λιστα που περιεχει τα rois των cutgazes
#args = { (xlist : λιστα με τα cutgazes_x), (ylist : λιστα με τα cutgazes_y) }
def CutGazesROIs(roistart, xlist, ylist, roibounds):
    newcgroi = []
    for i in range( len(xlist) ):
        point_roi = calcROI(roistart, xlist[i], ylist[i], roibounds[0], roibounds[1], roibounds[2], roibounds[3]) #Find point's ROI
        newcgroi.append(point_roi)
        
    return newcgroi



# finalindexes =  [0, 208, 333, 435, 626, 731, 770]
# text = 'efeyreseis'
# pageno = 3
# CutGazes(text, pageno, tindex, tx, ty, ttimestamp, finalindexes, roibounds, from_runcrashes)
