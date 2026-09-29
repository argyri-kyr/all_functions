

import math


def calculate_stats(subno, class_mapping, target_class, exercises, exercise, results_collection1, results_collection2):
    stat_list = []
    
    greek_target_class = class_mapping[target_class]
    
    # Define total number for PART 1
    if(subno in results_collection1.keys()):
        if(exercise=='Memory Short Audit Verb'):
                total_number = exercises[exercise][1]
        else:
                total_number = exercises[exercise]
    
    if(subno in results_collection1.keys()):
        subno_score = results_collection1[subno]
        
        if(subno_score==total_number):
            greater_score_list = [x for x in results_collection1.values() if x==subno_score]
            compared_score = subno_score
        else:
            greater_score_list = [x for x in results_collection1.values() if x>subno_score]
            compared_score = subno_score + 1
            
        stat_score = math.floor( ( len(greater_score_list) / len(results_collection1.values()) ) * 100 )
        
        if(exercise=='Raven Score'):
            stat = 'Το ' + str(stat_score) + '% των μαθητών της ' + str(greek_target_class) + ' έχουν σκορ μεγαλύτερο ή ίσο του ' + str(compared_score) + '.'
        
        elif(exercise=='Decode Words Pseudo'):
            if(compared_score==total_number):
                stat = 'Το ' + str(stat_score) + '% των μαθητών της ' + str(greek_target_class) + ' απάντησε σωστά σε ' + str(compared_score) + ' από τις ' + str(total_number) + ' λέξεις.'
            else:
                stat = 'Το ' + str(stat_score) + '% των μαθητών της ' + str(greek_target_class) + ' απάντησε σωστά σε ' + str(compared_score) + ' ή περισσότερες από τις ' + str(total_number) + ' λέξεις.'
        
        else:          
            if(compared_score==total_number):
                stat = 'Το ' + str(stat_score) + '% των μαθητών της ' + str(greek_target_class) + ' απάντησε σωστά σε ' + str(compared_score) + ' από τις ' + str(total_number) + ' ερωτήσεις.'
            else:
                stat = 'Το ' + str(stat_score) + '% των μαθητών της ' + str(greek_target_class) + ' απάντησε σωστά σε ' + str(compared_score) + ' ή περισσότερες από τις ' + str(total_number) + ' ερωτήσεις.'
        
        stat_list.append(stat)
    

    # Define total number for PART 2
    if(subno in results_collection2.keys()):
        if(exercise=='Memory Short Audit Verb'):
                total_number = exercises[exercise][2]
        else:
                total_number = exercises[exercise]

    
    if(subno in results_collection2.keys()):
        subno_score = results_collection2[subno]
        
        if(subno_score==total_number):
            greater_score_list = [x for x in results_collection2.values() if x==subno_score]
            compared_score = subno_score
        else:
            greater_score_list = [x for x in results_collection2.values() if x>subno_score]
            compared_score = subno_score + 1
        
        stat_score = math.floor( ( len(greater_score_list) / len(results_collection2.values()) ) * 100 )
        
        if(exercise=='Decode Words Pseudo'):
            if(compared_score==total_number):
                stat = 'Το ' + str(stat_score) + '% των μαθητών της ' + str(greek_target_class) + ' απάντησε σωστά σε ' + str(compared_score) + ' από τις ' + str(total_number) + ' λέξεις.'
            else:
                stat = 'Το ' + str(stat_score) + '% των μαθητών της ' + str(greek_target_class) + ' απάντησε σωστά σε ' + str(compared_score) + ' ή περισσότερες από τις ' + str(total_number) + ' λέξεις.'
        else:          
            if(compared_score==total_number):
                stat = 'Το ' + str(stat_score) + '% των μαθητών της ' + str(greek_target_class) + ' απάντησε σωστά σε ' + str(compared_score) + ' από τις ' + str(total_number) + ' ερωτήσεις.'
            else:
                stat = 'Το ' + str(stat_score) + '% των μαθητών της ' + str(greek_target_class) + ' απάντησε σωστά σε ' + str(compared_score) + ' ή περισσότερες από τις ' + str(total_number) + ' ερωτήσεις.'
            
        stat_list.append(stat)
        
        
    return stat_list