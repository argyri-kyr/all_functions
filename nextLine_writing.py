

import statistics
from chosenrois import chosenrois

from find_y_fromhist import find_y_fromhist
from CutGazesROIs import CutGazesROIs
from calculateYline import calculateYline


def nextLine_writing(text, pageno, noshiftline_cgi, noshiftline_cgx, noshifted_raw_y, noshiftline_cgtimestamp, noshiftline_cgvalidity, shiftedLines, lastlinewords, roistart, roibounds, ylinesin):
    chosen_i = []
    chosen_x = []
    chosen_y = []
    chosen_timestamp = []
    chosen_validity = []

    nochosen_i = []
    nochosen_x = []
    nochosen_y = []
    nochosen_timestamp = []
    nochosen_validity = []

    shifted_y = []


    ymedian = statistics.median(list(filter(lambda x: x != 0, noshifted_raw_y)))
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
    # print("chosenline = ", chosenline)
    
    chosenroislist = chosenrois(chosenline, lastlinewords)
    

    #Εδω θα φτιαξω την cgy με τα shift
    yline = calculateYline(text, pageno)
    for i in range(len(noshifted_raw_y)):
        shifted_y.append( noshifted_raw_y[i] + (yline[linedist]-avg) )
    
    new_roi = CutGazesROIs(roibounds, roistart, noshiftline_cgx, shifted_y)

    for i in range(len(shifted_y)):
        if( new_roi[i] in chosenroislist ):
            chosen_i.append( noshiftline_cgi[i] )
            chosen_x.append( noshiftline_cgx[i] )
            chosen_y.append( shifted_y[i] )
            chosen_timestamp.append( noshiftline_cgtimestamp[i] )
            chosen_validity.append(noshiftline_cgvalidity[i]  )

        elif( new_roi[i] not in chosenroislist ):
            nochosen_i.append( noshiftline_cgi[i] )
            nochosen_x.append( noshiftline_cgx[i] )
            nochosen_y.append( noshifted_raw_y[i] )
            nochosen_timestamp.append( noshiftline_cgtimestamp[i] )
            nochosen_validity.append( noshiftline_cgvalidity[i] )


    chosenlist = [chosen_i, chosen_x, chosen_y, chosen_timestamp, chosen_validity]
    nochosenlist = [nochosen_i, nochosen_x, nochosen_y, nochosen_timestamp, nochosen_validity]

    return chosenline, chosenlist, nochosenlist