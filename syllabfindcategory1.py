



def syllabfindcategory1(numbers, wordsinitialinfodict, wordsandroi):
    general_category1 = ['Φ', 'ΦΣ', 'ΣΦ', 'ΣΦΣ', 'ΦΦ', 'ΦΦΣ', 'ΣΦΦ', 'ΣΦΦΣ', 'ΣΦΦΦΣ']
    general_category2 = ['ΣΣΦ', 'ΣΣΦΣ', 'ΣΣΦΦΣ', 'ΣΣΦΦ']
    general_category3 = ['ΣΣΣΦ', 'ΣΣΣΦΣ', 'ΣΣΣΦΦ', 'ΣΣΣΦΦΣ']
    
    
    category3 = []
    category3_words = []
    for i in range(len(numbers)):
        if ( bool(set(general_category3) & set(wordsinitialinfodict[numbers[i]][1]))):
        # if( 'ΣΣΣΦ' in wordsinitialinfodict[numbers[i]][1]   or  'ΣΣΣΦΣ' in wordsinitialinfodict[numbers[i]][1] or 'ΣΣΣΦΦ' in wordsinitialinfodict[numbers[i]][1] or 'ΣΣΣΦΦΣ' in wordsinitialinfodict[numbers[i]][1] ):
            category3.append( numbers[i] )
            category3_words.append( wordsandroi[numbers[i]] )
            

    category2 = []
    category2_words = []
    for i in range(len(numbers)):
        # if( ('ΣΣΦ' in wordsinitialinfodict[numbers[i]][1]    or  'ΣΣΦΣ' in wordsinitialinfodict[numbers[i]][1]    or   'ΣΣΦΦΣ' in wordsinitialinfodict[numbers[i]][1]   or    'ΣΣΦΦ' in wordsinitialinfodict[numbers[i]][1])   and   (not ('ΣΣΣΦ' in wordsinitialinfodict[numbers[i]][1]   or  'ΣΣΣΦΣ' in wordsinitialinfodict[numbers[i]][1]    or    'ΣΣΣΦΦ' in wordsinitialinfodict[numbers[i]][1]     or    'ΣΣΣΦΦΣ' in wordsinitialinfodict[numbers[i]][1]) )  ):
        if ( bool(set(general_category2) & set(wordsinitialinfodict[numbers[i]][1])) and not bool(set(general_category3) & set(wordsinitialinfodict[numbers[i]][1]))):
            category2.append( numbers[i] )
            category2_words.append( wordsandroi[numbers[i]] )
            
            
    category1 = []
    category1_words = []
    for i in range(len(numbers)):
        # if( ('Φ' in wordsinitialinfodict[numbers[i]][1]    or   'ΦΣ' in wordsinitialinfodict[numbers[i]][1]   or    'ΣΦ' in wordsinitialinfodict[numbers[i]][1]   or  'ΣΦΣ' in wordsinitialinfodict[numbers[i]][1]   or  'ΦΦ' in wordsinitialinfodict[numbers[i]][1]   or   'ΦΦΣ' in wordsinitialinfodict[numbers[i]][1]   or  'ΣΦΦ' in wordsinitialinfodict[numbers[i]][1]   or  'ΣΦΦΣ' in wordsinitialinfodict[numbers[i]][1])   and   (not ('ΣΣΣΦ' in wordsinitialinfodict[numbers[i]][1]   or  'ΣΣΣΦΣ' in wordsinitialinfodict[numbers[i]][1]   or    'ΣΣΣΦΦ' in wordsinitialinfodict[numbers[i]][1]    or    'ΣΣΣΦΦΣ' in wordsinitialinfodict[numbers[i]][1]  or 'ΣΣΦ' in wordsinitialinfodict[numbers[i]][1]  or 'ΣΣΦΣ' in wordsinitialinfodict[numbers[i]][1]   or   'ΣΣΦΦΣ' in wordsinitialinfodict[numbers[i]][1]    or    'ΣΣΦΦ' in wordsinitialinfodict[numbers[i]][1]) )   ):
        if ( bool(set(general_category1) & set(wordsinitialinfodict[numbers[i]][1])) and not bool(set(general_category3) & set(wordsinitialinfodict[numbers[i]][1])) and not bool(set(general_category2) & set(wordsinitialinfodict[numbers[i]][1]))):
            category1.append( numbers[i] )
            category1_words.append( wordsandroi[numbers[i]] )
    
    
    category4 = []
    category4_words = []
    for i in range(len(numbers)):
        if(  (numbers[i] not in category1) and ( numbers[i] not in category2)  and  (numbers[i] not in category3)):
            category4.append( numbers[i] )
            category4_words.append( wordsandroi[numbers[i]] )
            if( len(numbers) == len(wordsinitialinfodict)):
                print("\nWord = ", wordsandroi[numbers[i]], "with roino = ",  numbers[i], "is not in any category as the syllabes of it are = ", wordsinitialinfodict[numbers[i]][1] , "\n")
            
    
    return category1, category1_words, category2, category2_words, category3, category3_words, category4, category4_words
