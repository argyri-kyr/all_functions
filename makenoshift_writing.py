

def makenoshift_writing(noshifttxt, noshiftline_cgi, noshiftline_cgx, noshifted_raw_y, noshiftline_cgtimestamp, noshiftline_cgvalidity):
    noshifted_has_roi = -1

    for i in range(len(noshiftline_cgi)):
        f = open(noshifttxt,"a")
        f.write(  str(noshiftline_cgi[i]) + "\t" + str(noshiftline_cgx[i]) + "\t" + str(noshifted_raw_y[i]) + "\t" + str(noshiftline_cgtimestamp[i]) + "\t" + str(noshiftline_cgvalidity[i]) + "\t" + str(noshifted_has_roi) + "\n" )
    f.close()