




from asyncio.windows_events import NULL
import xlsxwriter
import os
import time

from globalVars import folder1
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass


def testaparta_scoring():
    from_runcrashes = False 

    subs = [subno for subno in range(13001, 13276)]
    # subs = [13260]

    testaparteanswerspath = folder1 + 'testaparta_answers.xlsx'
    workbook = xlsxwriter.Workbook(testaparteanswerspath)
    
    worksheet = workbook.add_worksheet()
    subjectno_col = 0
    ex1_cor_col = 1
    ex1_error_col = 2
    ex1_scoring_col = 3
    ex2_cor_col = 4
    ex2_error_col = 5
    ex2_scoring_col = 6


    worksheet.write(0, 0, "ID")
    worksheet.write(0, 1, "EXERCISE_A1 CORRECTS")
    worksheet.write(0, 2, "EXERCISE_A1 ERRORS")
    worksheet.write(0, 3, "EXERCISE_A1 SCORING")
    worksheet.write(0, 4, "EXERCISE_A2 CORRECTS")
    worksheet.write(0, 5, "EXERCISE_A2 ERRORS")
    worksheet.write(0, 6, "EXERCISE_A2 SCORING")
    
    countsubs = 0

    for sub1 in subs:
        print("\nSub = ", sub1)

        # # # Clear  variables # # #
        answerspath = ''
        totalanswers = []

        # # # end of clear # # #

        
        # # # # # # # # # # # # # #  Check if cbma, cbmb, cbmc exists, in order to start main process  # # # # # # # # # # # # # #

        search1 = getGazesFoldersandClass(sub1)
        
        if( search1 != NULL ): # # if subject exists 
            
            search1 = getGazesFoldersandClass(sub1)
            gazesfolders, sub1class, subexam = search1[0], search1[1], search1[2]
            text = 'testaparta'
            file1 = getGazesFolderbyText(sub1, subexam, text, gazesfolders, sub1class, from_runcrashes)


            if( file1!=NULL ):
                countsubs += 1

                # # # # Read & Collect data for all parts # # # #

                answerspath = folder1 + 'subject_' + str(sub1) + "/" + file1 + '/testa.txt'
                
                if( os.path.exists(answerspath) ):
                    subsfile = open(answerspath , 'r')
                    Lines = subsfile.readlines()
                    
                    for line in Lines:
                        if( line.strip() ):
                            s = [ int(x) for x in line.strip().split(" ") ]
                            totalanswers.append(s)
                
                # Handle Case: testa.txt doesn't exist
                else:
                    countsubs -= 1
                    continue
                
                # print("Total Answers = ", totalanswers)

                # # # #  End-of read & collect data # # # #



                # # # # # # # First Statistics # # # # # #

                # Check only Second Exercise, because in first exercise the score will occure immediately from count ones and zeros from each child's answer
                                        
                
                total_correct_ex1 = totalanswers[0].count(1)
                total_errors_ex1 = totalanswers[0].count(0)

                total_correct_ex2 = totalanswers[1].count(1)
                total_errors_ex2 = totalanswers[1].count(0)



                # # # # # # Write first statistic results into excel # # # # # #
             
                worksheet.write(countsubs, subjectno_col, sub1)
                worksheet.write(countsubs, ex1_cor_col, total_correct_ex1)
                worksheet.write(countsubs, ex1_error_col, total_errors_ex1)
                worksheet.write(countsubs, ex1_scoring_col, total_correct_ex1 - total_errors_ex1)
                worksheet.write(countsubs, ex2_cor_col, total_correct_ex2)
                worksheet.write(countsubs, ex2_error_col, total_errors_ex2)
                worksheet.write(countsubs, ex2_scoring_col, total_correct_ex2 - total_errors_ex2)
              
                # # # # # # End of write first statistic results into excel # # # # # #


    workbook.close()

testaparta_scoring()
