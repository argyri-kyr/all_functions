



def eyeposition_finalindex_clear(tempindex, templeftx, temprightx, templefty, temprighty, templeftvalid, temprightvalid, finalindexes):
    start = finalindexes[0]
    end = finalindexes[-1]
    start = tempindex.index(start)
    end = tempindex.index(end)
    

    vergenceleftx_clean = [None for i in range(start)]
    vergenceleftx_clean += templeftx[start:end+1]
    vergenceleftx_clean += [None for i in range(end+1, len(templeftx))]
    
    vergencerightx_clean = [None for i in range(start)]
    vergencerightx_clean += temprightx[start:end+1]
    vergencerightx_clean += [None for i in range(end+1, len(temprightx))]
    
    vergencelefty_clean = [None for i in range(start)]
    vergencelefty_clean += templefty[start:end+1]
    vergencelefty_clean += [None for i in range(end+1, len(templefty))]
    
    vergencerighty_clean = [None for i in range(start)]
    vergencerighty_clean += temprighty[start:end+1]
    vergencerighty_clean += [None for i in range(end+1, len(temprighty))]
    
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    for j in range(len(tempindex)):
        if(templeftvalid[j]==1):
            count1+=1
        if(temprightvalid[j]==1):
            count2+=1
        if(templeftvalid[j]==1 and temprightvalid[j]==0):
            myindex = tempindex[j]
            count3+=1
        if(templeftvalid[j]==0 and temprightvalid[j]==1):
            myindex = tempindex[j]
            count4+=1
    
    
    return tempindex, vergenceleftx_clean, vergencerightx_clean, vergencelefty_clean, vergencerighty_clean, templeftvalid, temprightvalid