
import cv2
import numpy as np

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, textends


def brighterimages(text, pageno, path1):
    image = cv2.imread(path1)

    #image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    increase = 200

    v = image[:, :, 0]
    v = np.where(v <= 255 - increase, v + increase, 255)
    image[:, :, 0] = v
    
    v = image[:, :, 1]
    v = np.where(v <= 255 - increase, v + increase, 255)
    image[:, :, 1] = v
    
    v = image[:, :, 2]
    v = np.where(v <= 255 - increase, v + increase, 255)
    image[:, :, 2] = v

    #image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)

    path2 = folder1 + 'texts/'+ text + textends + '/Slide' + str(pageno) + 'brighter.PNG'
    cv2.imwrite(path2, image)

    return image