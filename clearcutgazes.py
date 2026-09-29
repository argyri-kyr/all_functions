


# # # # # OMIT NON VALID GAZES on NEW GAZE FILE
# # #  # omit all gazes that are not valid

def clearcutgazes(cgdata, noshifted_y):
    clear_cutgazes = []
    clear_index = []
    clear_x = []
    clear_y = []
    clear_timestamp = []
    clear_roi = []

    clear_noshifted_y = []

    for i in range(len(cgdata[0])):
        if( cgdata[4][i] != -1 ):
            clear_index.append(cgdata[0][i])
            clear_x.append(cgdata[1][i])
            clear_y.append(cgdata[2][i])
            clear_timestamp.append(cgdata[3][i])
            clear_roi.append(cgdata[4][i])

            if( noshifted_y != [] ):
                clear_noshifted_y.append(noshifted_y[i])
    
    clear_cutgazes = [ clear_index, clear_x, clear_y, clear_timestamp, clear_roi ]
        
    return clear_cutgazes, clear_noshifted_y