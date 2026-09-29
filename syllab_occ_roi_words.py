



def syllab_occ_roi_words(numbers, wordsinitialinfodict, wordsandroi):
    results_occ = {}
    results_roi = {}
    results_words = {}
    for roino in range(len(numbers)):
        countwordsyllabes = wordsinitialinfodict[numbers[roino]][0]
        # antistoixizw th sillabi me ta occurences ths, dhladh poses x-sillabes lexeis exw, dhladh sillabi_number=4(tetrasillabes lexeis) exw sinolo 5 (occurenses=5)
        if( countwordsyllabes not in results_occ ):
            results_occ[countwordsyllabes] = 1
        else:
            results_occ[countwordsyllabes] += 1

        # antistoixizw th sillabi me to roi twn lexewn pou antapokrinontai se afth th sillabi, dhladh sillabi_number=4 exoun oi lexeis 1,2,5,180,....
        if( countwordsyllabes not in results_roi ):
            results_roi[countwordsyllabes] = [ numbers[roino] ]
        else:
            results_roi[countwordsyllabes].append( numbers[roino] ) 
        
        # antistoixizw th sillabi me tis lexeis pou antapokrinontai se afth th sillabi, dhladh sillabi_number=4 exoun oi lexeis pigainw, aderfi, bash, sintribani, .....
        if( countwordsyllabes not in results_words ):
            results_words[countwordsyllabes] = [ wordsandroi[numbers[roino]] ]
        else:
            results_words[countwordsyllabes].append( wordsandroi[numbers[roino]] )
    
    
    return results_occ, results_roi, results_words
    