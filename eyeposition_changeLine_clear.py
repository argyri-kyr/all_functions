

import xlsxwriter


from globalVars import folder1, folder2


def eyeposition_changeLine_clear(sub1, file, pageno, vergenceindex, vergenceleftx, vergencerightx, vergencelefty, vergencerighty, vergenceleftvalid, vergencerightvalid, finalindexes):
    remove_number = 15
    
    removed_indexes = []
    for i in range(len(vergenceindex)):
        for j in range(len(finalindexes)):
            if(finalindexes[j]==vergenceindex[i]):
                # afairw  "15"  prin
                tempindex = i
                while( tempindex>=0 and abs(tempindex-i)<=remove_number ):
                    removed_indexes.append(vergenceindex[tempindex])
                    tempindex-=1
                
                #afairw  "15"  meta
                tempindex = i+1
                while( tempindex<len(vergenceindex) and abs(tempindex-i)<=remove_number ):
                    removed_indexes.append(vergenceindex[tempindex])
                    tempindex+=1

                break
    
    
    vergenceleftx_clean = []
    vergencerightx_clean = []
    vergencelefty_clean = []
    vergencerighty_clean = []
    for i in range(len(vergenceleftx)):
        if( vergenceindex[i] in removed_indexes ):
            vergenceleftx_clean.append( None )
            vergencerightx_clean.append( None )
            vergencelefty_clean.append( None )
            vergencerighty_clean.append( None )
        else:
            vergenceleftx_clean.append( vergenceleftx[i] )
            vergencerightx_clean.append( vergencerightx[i] )
            vergencelefty_clean.append( vergencelefty[i] )
            vergencerighty_clean.append( vergencerighty[i] )
        
            
    # vergenceleftx = [vergenceleftx[i] for i in range(len(vergenceleftx)) if vergenceindex[i] not in removed_indexes]
    # vergencerightx = [vergencerightx[i] for i in range(len(vergencerightx)) if vergenceindex[i] not in removed_indexes]
    # vergencelefty = [vergencelefty[i] for i in range(len(vergencelefty)) if vergenceindex[i] not in removed_indexes]
    # vergencerighty = [vergencerighty[i] for i in range(len(vergencerighty)) if vergenceindex[i] not in removed_indexes]
    # vergenceindex = [vergenceindex[i] for i in range(len(vergenceindex)) if vergenceindex[i] not in removed_indexes]


    # disparitywb = xlsxwriter.Workbook(folder1 + folder2 + '/subject_' + str(sub1) + '/' + file + '/py/vergence_clear_page' + str(pageno) + '.xlsx')
    # disparitywsh = disparitywb.add_worksheet()
    # disparitywsh.write_column(0, 0, vergenceindex)
    # disparitywsh.write_column(0, 1, vergenceleftx_clean)
    # disparitywsh.write_column(0, 2, vergencelefty_clean)
    # disparitywsh.write_column(0, 3, vergencerightx_clean)
    # disparitywsh.write_column(0, 4, vergencerighty_clean)
    # disparitywb.close()
        
        
    return vergenceindex, vergenceleftx_clean, vergencerightx_clean ,vergencelefty_clean ,vergencerighty_clean, vergenceleftvalid, vergencerightvalid
                
                