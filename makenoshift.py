
# About ROI:
# τα gazes αυτα ειναι gazes που δεν επεσαν ποτε μεσα σε καποιο roi κατα τη διαδικασια των shift, αρα το roi που θα αποθηκευσω γιαυτα τα gazes ειναι το αρχικο τους roi, δηλαδη αυτο που κατεγραψε ο tracker και αποθηκευτηκε στο gazes.txt
def makenoshift(noshifttxt, noshifted_list):
    noshifted_index, noshifted_x, noshifted_raw_y, noshifted_timestamp, noshifted_roi, noshifted_validity, noshifted_vergence, noshifted_pupilsize = noshifted_list[0], noshifted_list[1], noshifted_list[2], noshifted_list[3], noshifted_list[4], noshifted_list[5], noshifted_list[6], noshifted_list[7]
    
    for i in range(len(noshifted_index)):
        f = open(noshifttxt,"a")
        f.write(  str(noshifted_index[i]) + " \t " + str(noshifted_x[i]) + " \t " + str(noshifted_raw_y[i]) + " \t " + str(noshifted_timestamp[i]) + " \t " + str(noshifted_roi[i]) + " \t " + str(noshifted_validity[i]) + " \t " + str(noshifted_vergence[i]) + " \t " + str(noshifted_pupilsize[i]) + "\n" )
    f.close()