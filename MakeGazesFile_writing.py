
#Συναρτηση που γραφει το αρχειο cutgazes.txt
#args = { (cutgazesfile : cutgazes.txt file path), (cgi : cutgazes index list), (cgx : cutgazes X list), (cgy : cytgazes Y list), (cgtimestamp : cutgazes timestamp list), (cgroi : cutgazes ROI list) }
#columns of cutgazes.txt:
#1: index
#2: x 
#3: y
#4: timestamp
#5: validity
#6: ROI
def MakeGazesTxt_writing(cutgazesfile, gazedata):    
    for i in range( len(gazedata) ):
        f = open(cutgazesfile,"a")
        f.write( str(gazedata[i][0]) + "\t" + str(gazedata[i][1]) + "\t" + str(gazedata[i][2]) + "\t" + str(gazedata[i][3]) + "\t" + str(gazedata[i][4]) + "\t" + str(gazedata[i][5]) + "\n" )
        
    f.close()