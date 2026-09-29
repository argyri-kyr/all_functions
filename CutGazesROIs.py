

from calcROI import calcROI

#Φτιαχνω και επιστρεφω μια λιστα που περιεχει τα rois των cutgazes
#args = { (xlist : λιστα με τα cutgazes_x), (ylist : λιστα με τα cutgazes_y) }
def CutGazesROIs(roibounds, roistart, xlist, ylist):
    roislist = []
    for i in range( len(xlist) ):
        point_roi = calcROI(roistart, xlist[i], ylist[i], roibounds[0], roibounds[1], roibounds[2], roibounds[3]) #Find point's ROI
        roislist.append(point_roi)
        
    return roislist