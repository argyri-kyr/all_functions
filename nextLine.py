

import statistics
from chosenrois import chosenrois

from find_y_fromhist import find_y_fromhist
from CutGazesROIs import CutGazesROIs
from calculateYline import calculateYline


def nextLine(text, pageno, noshifted_list, shiftedLines, lastlinewords, roistart, roibounds, ylinesin):
    noshifted_cgi, noshifted_cgx, noshifted_raw_y, noshifted_cgtimestamp, noshifted_cgroi, noshifted_cgvalidity, noshifted_cgvergence, noshifted_cgpupilsize = noshifted_list[0], noshifted_list[1], noshifted_list[2], noshifted_list[3], noshifted_list[4], noshifted_list[5], noshifted_list[6], noshifted_list[7]
    
    chosen_i = []
    chosen_x = []
    chosen_y = []
    chosen_timestamp = []
    chosen_validity = []
    chosen_vergence = []
    chosen_pupilsize = []

    nochosen_i = []
    nochosen_x = []
    nochosen_y = []
    nochosen_timestamp = []
    nochosen_roi = []
    nochosen_validity = []
    nochosen_vergence = []
    nochosen_pupilsize = []

    shifted_y = []


    ymedian = statistics.median(list(filter(lambda x: x != -1, noshifted_raw_y)))
    print("ymedian = ",ymedian)

    ymode = statistics.mode(list(filter(lambda x: x != 0, noshifted_raw_y)))
    print("ymode = ",ymode)
    # print("count(ymode) = ", nonzerostempcgy.count(ymode))

    avg = find_y_fromhist(list(filter(lambda x: x != 0, noshifted_raw_y)))
    print("avg_occ = ",avg)


    # identify lines
    templinedist = []
    for origlineno in range(len(ylinesin)):
        templinedist.append( abs(avg - ylinesin[origlineno]) )
        if( (origlineno+1) in shiftedLines ):
            templinedist[-1] = float('inf')
    print("templinedist = ",templinedist)

    linedist = templinedist.index( min(templinedist) )
    chosenline = linedist + 1
    print("chosenline = ", chosenline)
    
    chosenroislist = chosenrois(chosenline, lastlinewords)
    

    #Εδω θα φτιαξω την cgy με τα shift
    yline = calculateYline(text, pageno)
    for i in range(len(noshifted_raw_y)):
        shifted_y.append( noshifted_raw_y[i] + (yline[linedist]-avg) )
    
    new_roi = CutGazesROIs(roibounds, roistart, noshifted_cgx, shifted_y)

    for i in range(len(shifted_y)):
        if( new_roi[i] in chosenroislist ):
            chosen_i.append( noshifted_cgi[i] )
            chosen_x.append( noshifted_cgx[i] )
            chosen_y.append( shifted_y[i] )
            chosen_timestamp.append( noshifted_cgtimestamp[i] )
            chosen_validity.append( noshifted_cgvalidity[i] )
            chosen_vergence.append( noshifted_cgvergence[i] )
            chosen_pupilsize.append( noshifted_cgpupilsize[i] )

        elif( new_roi[i] not in chosenroislist ):
            nochosen_i.append( noshifted_cgi[i] )
            nochosen_x.append( noshifted_cgx[i] )
            nochosen_y.append( noshifted_raw_y[i] )
            nochosen_timestamp.append( noshifted_cgtimestamp[i] )
            nochosen_roi.append( noshifted_cgroi[i] )
            nochosen_validity.append( noshifted_cgvalidity[i] )
            nochosen_vergence.append( noshifted_cgvergence[i] )
            nochosen_pupilsize.append( noshifted_cgpupilsize[i] )

    chosenlist = [chosen_i, chosen_x, chosen_y, chosen_timestamp, chosen_validity, chosen_vergence, chosen_pupilsize]
    nochosenlist = [nochosen_i, nochosen_x, nochosen_y, nochosen_timestamp, nochosen_roi, nochosen_validity, nochosen_vergence, nochosen_pupilsize]

    return chosenline, chosenlist, nochosenlist