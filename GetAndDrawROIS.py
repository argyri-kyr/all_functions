
from asyncio.windows_events import NULL
import matplotlib
import matplotlib.pyplot as plt
from drawFixations import drawFixations
import pandas as pd
from globalVars import folder1, folder2, textends,pyimagepath

#Sinarthsh opou diabazei apo ton fakelo py tou keimenou ta ROI bounds tou kai ta epistrefei
def getROIbounds(text, pageno):

    #Read ROI bounds
    path = folder1 + 'texts/' + text + textends + '/py/ROIbounds/mytext.page_' + str(pageno) + '.ROIbounds.xlsx'

    data = pd.read_excel (path)

    x = []
    x = data.iloc[:,0]
    x = x.to_list()

    y = []
    y = data.iloc[:,1]
    y = y.to_list()

    width = []
    width = data.iloc[:,2]
    width = width.to_list()

    height = []
    height = data.iloc[:,3]
    height = height.to_list()

    return x, y, width, height



#Φτιαχνω τις λιστες που περιεχουν τα δεδομενα των ROI bounds της καθε σελιδας του κειμενου που θελω και ζωφραφιζω ειτε το γραφημα των cutgazes ειτε των rawgazes
#args = { (sub1 : subject's id), (exam : subject's exam), (text : analysis text), (pageno : page number), (roibounds : text's roi bounds), (cgx : cutgazes X list), (cgy : cytgazes Y list), (draw : entolh opou pairnei ws times -- "cutgazes" or "rawgazes" -- prokeimenou na gnwrizv poio grafima thelw apo ta duo na zwgrafisw otan kalesw th sinarthsh), (fixationdata : δεδομενα που εχουν δημιουργηθει απο τις συναρτησεις fixationfun.py,cmshiftfun2.py , δηλαδη fixationdata=newfixdata), (plot : plot's parametre in order to draw ,in this function, the rest of things i want in a plot that's already open) }

def drawROIbounds(sub1, exam, text, pageno, roibounds, cgx, cgy, draw, fixationdata, plot, closeplot):
    
    if(plot==NULL):
        f = plt.figure(dpi=100) 
        f.set_size_inches(13.66, 7.68)
        plot=plt


    image = folder1 + 'texts/' + text + textends + '/Slide' + str(pageno) + '.PNG'
    img = plt.imread(image)
    ax = plt.subplot(1,1,1)
    ax.imshow(img)
    
    plot.axis('off')

    #I WILL MAKE/DRAW THE ROI BOUNDS
    x = roibounds[0]
    y = roibounds[1]
    width = roibounds[2]
    height = roibounds[3]

    for i in range(len(x)):
        rect = matplotlib.patches.Rectangle((x[i],y[i]),
                                        width[i], height[i],
                                        color ='#79D0EB',
                                        fill=False)


        ax.add_patch(rect)
    
    
    #I WILL PLOT THE CUTGAZES OR I WILL SAVE THE RAWGAZES PLOT THAT I HAVE MADE
    if(draw=="cutgazes"):
        plot.plot(cgx, cgy, 'bx', markeredgewidth=0.5)
        drawFixations(sub1, exam, text, fixationdata, pageno, "no", plot)


    if(draw=="rawgazes"):
        # plot.pause(3)
        plot.savefig(folder1 + folder2 + 'subject_'+ str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/rawgazes' + str(pageno) + '.png', dpi=100)

    if(draw=="shift'em"):
        plot.savefig(folder1 + folder2 + 'subject_'+ str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/autoshifted' + str(pageno) + '.png', dpi=100)
    
    if(closeplot=="close"):
        plot.close()