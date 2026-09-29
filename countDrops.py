

from globalVars import folder1, folder2, textends

def countDrops(sub1, exam, text, from_filename, worksheet):

    filepath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_data/' + text + str(exam) + '/' + from_filename + '_gap.txt'
    myfile = open(filepath, "r")

    filedata = []
    for line in myfile:
        filedata.append( [float(x) for x in line[:-1].split("\t")] )
    
    if(from_filename=='cutgazes'):
        validitycolumn = 4
    elif(from_filename=='fixations'):
        validitycolumn = 5

    wordnumberpath = folder1 + 'texts/' + text + textends + '/py/mytext/wordnumber.txt'
    wordnumberfile = open(wordnumberpath, "r")
    wordnumber = int(wordnumberfile.read())
    
    drops = [0 for i in range(wordnumber)]

    for i in range(len(filedata)):
        if( i>0 and filedata[i][validitycolumn]==-1 and filedata[i-1][validitycolumn]!=-1 ):
            prev_roi = int(filedata[i-1][validitycolumn])
            drops[prev_roi-1] += 1
    

    worksheet.write_column('A1', drops)

    return drops