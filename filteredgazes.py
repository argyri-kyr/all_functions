


from loaduncutfiltereddata import loaduncutfiltereddata


##################################################################################################
#
# This function replaces the non valid gazes of gazes.txt with valid gazes from gazes_filtered.txt 
#
##################################################################################################


def filteredgazes(sub, exam, text, file, uncutgazes):
    # # # read and collect gazes FILTERED # # #
    gazesfiltered = loaduncutfiltereddata(text, exam, file, sub)
    # # #    # # #
    counter = 0

    indexcol = 0
    xcol = 1
    ycol = 2
    timestampcol = 3
    validitycol = 5

    for i in range(len(uncutgazes[indexcol])):
        if(uncutgazes[validitycol][i]==0):
            while(counter<len(gazesfiltered[0])):
                if(int(uncutgazes[timestampcol][i]) == int(gazesfiltered[timestampcol][counter]) or int(uncutgazes[timestampcol][i])-1 == int(gazesfiltered[timestampcol][counter])):
                    uncutgazes[xcol][i] = gazesfiltered[xcol][counter]
                    uncutgazes[ycol][i] = gazesfiltered[ycol][counter]

                    if(gazesfiltered[xcol][counter]>0 and gazesfiltered[ycol][counter]>0):
                        uncutgazes[validitycol][i] = 1

                    break

                counter += 1


    return uncutgazes