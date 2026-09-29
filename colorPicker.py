


def colorPicker(indexes, lines):
    # # # # redefine the color that i will paint each cut i've made
    if( len(indexes)%lines == 0 ):
        mycolor = "aqua"
    if( len(indexes) == 1 ): # To prwto kopsimo den thelw na exei xroma
        mycolor = None
    if( len(indexes)!=1 and len(indexes)%lines == 1 ):
        mycolor = "fuchsia"
    if( len(indexes)%lines == 2 ):
        mycolor = "darkorange"
    if( len(indexes)%lines == 3 ):
        mycolor = "lime"
    if( len(indexes)%lines == 4 ):
        mycolor = "mediumorchid"
    if( len(indexes)%lines == 5 ):
        mycolor = "crimson"
    if( len(indexes)%lines == 6 ):   # change 29/11/2014, it was ==7, i.e the number =6 wasn't exist
        mycolor = "fuchsia"
    if( len(indexes)%lines == 7 ):     # change 29/11/2014, it was ==7
        mycolor = "goldenrod"
    if( len(indexes)%lines == 8 ):     # change 29/11/2014, it was ==7
        mycolor = "green"
    if( len(indexes)%lines == 9 ):     # change 29/11/2014, it was ==7
        mycolor = "brown"
    if( len(indexes)%lines == 10 ):    
        mycolor = "navy"
    if( len(indexes)%lines == 11 ):    
        mycolor = "olive"
    if( len(indexes)%lines == 12 ):     
        mycolor = "teal"
    if( len(indexes)%lines == 13 ):     
        mycolor = "maroon"
    if( len(indexes)%lines == 14 ):    
        mycolor = "purple"
    # # # # #
    
    return mycolor