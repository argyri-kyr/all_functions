
def first_clarification(cgdata, noshifted_y, chosenroislist):
    # Find chosen -- index, x, y, timestamp, roi -- according to chosen line
    shifted_i = []
    shifted_x = []
    shifted_y = []
    shifted_timestamp = []
    shifted_validity = []
    shifted_vergence = []
    shifted_pupilsize = []

    for k in range(len(cgdata[2])):
        if(cgdata[4][k] in chosenroislist):
            shifted_i.append( cgdata[0][k] )
            shifted_x.append( cgdata[1][k] )
            shifted_y.append( cgdata[2][k] )
            shifted_timestamp.append( cgdata[3][k] )
            shifted_validity.append( cgdata[5][k] )
            shifted_vergence.append( cgdata[6][k] )
            shifted_pupilsize.append( cgdata[7][k] )

    #  chosen y from cgy list
    noshifted_cgi = []
    noshifted_cgx = []
    noshifted_raw_y = []
    noshifted_cgtimestamp = []
    noshifted_cgroi = []
    noshifted_cgvalidity = []
    noshifted_cgvergence = []
    noshifted_cgpupilsize = []

    for k in range(len(cgdata[2])):
        if( cgdata[2][k] not in shifted_y ):
            noshifted_cgi.append(cgdata[0][k])
            noshifted_cgx.append(cgdata[1][k])
            noshifted_raw_y.append(noshifted_y[k])
            noshifted_cgtimestamp.append(cgdata[3][k])
            noshifted_cgroi.append(cgdata[4][k])
            noshifted_cgvalidity.append( cgdata[5][k] )
            noshifted_cgvergence.append( cgdata[6][k] )
            noshifted_cgpupilsize.append( cgdata[7][k] )
    

    shifted_list = [shifted_i, shifted_x, shifted_y, shifted_timestamp, shifted_validity, shifted_vergence, shifted_pupilsize]
    noshifted_list = [noshifted_cgi, noshifted_cgx, noshifted_raw_y, noshifted_cgtimestamp, noshifted_cgroi, noshifted_cgvalidity, noshifted_cgvergence, noshifted_cgpupilsize]

    return shifted_list, noshifted_list
