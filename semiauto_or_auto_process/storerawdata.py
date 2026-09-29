
# Store gazedata per page, i.e gazes_page1.txt, gazes_page2.txt, gazes_page3.txt, .....  #
def storegazedata_old_data(file, tempindex, tempx, tempy, temptimestamp):
    for i in range( len(tempindex) ):
        f = open(file,"a")
        f.write( str(tempindex[i]) + "\t" + str(tempx[i]) + "\t" + str(tempy[i]) + "\t" + str(temptimestamp[i]) + "\n" )
        
    f.close()


# Store gazedata per page, i.e gazes_page1.txt, gazes_page2.txt, gazes_page3.txt, .....  #
def storegazedata(file, mypagecollection):
    tempindex, tempx, tempy, temptimestamp, temproi, tempvalidity, tempvergence, temppupilsize = mypagecollection[0], mypagecollection[1], mypagecollection[2], mypagecollection[3], mypagecollection[4], mypagecollection[5], mypagecollection[6], mypagecollection[7]
    
    for i in range( len(tempindex) ):
        f = open(file,"a")
        f.write( str(tempindex[i]) + "\t" + str(tempx[i]) + "\t" + str(tempy[i]) + "\t" + str(temptimestamp[i]) + "\t" + str(temproi[i]) + "\t" + str(tempvalidity[i])+ "\t" + str(tempvergence[i]) + "\t" + str(temppupilsize[i]) + "\n" )
        
    f.close()


# Store validationdata per page, i.e vergence_page1.txt, vergence_page2.txt, vergence_page3.txt, .....  #
def storevergencedata(file, vergenceindex, vergenceleftx, vergencelefty, vergencerightx, vergencerighty, vergencetimestamp, pupilleft, pupilright):
    for i in range( len(vergenceindex) ):
        f = open(file,"a")
        f.write( str(vergenceindex[i]) + "\t" + str(vergenceleftx[i]) + "\t" + str(vergencelefty[i]) + "\t" + str(vergencerightx[i]) + "\t" + str(vergencerighty[i]) + "\t" + str(vergencetimestamp[i]) + "\t" + str(pupilleft[i]) + "\t" + str(pupilright[i]) + "\n" )
        
    f.close()


def store_pupil_z_data(file, pupilsizeleft, pupilsizeright, vergenceleftz, vergencerightz):
    for i in range( len(pupilsizeleft) ):
        f = open(file,"a")
        f.write( str(pupilsizeleft[i]) + "\t" + str(pupilsizeright[i]) + "\t" + str(vergenceleftz[i]) + "\t" + str(vergencerightz[i]) + "\n" )
        
    f.close()