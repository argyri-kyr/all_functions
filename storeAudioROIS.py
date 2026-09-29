


from selectROIS_audio import get_selectedROIS


# 1st version of storing the clicked ROIS
def storeAudioROIS_v1(text, pageno, roiselectedpath, finalx, finaly):
    selectedrois = get_selectedROIS(text, pageno, finalx, finaly)

    with open(roiselectedpath, 'a') as roifile:
        roifile.write('\n'.join(str(roi) for roi in selectedrois))
        roifile.write("\n")
    
    print("selectedrois = ", selectedrois)
    return selectedrois



# 2nd version of storing the first column of written comments from text box
def storeAudioROIS_v2(roiselectedpath, data1, data2):
    validcategories = [1,2,3,4]
    
    finalroisselected = []
    for i in range(len(data1)):
        if(data2[i] in validcategories):
            finalroisselected.append(data1[i])

    if( data1==[] ):
        with open(roiselectedpath, 'a') as roifile:
            roifile.write('\n'.join(str(0)) )
            roifile.write("\n")
    else:    
        with open(roiselectedpath, 'w') as roifile:
            roifile.write('\n'.join(str(roi) for roi in finalroisselected))
            roifile.write("\n")
    

        
    print("selectedrois = ", data1)
    return data1
