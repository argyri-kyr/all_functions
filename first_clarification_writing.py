
def first_clarification_writing(cgi, cgx, cgy, cgtimestamp, cgvalidity, cgroi, noshifted_y, chosenroislist):
    # Find chosen -- index, x, y, timestamp, roi -- according to chosen line
    shifted_i = []
    shifted_x = []
    shifted_y = []
    shifted_timestamp = []
    shifted_validity = []
    for k in range(len(cgy)):
        if(cgroi[k] in chosenroislist):
            shifted_i.append(cgi[k])
            shifted_x.append(cgx[k])
            shifted_y.append(cgy[k])
            shifted_timestamp.append(cgtimestamp[k])
            shifted_validity.append(cgvalidity[k])


    #  chosen y from cgy list
    noshiftline_cgi = []
    noshiftline_cgx = []
    noshifted_raw_y = []
    noshiftline_cgtimestamp = []
    noshiftline_cgvalidity = []

    for k in range(len(cgy)):
        if( cgy[k] not in shifted_y ):
            noshiftline_cgi.append(cgi[k])
            noshiftline_cgx.append(cgx[k])
            noshifted_raw_y.append(noshifted_y[k])
            noshiftline_cgtimestamp.append(cgtimestamp[k])
            noshiftline_cgvalidity.append(cgvalidity[k])
    
    return shifted_i, shifted_x, shifted_y, shifted_timestamp, shifted_validity, noshiftline_cgi, noshiftline_cgx, noshifted_raw_y, noshiftline_cgtimestamp, noshiftline_cgvalidity
