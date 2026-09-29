

import matplotlib.pyplot as plt

from globalVars import folder1, textends
from movefigure import movefigure


def GazesPreview(text, pageno, mypagecollection):
    tempx = mypagecollection[1]
    tempy = mypagecollection[2]
    
    image = folder1 + 'texts/'+ text + textends + '/Slide' + str(pageno) + '.PNG'
    img = plt.imread(image)
   
    g, ax = plt.subplots(1,1,constrained_layout=True)
    g.set_size_inches(5, 4)
    plt.title("Preview\n")
    movefigure(g, 1410, 5)


    plt.plot(tempx,tempy, 'bx', markeredgewidth=0.5)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis('off')
    
    ax.imshow(img)


    return g, ax

