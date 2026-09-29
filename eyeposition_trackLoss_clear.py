


def eyeposition_trackLoss_sideclear(vergenceindex, vergenceleft, vergenceright):
    remove_number = 5
    
    removed_indexes = []
    for i in range(len(vergenceleft)):
        if(vergenceleft[i]==0 or vergenceright[i]==0):
            # afairw  "5"  prin
            tempindex = i
            while( tempindex>=0 and abs(tempindex-i)<=remove_number ):
                removed_indexes.append(vergenceindex[tempindex])
                tempindex-=1
            
            #afairw  "5"  meta
            tempindex = i+1
            while( tempindex<len(vergenceindex) and abs(tempindex-i)<=remove_number ):
                removed_indexes.append(vergenceindex[tempindex])
                tempindex+=1

    
    vergenceleft_clean = []
    vergenceright_clean = []
    for i in range(len(vergenceleft)):
        if( vergenceindex[i] in removed_indexes ):
            vergenceleft_clean.append( None )
            vergenceright_clean.append( None )
        else:
            vergenceleft_clean.append( vergenceleft[i] )
            vergenceright_clean.append( vergenceright[i] )


    # vergenceleft_nozeros = []
    # vergenceright_nozeros = []
    # for i in range(len(vergencedata1)):
    #     if( vergencedata1[i]!=0 and vergencedata2[i]!=0 ):
    #         vergenceleft_nozeros.append(vergencedata1[i])
    #         vergenceright_nozeros.append(vergencedata2[i])
    #     elif( vergencedata1[i]==0 or vergencedata2[i]==0 ):
    #         vergenceleft_nozeros.append(None)
    #         vergenceright_nozeros.append(None)
    
    return vergenceleft_clean, vergenceright_clean



def eyeposition_trackLoss_bothclear(vergenceindex, vergenceleftx, vergencerightx, vergencelefty, vergencerighty, vergenceleftvalid, vergencerightvalid):
    remove_number = 5
    
    only_track_loss = []
    removed_indexes = []
    for i in range(len(vergenceindex)):
        if( vergenceleftvalid[i]==0 or vergencerightvalid[i]==0  ):    # if( vergenceleftx[i]==0 or vergencerightx[i]==0 or vergencelefty[i]==0 or vergencerighty[i]==0 ):
            only_track_loss.append(vergenceindex[i])
            
            # afairw  "5"  prin
            tempindex = i
            while( tempindex>=0 and abs(tempindex-i)<=remove_number ):
                removed_indexes.append(vergenceindex[tempindex])
                tempindex-=1
            
            #afairw  "5"  meta
            tempindex = i+1
            while( tempindex<len(vergenceindex) and abs(tempindex-i)<=remove_number ):
                removed_indexes.append(vergenceindex[tempindex])
                tempindex+=1

           
           
    vergenceleftx_clean = []
    vergencerightx_clean = []
    vergencelefty_clean = []
    vergencerighty_clean = []
    for i in range(len(vergenceindex)):
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
            
            
            
    # vergenceleftx_nozeros = []
    # vergencerightx_nozeros = []
    # vergencelefty_nozeros = []
    # vergencerighty_nozeros = []
    
    # for i in range(len(vergenceleftx)):
        
    #     if( vergenceleftx[i]!=0 and vergencerightx[i]!=0 and vergencelefty[i]!=0 and vergencerighty[i]!=0 ):
    #         vergenceleftx_nozeros.append(vergenceleftx[i])
    #         vergencerightx_nozeros.append(vergencerightx[i])
    #         vergencelefty_nozeros.append(vergencelefty[i])
    #         vergencerighty_nozeros.append(vergencerighty[i])
            
    #     else:
    #         vergenceleftx_nozeros.append(None)
    #         vergencerightx_nozeros.append(None)
    #         vergencelefty_nozeros.append(None)
    #         vergencerighty_nozeros.append(None)
    
    return vergenceleftx_clean, vergencerightx_clean, vergencelefty_clean, vergencerighty_clean, only_track_loss