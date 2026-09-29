

import sys

from get_exercise_block import get_exercise_block


def define_answers(subno, sub_dataframes, exercises, exercise, results_collection1, results_collection2):
    answer_list_final = []
    
    if(exercise=='Phonological Rhymes'):
        if(subno in results_collection1.keys()):
            answer_dict = {'Σωστό': [], 'Λάθος': []}
            
            test_dataframe = {'σήματα': ['τραπέζι', 'κύματα', 'φτερό', 'τοίχος'],
                            'οθόνη': ['μεγαλώνει', 'ανθίζει', 'μαραίνεται', 'χρωματίζει'],
                            'βελόνα': ['μπαλόνι', 'εικόνα', 'ακόμα', 'καρύδι'],
                            'χτύπος': ['όροφος', 'ύπνος', 'μύλος', 'κήπος'],
                            'γάτα': ['πάντα', 'ψάθα', 'πιάτα', 'κάπα'],
                            'στολίδι': ['βαρίδι', 'ρεβίθι', 'πατίνι', 'μολύβι'],
                            'γρανάζι': ['φαράσι', 'καράβι', 'χαλάζι', 'σκοτάδι'],
                            'χωράφι': ['κομμάτια', 'χωράφια', 'τμήματα', 'εδάφη'],
                            'σκουπίδι': ['πάρκο', 'σπίτι', 'ταξίδι', 'σκουπιδιού'],
                            'σχολείο': ['σχολάω', 'διαλύω', 'κοιτάω', 'δυσκολία']}
            test_dataframe_list_keys = list(test_dataframe.keys())
            test_dataframe_list_values = list(test_dataframe.values())
            
            test_correct = ['κύματα', 'μεγαλώνει', 'εικόνα', 'κήπος', 'πιάτα', 'βαρίδι', 'χαλάζι', 'εδάφη', 'ταξίδι', 'διαλύω']
            
            df = get_exercise_block(sub_dataframes[subno], exercise)
            
            given_answers = [0 if x == 'ΔΑ' else int(x) for x in df.iloc[0, :]]
            
            for ans in range(len(given_answers)):
                is_correct = ''
                if(given_answers[ans]==0):
                    is_correct = 'Λάθος'
                    reply = 'ΔΑ'
                elif test_dataframe_list_values[ans][given_answers[ans]-1]==test_correct[ans]:
                    is_correct = 'Σωστό'
                    reply = test_dataframe_list_values[ans][given_answers[ans]-1]
                else:
                    is_correct = 'Λάθος'
                    reply = test_dataframe_list_values[ans][given_answers[ans]-1]
                
                distractor = ''
                if(is_correct=='Λάθος'):
                    if(test_dataframe_list_keys[ans]=='χωράφι'):
                        if(reply=='χωράφια'):
                            distractor = '  (distractor)'
                    if(test_dataframe_list_keys[ans]=='σκουπίδι'):
                        if(reply=='σκουπιδιού'):
                            distractor = '  (distractor)'
                    if(test_dataframe_list_keys[ans]=='σχολείο'):
                        if(reply=='σχολάω'):
                            distractor = '  (distractor)'
                
                answer_dict[is_correct].append(test_dataframe_list_keys[ans] +  ' ⟶ ' + reply + distractor)
        
            answer_list_final.append(answer_dict)   
            
            
    elif(exercise=='Decode Words Pseudo'):
        if subno in sub_dataframes:
            df = get_exercise_block(sub_dataframes[subno], exercise)
   
            # Real Words
            if(subno in results_collection1.keys()):
                if('?' in df.iloc[:, 0].tolist()):
                    print("\n\n '?' exist in Decode Words Pseudo, make corrections at first and then re-run the analysis.\n")
                    # sys.exit()
                    return
                answer_dict_1 = {'Παρατονισμός': [], 'Λάθος': []}
                given_answers_realwords_number = [2 if x == 'T' else int(x) for x in df.iloc[:, 0]]
                given_answers_realwords_string = [x for x in df.iloc[:, 3]]
                
                for ans in range(len(given_answers_realwords_number)):
                    if given_answers_realwords_number[ans] == 2:
                        answer_dict_1['Παρατονισμός'].append(given_answers_realwords_string[ans])
                    elif given_answers_realwords_number[ans] == 0:
                        answer_dict_1['Λάθος'].append(given_answers_realwords_string[ans])
                        
                answer_list_final.append(answer_dict_1)
            else:
                answer_list_final.append({})
            
            # Pseudo Words
            if(subno in results_collection2.keys()):
                if('?' in df.iloc[:, 1].tolist()):
                    print("\n\n '?' exist in Decode Words Pseudo, make corrections at first and then re-run the analysis.\n")
                    # sys.exit()
                    return
                answer_dict_2 = {'Παρατονισμός': [], 'Λάθος': []}
                given_answers_pseudowords_number = [2 if x == 'T' else int(x) for x in df.iloc[:, 1]]
                given_answers_pseudowords_string = [x for x in df.iloc[:, 4]]
                
                for ans in range(len(given_answers_pseudowords_number)):
                    if(given_answers_pseudowords_number[ans]==2):
                        answer_dict_2['Παρατονισμός'].append(given_answers_pseudowords_string[ans])
                    elif(given_answers_pseudowords_number[ans]==0):
                        answer_dict_2['Λάθος'].append(given_answers_pseudowords_string[ans])
    
                
                answer_list_final.append(answer_dict_2)
            else:
                answer_list_final.append({})
        
        
    elif(exercise=='Visual Orthographic Rec'):
        if subno in sub_dataframes:
            df = get_exercise_block(sub_dataframes[subno], exercise)
            
            # Visual Recognition
            if(subno in results_collection1.keys()):
                answer_dict1 = {'Σωστό': [], 'Λάθος': []}
                given_answers1 = [int(x) for x in df.iloc[1,:exercises[exercise]]]
                
                test_dataframe1 = {'τετράδιο': ['τερτάδιο', 'τετράδιο', 'τετρόδιο', 'τρετάδιο', 'τεδράδιο'],
                                'διάρκεια': ['διάκρεια', 'διόρκεια', 'δριάκεια', 'βιάρκεια', 'διάρκεια'],
                                'θόρυβος': ['φόρυβος', 'θόρυβος', 'θόρυδος', 'βόρυθος', 'θόροβυς'],
                                'γιορτή': ['γορτή', 'γιοτρή', 'χιορτή', 'γιορτή', 'γιορπή'],
                                'άνθρωπος': ['άνρθρωπος', 'άνθρωτος', 'άνρθωπος', 'άνφρωπος', 'άνθρωπος'],
                                'έπρεπε': ['έπρ3πε', 'έρπεπε', 'έπερπε', 'έπρειπε', 'έπρεπε'],
                                'μυρμήγκι': ['μυρμρήγκι', 'μυρμήκι', 'μυρμήγκι', 'μυμρήγκι', 'μρυμήγκι'],
                                'θέατρο': ['θέαρτο', 'θάετρο', 'θέαπρο', 'θέατρο', 'φέατρο'],
                                'πράγματα': ['πράχματα', 'πάργματα', 'πράγμαπα', 'πράμγατα', 'πράγματα'],
                                'σύμφωνα': ['σύφμωνα', 'σύμφανα', 'σύμθωνα', 'σύμφωνα', 'σύφωνα']}
                test_dataframe1_list_keys = list(test_dataframe1.keys())
                test_dataframe1_list_values = list(test_dataframe1.values())
                
                for ans in range(len(given_answers1)):
                    is_correct = ''
                    if test_dataframe1_list_values[ans][given_answers1[ans]-1] == test_dataframe1_list_keys[ans]:
                        is_correct = 'Σωστό'
                    else:
                        is_correct = 'Λάθος'
                        
                    reply = test_dataframe1_list_values[ans][given_answers1[ans]-1]
                    answer_dict1[is_correct].append(test_dataframe1_list_keys[ans] +  ' ⟶ ' + reply)
                
                answer_list_final.append(answer_dict1)
            else:
                answer_list_final.append({})
            
            # Visual Recognition
            if(subno in results_collection2.keys()):
                answer_dict2 = {'Σωστό': [], 'Λάθος': []}
                given_answers2 = [int(x) for x in df.iloc[1,exercises[exercise]:]]        

                test_dataframe2 = {'είναι': ['είνε', 'ίναι', 'είναι', 'ειναί', 'ήναι'],
                                'ήλιος': ['ηλίος', 'ήλιος', 'ήληος', 'ήλλιος', 'ήλιως'],
                                'διάβασε': ['διάβασε', 'διαβάσε', 'δειάβασε', 'διάβασαι', 'δυάβασε'],
                                'παιχνίδι': ['παιχνήδι', 'πεχνίδι', 'παίχνιδι', 'παιχνίδη', 'παιχνίδι'],
                                'γλώσσα': ['γλωσσά', 'γλόσα', 'γλώσα', 'γλώσσα', 'γλόσσα'],
                                'γειτονιά': ['γιτονιά', 'γειτόνια', 'γειτονιά', 'γειτωνιά', 'γειτονειά'],
                                'εικόνα': ['ικόνα', 'εικώνα', 'οικόνα', 'εικονά', 'εικόνα'],
                                'χωριό': ['χοριό', 'χωριό', 'χωριώ', 'χωρειό', 'χώριο'],
                                'ταξίδι': ['ταξίδοι', 'ταξίδη', 'ταξίδι', 'ταξιδί', 'ταξήδι'],
                                'τέσσερα': ['τεσσέρα', 'τέσσερα', 'τέσερα', 'ταίσσερα', 'τέσσαιρα']}
                test_dataframe2_list_keys = list(test_dataframe2.keys())
                test_dataframe2_list_values = list(test_dataframe2.values())

                for ans in range(len(given_answers2)):
                    is_correct = ''
                    if test_dataframe2_list_values[ans][given_answers2[ans]-1] == test_dataframe2_list_keys[ans]:
                        is_correct = 'Σωστό'
                    else:
                        is_correct = 'Λάθος'
                        
                    reply = test_dataframe2_list_values[ans][given_answers2[ans]-1]
                    answer_dict2[is_correct].append(test_dataframe2_list_keys[ans] +  ' ⟶ ' + reply)
                
                answer_list_final.append(answer_dict2)
            else:
                answer_list_final.append({})

    elif(exercise=='Decode Sentences'):
        if(subno in results_collection1.keys()):
            answer_dict = {'Σωστό': [], 'Λάθος': []}
            
            test_dataframe = {'έτρεξε': ['έκρυψε', 'έτρεξε', 'φοβήθηκε'],
                            'έπιασε': ['πέταξε', 'έχασε', 'έπιασε'],
                            'σταματά': ['ξεκινά', 'σταματά', 'φεύγει'],
                            'απογοητεύτηκαν': ['απογοητεύτηκαν', 'ενθουσιάστηκαν', 'θύμωσαν'],
                            'παρέλειψε': ['συνέχισε', 'διάβασε', 'παρέλειψε'],
                            'μεγάλωναν': ['λιγόστευαν', 'έσβηναν', 'μεγάλωναν'],
                            'απέτυχε': ['απέτυχε', 'θριάμβευσε', 'χαλάρωσε'],
                            'διέφυγε': ['παραθέρισε', 'διέφυγε', 'φυλακίστηκε'],
                            'προβλέπει': ['ακυρώνει', 'απορρίπτει', 'προβλέπει'],
                            'υιοθετήσουν': ['υιοθετήσουν', 'αμφισβητήσουν', 'αγνοήσουν']}
            test_dataframe_list_keys = list(test_dataframe.keys())
            test_dataframe_list_values = list(test_dataframe.values())
            
            test_correct = ['έτρεξε', 'έπιασε', 'σταματά', 'απογοητεύτηκαν', 'παρέλειψε', 'μεγάλωναν', 'απέτυχε', 'διέφυγε', 'προβλέπει', 'υιοθετήσουν']
            
            df = get_exercise_block(sub_dataframes[subno], exercise)
            
            given_answers = [0 if x == 'ΔΑ' else int(x) for x in df.iloc[0, :]]
            
            for ans in range(len(given_answers)):
                is_correct = ''
                if(given_answers[ans]==0):
                    is_correct = 'Λάθος'
                    reply = 'ΔΑ'
                elif test_dataframe_list_values[ans][given_answers[ans]-1]==test_correct[ans]:
                    is_correct = 'Σωστό'
                    reply = test_dataframe_list_values[ans][given_answers[ans]-1]
                else:
                    is_correct = 'Λάθος'
                    reply = test_dataframe_list_values[ans][given_answers[ans]-1]

            
                answer_dict[is_correct].append(test_dataframe_list_keys[ans] +  ' ⟶ ' + reply)
        
            answer_list_final.append(answer_dict)

    else:
        answer_list_final.append({})
        if(exercise=='Memory Short Audit Verb'):
            answer_list_final.append({})
                
            
    return answer_list_final