


import matplotlib.pyplot as plt
import matplotlib as mpl
from globalVars import folder1, textends
from movefigure import movefigure


def GazesPreview_testattention(text, pageno, mypagecollection, cgdata):
    tempx = mypagecollection[1]
    tempy = mypagecollection[2]
    
    cgx = cgdata[1]
    cgy = cgdata[2]
    
    image = folder1 + 'texts/'+ text + textends + '/Slide' + str(pageno) + '.PNG'
    img = plt.imread(image)
   
    g, ax = plt.subplots(1,1,constrained_layout=True)
    g.set_size_inches(9, 7)
    ax.margins(x=0)
    mpl.rcParams['savefig.pad_inches'] = 0
    
    plt.title("Test Attention - Gazes Preview\n")
    movefigure(g, 550, 100)


    plt.plot(tempx,tempy, 'x', color = '#6685E9', markeredgewidth=0.5)
    plt.plot(cgx, cgy, 'x', color = '#E96F66', markeredgewidth=0.5)
    
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis('off')
    
    ax.imshow(img)


    return g, ax