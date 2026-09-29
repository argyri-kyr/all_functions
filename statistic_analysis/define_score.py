

from get_exercise_block import get_exercise_block


def define_score(subno, exercises, exercise, sub_dataframes, results_collection1, results_collection2):
    score_list = []
    
    if(subno in results_collection1.keys()):
        subno_score = results_collection1[subno]
        if(exercise=='Raven Score'):
            subno_score_sentence = 'To σκορ στο Raven είναι ' + str(subno_score) + '.'
        elif(exercise=='Decode Words Pseudo'):
            if(subno_score==exercises[exercise]):
                subno_score_sentence = 'Έγιναν σωστά ' + str(subno_score) + ' λέξεις.'
            else:
                subno_score_sentence = 'Έγιναν σωστά ' + str(subno_score) + ' από τις ' + str(exercises[exercise]) + ' λέξεις.'
        elif(exercise=='Memory Short Audit Verb'):
            df = get_exercise_block(sub_dataframes[subno], exercise)
            total_correct_ans = [3,4,4,5,5,6,7]
            given_total_correct_ans = df.iloc[-2][:exercises[exercise][0]].tolist()
            subno_score_sentence = ''
            for i in range(len(total_correct_ans)):
                if(i==1 or i==2):
                    if( (i==1 and given_total_correct_ans[i]<given_total_correct_ans[i+1]) or (i==2 and given_total_correct_ans[i]<=given_total_correct_ans[i-1]) ):
                        continue
                if(i==3 or i==4):
                    if( (i==3 and given_total_correct_ans[i]<given_total_correct_ans[i+1]) or (i==4 and given_total_correct_ans[i]<=given_total_correct_ans[i-1]) ):
                        continue
                subno_score_sentence +=  'Ανακάλεσε ' + str(given_total_correct_ans[i]) + ' από τα ' + str(total_correct_ans[i]) + ' στοιχεία.\n'
        elif(exercise=='Memory Work Audit Verb'):
            df = get_exercise_block(sub_dataframes[subno], exercise)
            total_correct_ans = [3,4,5,5,6,7,7]
            given_total_correct_ans = df.iloc[-2][:exercises[exercise]].tolist()
            inordered_totalcorrect = [int(x.split(',')[0]) for x in given_total_correct_ans]
            subno_score_sentence = ''
            for i in range(len(total_correct_ans)):
                if(i==2 or i==3):
                    if( (i==2 and inordered_totalcorrect[i]<inordered_totalcorrect[i+1]) or (i==3 and inordered_totalcorrect[i]<=inordered_totalcorrect[i-1]) ):
                        continue
                if(i==5 or i==6):
                    if( (i==5 and inordered_totalcorrect[i]<inordered_totalcorrect[i+1]) or (i==6 and inordered_totalcorrect[i]<=inordered_totalcorrect[i-1]) ):
                        continue
                subno_score_sentence +=  'Ανακάλεσε ' + str(inordered_totalcorrect[i]) + ' από τα ' + str(total_correct_ans[i]) + ' στοιχεία.\n'
        else:
            if(subno_score==exercises[exercise]):
                subno_score_sentence = 'Έγιναν σωστά ' + str(subno_score) + ' ερωτήσεις.'
            else:
                subno_score_sentence = 'Έγιναν σωστά ' + str(subno_score) + ' από τις ' + str(exercises[exercise]) + ' ερωτήσεις.'
        score_list.append(subno_score_sentence)
    
    
    if(subno in results_collection2.keys()):
        subno_score = results_collection2[subno]
        if(exercise=='Decode Words Pseudo'):
            if(subno_score==exercises[exercise]):
                subno_score_sentence = 'Έγιναν σωστά ' + str(subno_score) + ' λέξεις.'
            else:
                subno_score_sentence = 'Έγιναν σωστά ' + str(subno_score) + ' από τις ' + str(exercises[exercise]) + ' λέξεις.'
        elif(exercise=='Memory Short Audit Verb'):
            if(subno_score==exercises[exercise][2]):
                subno_score_sentence = 'Έγιναν σωστά ' + str(subno_score) + ' ερωτήσεις.'
            else:
                subno_score_sentence = 'Έγιναν σωστά ' + str(subno_score) + ' από τις ' + str(exercises[exercise][2]) + ' ερωτήσεις.'
        elif(exercise=='Memory Work Audit Verb'):
            df = get_exercise_block(sub_dataframes[subno], exercise)
            total_correct_ans = [3,4,5,5,6,7,7]
            given_total_correct_ans = df.iloc[-2][:exercises[exercise][0]].tolist()
            subno_score_sentence = ''
            for i in range(len(total_correct_ans)):
                if(i==2 or i==3):
                    if( (i==2 and given_total_correct_ans[i]<given_total_correct_ans[i+1]) or (i==3 and given_total_correct_ans[i]<=given_total_correct_ans[i-1]) ):
                        continue
                if(i==5 or i==6):
                    if( (i==5 and given_total_correct_ans[i]<given_total_correct_ans[i+1]) or (i==6 and given_total_correct_ans[i]<=given_total_correct_ans[i-1]) ):
                        continue
                subno_score_sentence +=  'Ανακάλεσε ' + str(given_total_correct_ans[i]) + ' από τα ' + str(total_correct_ans[i]) + ' στοιχεία.\n'
        else:
            if(subno_score==exercises[exercise]):
                subno_score_sentence = 'Έγιναν σωστά ' + str(subno_score) + ' ερωτήσεις.'
            else:
                subno_score_sentence = 'Έγιναν σωστά ' + str(subno_score) + ' από τις ' + str(exercises[exercise]) + ' ερωτήσεις.'
        score_list.append(subno_score_sentence)
    return score_list        