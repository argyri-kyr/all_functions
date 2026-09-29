



def syllabtotalno(wordsyllabnumber):
    unique_values = list(set(wordsyllabnumber))
    occurences = {}
    for element in unique_values:
        occurences[element] = wordsyllabnumber.count(element)
    
    return occurences