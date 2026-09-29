


import os, sys


from plottestattention import plottestattention_fun




#################################################
# INSTALL FFMPEG FIRST
"""
    You need to install ffmpeg first follow the instructions
    from extra_libraries folder.

"""
##################################################




def plottestattention_main():
    
    filefound = False
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    fixationspagetxt_final = script_directory + '\\fixationspy1.txt' 
        
    if( os.path.exists(fixationspagetxt_final) ):
        filefound = True

                        
    if( filefound==True ):
        # # # # # # collect vergence data  # # # # # # #
        fixationfilepath = open(fixationspagetxt_final, 'r')
        lines = fixationfilepath.readlines()
        fixationx = []
        fixationy = []
        fixationduration = []
        for p in lines:
            fixationx.append( int(p.split(None)[1]) ) 
            fixationy.append( float(p.split(None)[2]) ) 
            fixationduration.append( float(p.split(None)[4]) ) 


        # # # # # # # # # # # # #  end of collect data  # # # # # # # # # # # # #

        # # # # # # # # # # # # # # # #   PLOT EYE FIXATIONS   # # # # # # # # # # # # # # # #    
        plottestattention_fun(fixationx, fixationy, fixationduration)
    
    else:
        print("\n\nNo fixations.txt found")

            






plottestattention_main()
