


from calcROI import calcROI
from globalVars import folder1, folder2


#Συναρτηση που γραφει το αρχειο fixations.txt
#args = { (fixationdata : δεδομενα που εχουν δημιουργηθει απο τις συναρτησεις fixationfun.py,cmshiftfun2.py , δηλαδη fixationdata=newfixdata), (fixationsfile : fixations.txt file path), (roibounds : list with x,y,width,height of ROIS), (pageno : page number) }
#columns of fixations.txt:
#1: Aplh arithmisi
#2: x
#3: y
#4: timestamp gaze start
#5: duration
#6: ROI
#7: gaze start
#8: gaze end
#9: page
#10: timestamp gaze end
def MakeFixationsTxt(sub, exam, text, pageno, roistart, fixationdata, roibounds):
    fixationsgappagetxt = folder1 + folder2 + 'subject_' + str(sub) + '/all_data/' + text + str(exam) + '/fixations' + str(pageno) + '.txt' #Αυτο το αρχειο ειναι το αντιστοιχο του fixationsFF που δημιουργει το matlab με προσθετη στηλη στο τελος τη στηλη του timestampend
    fixationsgappagefile = open(fixationsgappagetxt,'w')
    fixationsgappagefile.close()
    
    fixationtxt = open(fixationsgappagetxt,"a")

    for i in range(len(fixationdata)):
        meanx = int( fixationdata[i][0] ) 
        meany = int( fixationdata[i][1] )
        gazestart = str( fixationdata[i][2] )
        gazeend = str( fixationdata[i][3] )
        timestampstart = str( fixationdata[i][4] )
        timestampend = str( fixationdata[i][5] )
        duration = str( fixationdata[i][6] )

        roi = calcROI(roistart, meanx, meany, roibounds[0], roibounds[1], roibounds[2], roibounds[3])  #Υπολογιζω σε ποιο ROI ανηκει το fixation
        
             
        fixationtxt.write( str(i+1) + "\t" +  str(meanx) + "\t" + str(meany) + "\t" + timestampstart + "\t" + duration + "\t" + str(roi) + "\t" + gazestart + "\t" + gazeend + "\t" + str(pageno) + "\t" + timestampend + "\n" )
    
    fixationtxt.close()  

