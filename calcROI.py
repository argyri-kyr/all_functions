

#Υπολογιζει σε ποιο ROI ανηκει ενα σημειο
#args = { (X : x coordinate of point), (Y : y coordinate of point), (x,y,width,height : lists with ROI bounds) }
def calcROI(roistart, X, Y, x, y, width, height):  
    roi=-1   #if a point is not into a ROI bound then point's  roi = -1 (assumption)


    for i in range(len(x)):
        if( x[i] < X <= x[i]+width[i]  and  y[i] < Y <= y[i]+height[i] ):
            roi = i + roistart
 
    return roi  # because roi index starts from 1 not from 0 
    
