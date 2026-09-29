


from asyncio.windows_events import NULL


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2


def gazeshandling(file, sub1, filtered_flag):
    
    newgazes = []
    vergence = []
    vergence_z = []


    if( filtered_flag == 1 ):
        print('\nAttention: filter flag enabled. Loading gazes from gazes_filtered.txt!\n')
        gazesfilteredfilepath = folder1 + folder2 + 'subject_' + str(sub1) + '/' + file + '/gazes_filtered.txt' 
        gazesfilteredfile = open(gazesfilteredfilepath,"r")
        lines = gazesfilteredfile.readlines()
        return gazesfilteredfile, lines, newgazes, vergence, vergence_z
         

    gazesfilepath = folder1 + folder2 + 'subject_' + str(sub1) + '/' + file + '/gazes.txt' 
    gazesfile = open(gazesfilepath,"r")
    lines = gazesfile.readlines()
    for p in lines:
        size = len( p.split(None) )
        break


    if( size < 7 ):
        print('\nAttention: Loading OLD TYPE gazes from gazes-orignal-1920.txt!\n')
        gazesfilepath = folder1 + folder2 + 'subject_' + str(sub1) + '/' + file + '/gazes-orignal-1920.txt' 
        if not os.path.exists( gazesfilepath ):
            print('File gazes-orignal-1920.txt not found. Loading OLD TYPE gazes from gazes.txt!\n')
            gazesfilepath = folder1 + folder2 + 'subject_' + str(sub1) + '/' + file + '/gazes.txt' 
        
        gazesfile = open(gazesfilepath,"r")
        lines = gazesfile.readlines()
        return gazesfile, lines, newgazes, vergence, vergence_z
    
    else:
        print('\nAttention: new GAZES file found!\n')

        gazespyfilepath = folder1 + folder2 + 'subject_' + str(sub1) + '/' + file + '/gazespy.txt' 
        gazespyfile = open(gazespyfilepath, 'w')
    
        # # # # # # # # # # # # # # # # # # # # # #  NEW GAZES FILE HANDLING  # # # # # # # # # # # # # # # # # # # # # #

        AA = []
                      
        leftxvar = []
        leftyvar = []
        leftvalid = []

        rightxvar = []
        rightyvar = []
        rightvalid = []

        tvar = []

        pupilsizeleft = []
        pupilsizeright = []

        vergenceleftz = []
        vergencerightz = []

        # Here I will load all gazes data into the lists I made before
        for p in lines:
            AA.append( int(p.split(None)[0]) ) 

            leftxvar.append( int(p.split(None)[1]) )                   
            leftyvar.append( int(p.split(None)[2]) )
            leftvalid.append( int(p.split(None)[4]) )

            rightxvar.append( int(p.split(None)[5]) )                   
            rightyvar.append( int(p.split(None)[6]) )
            rightvalid.append( int(p.split(None)[8]) )            
            
            tvar.append( float(p.split(None)[9]) )

            pupilsizeleft.append( float(p.split(None)[10]) )
            pupilsizeright.append( float(p.split(None)[12]) )

            vergenceleftz.append( float(p.split(None)[3]) )
            vergencerightz.append( float(p.split(None)[7]) )

        
        gazesfile.close()


        for i in range(len(leftxvar)):
            # If --both-- eyes are valid
            if( leftvalid[i]==1 and rightvalid[i]==1 and leftxvar[i]>0 and leftyvar[i]>0 and rightxvar[i]>0 and rightyvar[i]>0 ):
                newgazes.append( [ AA[i], (leftxvar[i] + rightxvar[i])/2, (leftyvar[i] + rightyvar[i])/2, tvar[i], leftvalid[i] ] )

                vergence.append( [ AA[i], leftxvar[i], leftyvar[i], rightxvar[i], rightyvar[i], tvar[i], leftvalid[i], pupilsizeleft[i], pupilsizeright[i] ] )
                vergence_z.append( [ vergenceleftz[i], vergencerightz[i] ] )
            
            # If I have an invalid eye
            else:
                # I have to set it like that because otherwise it will give me "0" on AA column and I would miss the page start 
                newgazes.append( [ AA[i], 0, 0, tvar[i], -1 ] )

                vergence.append( [ AA[i], 0, 0, 0, 0, tvar[i], 0 , -1, -1 ] ) # Same as above
                vergence_z.append( [0, 0] )


        # # write gazespy.txt
        for i in range(len(newgazes)-1):
            gazespyfile.write( str(newgazes[i][0]) + "\t" + str(newgazes[i][1]) + "\t" + str(newgazes[i][2]) + "\t" + str(newgazes[i][3]) + "\t" + str(newgazes[i][4]) + "\n" )
        
        gazespyfile.write( str(newgazes[-1][0]) + "\t" + str(newgazes[-1][1]) + "\t" + str(newgazes[-1][2]) + "\t" + str(newgazes[-1][3]) + "\t" + str(newgazes[-1][4]) )
        gazespyfile.close()
        # # 

        if(newgazes!=NULL):
            gazesfilepath = gazespyfilepath
            gazesfile = open(gazesfilepath,"r")
            lines = gazesfile.readlines()


        return gazesfile, lines, newgazes, vergence, vergence_z

