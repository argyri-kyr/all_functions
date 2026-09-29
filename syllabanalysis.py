


from globalVars import folder1, folder2
from syllabfindcategory1 import syllabfindcategory1
from syllabfindcategory2 import syllabfindcategory2
from syllab_occ_roi_words import syllab_occ_roi_words
from syllabanalysisfortext1 import syllabanalysisfortext1
from syllabanalysisfortext2 import syllabanalysisfortext2
from syllabtotalno import syllabtotalno
from syllabanalysispercategory import syllabanalysispercategory
import sys

################################################
# eg> python syllabanalysis.py 1504 visit False 1  : for subject analysis
# eg> python syllabanalysis.py 1504 visit True  1  : for text analysis
################################################



def syllabanalysis():
    exam = 1

    # if( len(sys.argv) > 1 and  len(sys.argv) == 5 ):
    #     subs = [int(sys.argv[1])]
    #     texts = [sys.argv[2]]
    #     flagtext = sys.argv[3]
    #     analysischoice = int(sys.argv[4])

    # elif( len(sys.argv) > 1 and  len(sys.argv) != 5 ):
    #     print("\nInput data have to be like:\n\nsubgect_number(integer) \t text(string) \t flagtext(True/False) ")
    #     return
    # else:
    #     print("\nInput data have to be like:\n\nsubgect_number(integer) \t text(string) \t flagtext(True/False) ")
    #     return 
    
    # if( flagtext == 'False' ):
    #     flagtext = False
    # elif( flagtext == 'True' ):
    #     flagtext = True
    
  ###################################################################################################
    subs = [1704]                                                                                   #
    texts = ['visit', 'zoo']                                                                            #
    # texts = ['efeyreseis', 'island', 'morning', 'olympia', 'psaras', 'visit', 'zebra', 'zoo']     #
    flagtext = False                                                                                 #
    analysischoice = 1                                                                       #
  # #################################################################################################
    
    for text in texts:
        print(text)
            
        if( analysischoice == 1 ):
            words, wordsroi, wordsandroi, wordsyllabnumber, wordsyllab, wordsinitialinfodict = syllabanalysisfortext1(text)
            maxsyllabnumber = max(wordsyllabnumber)
        elif( analysischoice == 2 ):
            words, wordsroi, wordsandroi, wordsyllabnumber, wordsyllab, wordsinitialinfodict = syllabanalysisfortext2(text)
        
        syllaboccurences = syllabtotalno(wordsyllabnumber)
        
        for sub in subs:
            
            if( flagtext==False):
                reddweltimewordsdata = folder1 + folder2 + 'subject_' + str(sub) + '/all_data/' + text + str(exam) + '/notes/reddwelltimewords.txt'            
            else:
                reddweltimewordsdata = folder1 + 'texts/' + text + '_1920/reddweltimewords.txt'

            with open(reddweltimewordsdata, "r") as file:
                content = file.read()

            # Split the content by spaces and convert each token to an integer
            numbers = [int(num) for num in content.split()]

            results_occ, results_roi, results_words = syllab_occ_roi_words(numbers, wordsinitialinfodict, wordsandroi)  
            
            if( analysischoice == 1 ):
                category1_all, category1_words_all, category2_all, category2_words_all, category3_all, category3_words_all, category4_all, category4_words_all = syllabfindcategory1(numbers, wordsinitialinfodict, wordsandroi)
            elif( analysischoice == 2 ):
                category1_all, category1_words_all, category2_all, category2_words_all, category3_all, category3_words_all, category4_all, category4_words_all = syllabfindcategory2(numbers, wordsinitialinfodict, wordsandroi)
                
            syllabanalysispercategory(sub, text, exam, wordsinitialinfodict, wordsandroi, results_roi, syllaboccurences, flagtext, analysischoice)

        
    return
    



syllabanalysis()