

from globalVars import folder1, folder2, textends

def restoreDrops(sub1, exam, text, from_filename, txtfile, worksheet_before, worksheet_after):

    # Create list with fixation_data or cutgazes_data per line
    filepath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/' + from_filename + '_gap.txt'
    myfile = open(filepath, "r")

    filedata = []
    for line in myfile:
        filedata.append( [float(x) for x in line[:-1].split("\t")] )
    
    # Find roi's column in each case
    if(from_filename=='cutgazes'):
        validitycolumn = 4
        roicolumn = 5
    elif(from_filename=='fixations'):
        validitycolumn = 5

    # Create empty count lists
    wordnumberpath = folder1 + 'texts/' + text + textends + '/py/mytext/wordnumber.txt'
    wordnumberfile = open(wordnumberpath, "r")
    wordnumber = int(wordnumberfile.read())
    
    beforedrops = [0 for i in range(wordnumber)]
    afterdrops = [0 for i in range(wordnumber)]
   
    # Start Process 
    fromroi = False
     
    for i in range(len(filedata)):
        if( i>0 and filedata[i][validitycolumn]==-1 and filedata[i-1][validitycolumn]!=-1 ):
            fromroi = True
            prev_roi = int(filedata[i-1][roicolumn])
            txtfile.write("From ROI: " + str(prev_roi))
            if( prev_roi > 0 ):
                beforedrops[prev_roi-1] += 1
        
        if(  i<len(filedata)-1 and filedata[i][validitycolumn]==-1 and filedata[i+1][validitycolumn]!=-1 and fromroi==True ):
            fromroi = False
            next_roi = int(filedata[i+1][roicolumn])
            txtfile.write(" To ROI: " + str(next_roi) + "\n")
            if( next_roi > 0 ):
                afterdrops[next_roi-1] += 1
    
    
    worksheet_before.write_column('A1', beforedrops)
    worksheet_after.write_column('A1', afterdrops)