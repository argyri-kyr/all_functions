



def syllabfindcategory2(numbers, wordsinitialinfodict, wordsandroi):
    general_category1 = 0
    general_category2 = 2
    general_category3 = 3
    
    
    category1 = []
    category1_words = []
    for i in range(len(numbers)):
       if ( general_category1 == wordsinitialinfodict[numbers[i]][1] ): 
            category1.append( numbers[i] )
            category1_words.append( wordsandroi[numbers[i]] )
  


    category2 = []
    category2_words = []
    for i in range(len(numbers)):
        if ( general_category2 == wordsinitialinfodict[numbers[i]][1] ):
            category2.append( numbers[i] )
            category2_words.append( wordsandroi[numbers[i]] )
            

    category3 = []
    category3_words = []
    for i in range(len(numbers)):
        if ( general_category3 == wordsinitialinfodict[numbers[i]][1] ):
            category3.append( numbers[i] )
            category3_words.append( wordsandroi[numbers[i]] )
    
    
    
    category4 = []
    category4_words = []
    for i in range(len(numbers)):
        if(  (numbers[i] not in category1) and ( numbers[i] not in category2)  and  (numbers[i] not in category3)):
            category4.append( numbers[i] )
            category4_words.append( wordsandroi[numbers[i]] )
            if( len(numbers) == len(wordsinitialinfodict)):
                print("\nWord = ", wordsandroi[numbers[i]], "with roino = ",  numbers[i], "is not in any category as the syllabes of it are = ", wordsinitialinfodict[numbers[i]][1] , "\n")
            
    
    return category1, category1_words, category2, category2_words, category3, category3_words, category4, category4_words
