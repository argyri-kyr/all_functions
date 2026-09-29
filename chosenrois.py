

def chosenrois(chosenline, lastlinewords):
    chosenroislist = []

    if( chosenline > 1 ):
        chosenroislist += [x for x in range(lastlinewords[chosenline-2]+1, lastlinewords[chosenline-1]+1)]
    
    elif( chosenline == 1 ):
        chosenroislist += [x for x in range(1, lastlinewords[chosenline-1]+1)]

    return chosenroislist