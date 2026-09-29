

import numpy as np

from get_exercise_block import get_exercise_block


def define_recommendation(subno, exercises, exercise, sub_dataframes, results_collection1, results_collection2):
    recommendation = []
    
    # Visual Orthographic Recognition
    if(exercise=='Visual Orthographic Rec'):
        # Visual Recognition
        if( subno in results_collection1.keys() ):
            if(results_collection1[subno]<7):
                recommendation.append('Χρειάζονται ασκήσεις στην Οπτική Αναγνώριση.')
            elif(results_collection1[subno]>=7 and results_collection1[subno]<9):
                recommendation.append('Προτείνονται ασκήσεις στην Οπτική Αναγνώριση.')
            else:
                recommendation.append('Η Οπτική Αναγνώριση είναι εντός τυπικών ορίων.')
                 
        # Visual Orthography
        if( subno in results_collection2.keys() ):
            if(results_collection2[subno]<6):
                recommendation.append('Χρειάζονται ασκήσεις στην Οπτική Ορθογραφία.')
            elif(results_collection2[subno]>=6 and results_collection2[subno]<9):
                recommendation.append('Προτείνονται ασκήσεις στην Οπτική Ορθογραφία.')
            else:
                recommendation.append('Η Οπτική Ορθογραφία είναι εντός τυπικών ορίων.')
            
    
    # Phonological Syllables
    elif(exercise=='Phonological Syllables'):
        if(subno in results_collection1.keys()):
            if(results_collection1[subno]<5):
                recommendation.append('Χρειάζονται ασκήσεις στην Αντικατάσταση Συλλαβών.')
            elif(results_collection1[subno]>=5 and results_collection1[subno]<8):
                recommendation.append('Προτείνονται ασκήσεις στην Αντικατάσταση Συλλαβών.')
            else:
                recommendation.append('Η Αντικατάσταση Συλλαβών είναι εντός τυπικών ορίων.')  
         
    # Phonological Phonemes
    elif(exercise=='Phonological Phonemes'):
        if(subno in results_collection1.keys()):
            if(results_collection1[subno]<4):
                recommendation.append('Χρειάζονται ασκήσεις στην Απαλοιφή Φωνήματος.')
            elif(results_collection1[subno]>=4 and results_collection1[subno]<6):
                recommendation.append('Προτείνονται ασκήσεις στην Απαλοιφή Φωνήματος.')
            else:
                recommendation.append('Η Απαλοιφή Φωνήματος είναι εντός τυπικών ορίων.')
    
    # Phonological Rhymes
    elif(exercise=='Phonological Rhymes'):
        if(subno in results_collection1.keys()):
            if(results_collection1[subno]<5):
                recommendation.append('Χρειάζονται ασκήσεις στις Ρίμες.')
            elif(results_collection1[subno]>=5 and results_collection1[subno]<8):
                recommendation.append('Προτείνονται ασκήσεις στις Ρίμες.')
            else:
                recommendation.append('Οι Ρίμες είναι εντός τυπικών ορίων.')
            
    # Decode Words Pseudo
    elif(exercise=='Decode Words Pseudo'):
        # Real Words
        if(subno in results_collection1.keys()):
            if(results_collection1[subno]<=17):
                recommendation.append('Χρειάζονται ασκήσεις στην Αποκωδικοποίηση Πραγματικών Λέξεων.')
            elif(results_collection1[subno]>17 and results_collection1[subno]<=21):
                recommendation.append('Προτείνονται ασκήσεις στην Αποκωδικοποίηση Πραγματικών Λέξεων.')
            else:
                recommendation.append('Η Αποκωδικοποίηση Πραγματικών Λέξεων είναι εντός τυπικών ορίων.')
        
        # Pseudo Words
        if( subno in results_collection2.keys() ):
            if(results_collection2[subno]<17):
                recommendation.append('Χρειάζονται ασκήσεις στην Αποκωδικοποίηση Ψευδο-Λέξεων.')
            elif(results_collection2[subno]>=17 and results_collection2[subno]<=19):
                recommendation.append('Προτείνονται ασκήσεις στην Αποκωδικοποίηση Ψευδο-Λέξεων.')
            else:
                recommendation.append('Η Αποκωδικοποίηση Ψευδο-Λέξεων είναι εντός τυπικών ορίων.')
        
       
    # Decode Sentences
    elif(exercise=='Decode Sentences'):
        if(subno in results_collection1.keys()):
            if(results_collection1[subno]<5):
                recommendation.append('Χρειάζονται ασκήσεις στην Κατανόηση Προτάσεων.')
            elif(results_collection1[subno]>=5 and results_collection1[subno]<8):
                recommendation.append('Προτείνονται ασκήσεις στην Κατανόηση Προτάσεων.')
            else:
                recommendation.append('Η Κατανόηση Προτάσεων είναι εντός τυπικών ορίων.')
    
    
    elif(exercise=='Raven Score'):
        if(subno in results_collection1.keys()):
            recommendation.append('Το αποτέλεσμα του τεστ RAVEN είναι ' + str(results_collection1[subno]) + '.')
    
    
    elif(exercise=='Memory Short Audit Verb'):
        if( subno in sub_dataframes ):
            df = get_exercise_block(sub_dataframes[subno], exercise)
            if(subno in results_collection1.keys()):
                if(results_collection1[subno]<4):
                    recommendation.append('Χρειάζονται ασκήσεις στην Βραχύχρονη Ακουστική Λεκτική Μνήμη.')
                else:
                    recommendation.append('Η Βραχύχρονη Ακουστική Λεκτική Μνήμη είναι εντός τυπικών ορίων.')
            
            if(subno in results_collection2.keys()): 
                results_new_pt2 = df.iloc[0, exercises[exercise][0]:exercises[exercise][0]+exercises[exercise][2]].tolist()
                sub_recommendation = ''
                plainpswords = [0,2,4,6,8]
                diffpswords = [1,3,5,7,9]
                plainpswords_score = sum(results_new_pt2[idx] for idx in plainpswords)
                diffpswords_score = sum(results_new_pt2[idx] for idx in diffpswords)
                if(plainpswords_score<3):
                    sub_recommendation += 'Χρειάζονται ασκήσεις σε Βραχύχρονη Ακουστική Φωνολογική Μνήμη σε λέξεις ΧΩΡΙΣ ιδιαίτερες φωνολογικές δυσκολίες.'
                else:
                    sub_recommendation += 'Δεν χρειάζονται ασκήσεις σε Βραχύχρονη Ακουστική Φωνολογική Μνήμη σε λέξεις ΧΩΡΙΣ ιδιαίτερες φωνολογικές δυσκολίες.'
                
                if(diffpswords_score<2):
                    sub_recommendation += '\n Χρειάζονται ασκήσεις σε Βραχύχρονη Ακουστική Φωνολογική Μνήμη σε λέξεις ΜΕ ιδιαίτερες φωνολογικές δυσκολίες.'
                else:
                    sub_recommendation += '\n Δεν χρειάζονται ασκήσεις σε Βραχύχρονη Ακουστική Φωνολογική Μνήμη σε λέξεις ΜΕ ιδιαίτερες φωνολογικές δυσκολίες.'
                    
                recommendation.append(sub_recommendation)
    
    
    elif(exercise=='Memory Work Audit Verb'):
        if( subno in sub_dataframes ):
            df = get_exercise_block(sub_dataframes[subno], exercise)
            numbervect_total = [3,4,5,5,6,7,7]
            if(subno in results_collection1.keys()):
                results_ordered = [int(x.split(',')[0]) for x in df.iloc[-2].tolist()]
                found_totalcorrect = [results_ordered[i] for i in range(len(results_ordered)) if results_ordered[i]==numbervect_total[i]]
                max_found_totalcorrect = np.max(found_totalcorrect, initial=0)
                if( len(found_totalcorrect)<=1 ):
                    recommendation.append('Δεν γίνεται αντιληπτή η έννοια της Διάταξης Αριθμών.')
                elif( len(found_totalcorrect)>=2 and max_found_totalcorrect<=4 ):
                    recommendation.append('Χρειάζονται ασκήσεις στην Εργαζόμενη Ακουστική Μνήμη.')
                elif( len(found_totalcorrect)>=2 and max_found_totalcorrect==5 ):
                    recommendation.append('Προτείνονται ασκήσεις στην Εργαζόμενη Ακουστική Μνήμη.')
                else:
                    recommendation.append('Η Εργαζόμενη Ακουστική Μνήμη είναι εντός τυπικών ορίων.')
            
            
    return recommendation
            
        