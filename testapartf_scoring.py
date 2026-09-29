




from asyncio.windows_events import NULL
import xlsxwriter
import os
import time

from globalVars import folder1
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass


def testapartf_scoring():
    from_runcrashes = False 

    subs = [subno for subno in range(13001, 13276)]
    # subs = [13260]

    text1 = [4, 2, 4, 1, 1, 2, 3]
    text2 = [4, 2, 1, 1, 3, 2, 3]
    text3 = [4, 2, 4, 1, 3, 1, 3]

    testapartfanswerspath = folder1 + 'testapartf_answers.xlsx'
    workbook = xlsxwriter.Workbook(testapartfanswerspath)
    worksheet = workbook.add_worksheet()
    subjectno_col = 0
    text1_cor_col = 1
    text1_error_col = 2
    text2_cor_col = 3
    text2_error_col = 4
    text3_cor_col = 5
    text3_error_col = 6
    scoring_col = 7
    
    worksheet.write(0, 0, "ID")
    worksheet.write(0, 1, "TEXT1 CORRECTS")
    worksheet.write(0, 2, "TEXT1 ERRORS")
    worksheet.write(0, 3, "TEXT2 CORRECTS")
    worksheet.write(0, 4, "TEXT2 ERRORS")
    worksheet.write(0, 5, "TEXT3 CORRECTS")
    worksheet.write(0, 6, "TEXT3 ERRORS")
    worksheet.write(0, 7, "SCORING")


    countsubs = 0

    for sub1 in subs:
        print("\nSub = ", sub1)

        # # # Clear  variables # # #
        answerspath = ''
        totalanswers = []
        check1 = []
        check2 = []
        check3 = []

        # # # end of clear # # #

        
        # # # # # # # # # # # # # #  Check if cbma, cbmb, cbmc exists, in order to start main process  # # # # # # # # # # # # # #

        search1 = getGazesFoldersandClass(sub1)
        
        if( search1 != NULL ): # # if subject exists 
            
            search1 = getGazesFoldersandClass(sub1)
            gazesfolders, sub1class, subexam = search1[0], search1[1], search1[2]
            text = 'testapartf'
            file1 = getGazesFolderbyText(sub1, subexam, text, gazesfolders, sub1class, from_runcrashes)


            if( file1!=NULL ):
                countsubs += 1

                # # # # Read & Collect data for all parts # # # #

                answerspath = folder1 + 'subject_' + str(sub1) + "/" + file1 + '/Answers.txt'
                
                if( os.path.exists(answerspath) ):
                    subsfile = open(answerspath , 'r')
                    Lines = subsfile.readlines()
                    
                    for line in Lines:
                        if( line.strip() ):
                            s = [ int(x) for x in line.strip().split(" ") ]
                            totalanswers.append(s)
                
                
                # print("Total Answers = ", totalanswers)
                # # # #  End-of read & collect data # # # #


                # # Handle Case: Part TestapartF # #
                if( len(totalanswers)!=3 ):
                    print( "%d: part testapartf. \n" % sub1 )
                    time.sleep(5)
                    countsubs-=1
                    continue
                # # End of Handle Case # #



                # # # # # # # First Statistics # # # # # #

                # All Texts
                check1 = []
                check2 = []
                check3 = []
                for textno in range(len(totalanswers)):
                    if( textno == 0 ):
                        for j in range(len(totalanswers[textno])):
                            if( totalanswers[textno][j] == text1[j] ):
                                check1.append(1)
                            else:
                                check1.append(0)
                    if( textno == 1 ):
                        for j in range(len(totalanswers[textno])):
                            if( totalanswers[textno][j] == text2[j] ):
                                check2.append(1)
                            else:
                                check2.append(0)  
                    if( textno == 2 ):
                        for j in range(len(totalanswers[textno])):
                            if( totalanswers[textno][j] == text3[j] ):
                                check3.append(1)
                            else:
                                check3.append(0)                         
                
                total_correct_text1 = check1.count(1)
                total_errors_text1 = check1.count(0)

                total_correct_text2 = check2.count(1)
                total_errors_text2 = check2.count(0)

                total_correct_text3 = check3.count(1)
                total_errors_text3 = check3.count(0)



                # Average
                correct_average = (total_correct_text1 + total_correct_text2 + total_correct_text3) / 3
                errors_average = (total_errors_text1 + total_errors_text2 + total_errors_text3) / 3

                score = correct_average - errors_average
                # print("Mean(correct) - Mean(errors) = ", avg_subtr)

                # # # # # # End of first-statistics # # # # # 



                # # # # # # Write first statistic results into excel # # # # # #
             
                worksheet.write(countsubs, subjectno_col, sub1)
                worksheet.write(countsubs, text1_cor_col, total_correct_text1)
                worksheet.write(countsubs, text1_error_col, total_errors_text1)
                worksheet.write(countsubs, text2_cor_col, total_correct_text2)
                worksheet.write(countsubs, text2_error_col, total_errors_text2)
                worksheet.write(countsubs, text3_cor_col, total_correct_text3)
                worksheet.write(countsubs, text3_error_col, total_errors_text3)
                worksheet.write(countsubs, scoring_col, score)
              
                # # # # # # End of write first statistic results into excel # # # # # #


    workbook.close()

testapartf_scoring()
