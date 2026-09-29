
import numpy 

from get_exercise_block import get_exercise_block
from get_result import get_result


def collect_population_results(sub_dataframes, exercises, exercise):
    results_collection1 = {}
    results_collection2 = {}
    
    for subno in sub_dataframes.keys():
        df = get_exercise_block(sub_dataframes[subno], exercise)
        
        results = get_result(exercise, df)

        raven_extra_info = []
        
        if(results==[] or (results[0][0]==100 and (len(results)==1 or len(results)==2)) or results[0][0]<0):
            continue
            
        if(exercise=='Raven Score'):
            raven_extra_info.append('R_A: ' + str(results[1][0])) # raven age
            raven_extra_info.append('T_A: ' + str(results[2][0])) # true age
            raven_extra_info.append('C_S: ' + str(results[3][0])) # correct score
            results_collection1[subno] = results[0][0]
            
        elif(exercise=='Memory Short Audit Verb'):
            if( len(results) > 0 and results!=[[]]):
                if(len(results)==1):
                    if(df[0][2]==str(results[0][0])):
                        results_collection1[subno] = results[0][0]
                    elif(df[1][2]==str(results[0][0])):
                        results_collection2[subno] = results[0][0]
                elif(len(results)==2):
                    results_collection1[subno] = results[0][0]
                    results_collection2[subno] = results[1][0]
            
            
        elif(exercise=='Memory Work Audit Verb'):
            results_collection1[subno] = results[0][0]
           
            
        # elif(exercise=='Phonological Syllables'):
        #     given_answer = df.iloc[0].tolist()
        #     # i want only part 2 in syllabes, i ignore part 1, that's why i get only given_answer[5:]
        #     given_answer_pt2 = [int(x) for x in given_answer[5:]]
        #     results_collection1[subno] = sum(given_answer_pt2)
        
        # elif(exercise=='Phonological Phonemes'):
        #     results_new = results[0][1]
        #     results_collection1[subno] = results_new
            
        elif(exercise=='Decode Words Pseudo'):
            results_new_pt1 = results[0][0]
            results_new_pt2 = results[1][0]
            if(results_new_pt1!=-1):
                results_collection1[subno] = results_new_pt1
            if(results_new_pt2!=-1):
                results_collection2[subno] = results_new_pt2
            
        elif(exercise=='Visual Orthographic Rec'):
            results_new_pt1 = results[0][1]
            results_new_pt2 = results[1][1]   
            if(results_new_pt1!=-1 and df[0][0]!=100):
                results_collection1[subno] = results_new_pt1
            if(results_new_pt2!=-1 and df[exercises[exercise]][0]!=100):
                results_collection2[subno] = results_new_pt2
        else:
            results_new = results[0]
            results_collection1[subno] = sum(results_new)
        
            
                
    # print("exercise ", exercise, " results_collection1 = ", results_collection1)
    # print("exercise ", exercise, " results_collection2 = ", results_collection2)
    
    
    return results_collection1, results_collection2