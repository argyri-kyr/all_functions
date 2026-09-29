


from asyncio.windows_events import NULL
import xlsxwriter
import os


from globalVars import folder1
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass


def cbm_scoring():
    from_runcrashes = False 

    subs = [subno for subno in range(13001, 13276)]
    countsubs = 0
    # subs = [13020]

    compared_index = 2

    parta_cor = [2, 1, 1, 3, 2, 3, 3, 2, 3, 1, 3, 3, 1, 3, 2, 2, 1, 1]
    partb_cor = [1, 3, 1, 1, 3, 2, 1, 3, 3, 1, 2, 2, 1, 3, 2, 1, 3, 1, 3, 1, 3, 1, 1, 2]
    partc_cor = [2, 1, 2, 2, 1, 3, 1, 1, 2, 2, 2, 1, 3, 2, 1, 1, 3, 1, 2, 1, 3, 1, 1, 3]

    cbmanswerspath = folder1 + 'cbm_scoring_compared_index' + str(compared_index+1) + '.xlsx'
    workbook = xlsxwriter.Workbook(cbmanswerspath)
    worksheet = workbook.add_worksheet()
    subjectno_col = 0
    if(compared_index==0):
        parta_cor_col = 1
        parta_error_col = 2
        partb_cor_col = 3
        partb_error_col = 4
        partc_cor_col = 5
        partc_error_col = 6
        average_subtr = 7

        worksheet.write(countsubs, subjectno_col, "ID")
        worksheet.write(countsubs, parta_cor_col, "PART A CORRECTS")
        worksheet.write(countsubs, parta_error_col, "PART A ERRORS")
        worksheet.write(countsubs, partb_cor_col, "PART B CORRECTS")
        worksheet.write(countsubs, partb_error_col, "PART B ERRORS")
        worksheet.write(countsubs, partc_cor_col, "PART C CORRECTS")
        worksheet.write(countsubs, partc_error_col, "PART C ERRORS")
        worksheet.write(countsubs, average_subtr, "DIFF")
    else:
        partb_cor_col = 1
        partb_error_col = 2
        partc_cor_col = 3
        partc_error_col = 4
        average_subtr = 5   

        worksheet.write(countsubs, subjectno_col, "ID")
        worksheet.write(countsubs, partb_cor_col, "PART B CORRECTS")
        worksheet.write(countsubs, partb_error_col, "PART B ERRORS")
        worksheet.write(countsubs, partc_cor_col, "PART C CORRECTS")
        worksheet.write(countsubs, partc_error_col, "PART C ERRORS")
        worksheet.write(countsubs, average_subtr, "DIFF")     



    for sub1 in subs:
        print("\nSub = ", sub1)

        # # # Clear  variables # # #
        subspatha = ''
        answersa = []
        checka = []

        subspathb = ''
        answersb = []
        checkb = []

        subspathc = ''
        answersc = []
        checkc = []
        # # # end of clear # # #

        
        # # # # # # # # # # # # # #  Check if cbma, cbmb, cbmc exists, in order to start main process  # # # # # # # # # # # # # #

        search1 = getGazesFoldersandClass(sub1)
        
        if( search1 != NULL ): # # if subject exists 
            
            search1 = getGazesFoldersandClass(sub1)
            gazesfolders, sub1class, subexam = search1[0], search1[1], search1[2]
            text = 'cbmpartb'
            file1 = getGazesFolderbyText(sub1, subexam, text, gazesfolders, sub1class, from_runcrashes)


        
            search1 = getGazesFoldersandClass(sub1)
            gazesfolders, sub1class, subexam = search1[0], search1[1], search1[2]
            text = 'cbmpartc'
            file2 = getGazesFolderbyText(sub1, subexam, text, gazesfolders, sub1class, from_runcrashes)


            if( file1!=NULL or file2!=NULL ):
                countsubs += 1

                # # # # Read & Collect data for all parts # # # #

                if(file1!=NULL):
                    subspatha = folder1 + 'subject_' + str(sub1) + "/" + file1 + '/cbma.txt'
                    subspathb = folder1 + 'subject_' + str(sub1) + "/" + file1 + '/cbm.txt'
                if(file2!=NULL):
                    subspathc = folder1 + 'subject_' + str(sub1) + "/" + file2 + '/cbm.txt'
                

                # for cbm A
                if(file1!=NULL and os.path.exists(subspatha)):
                    subsfile = open(subspatha , 'r')
                    partAlines = subsfile.readlines()
                    
                    for line in partAlines:
                        if(line.strip()):
                            s = [ int(x) for x in line.strip().split(" ") ]
                            answersa.append(s)
                

                # for cbm B
                if( file1!=NULL and os.path.exists(subspathb)):
                    subsfile = open(subspathb , 'r')
                    partBlines = subsfile.readlines()

                    for line in partBlines:
                        if(line.strip()):
                            s = [ int(x) for x in line.strip().split(" ") ]
                            answersb.append(s)
                            

                # for cbm C
                if(file2!=NULL and os.path.exists(subspathc)):
                    subsfile = open(subspathc , 'r')
                    partClines = subsfile.readlines()

                    for line in partClines:
                        if(line.strip()):
                            s = [ int(x) for x in line.strip().split(" ")]
                            answersc.append(s)

                # # # #  End-of read & collect data # # # #



                # # Handle Case: One of the files doesn't exist # #
                
                if( (file1==NULL) or (file1!=NULL and not os.path.exists(subspatha)) ):
                    answersa = [[0]]
                
                if( (file1==NULL) or (file1!=NULL and not os.path.exists(subspathb)) ):
                    answersb = [[0],[0],[0]]
                
                if( file2==NULL or (file2!=NULL and not os.path.exists(subspathc)) ):
                    answersc = [[0],[0],[0]]
                

                if(compared_index==1):
                    if( len(answersb)<=1 ):
                        answersb = [[0],[0],[0]]
                    if( len(answersc)<=1 ):
                        answersc = [[0],[0],[0]]      
                
                if(compared_index==2):
                    if(len(answersb)<=2):
                        answersb = [[0],[0],[0]]
                    if(len(answersc)<=2):
                        answersc = [[0],[0],[0]]   

                # # End of Handle Case # #


                # print("answersa = ", answersa)
                # print("answersb = ", answersb)
                # print("answersc = ", answersc)

                # # # # # End of Collect Data # # # # #



                # # # # # # # First Statistics # # # # # #

                # cbmA 
                if( compared_index==0 ):
                    checka = []
                    for i in range(len(answersa[compared_index])):
                        if(answersa[compared_index][i]==parta_cor[i]):
                            checka.append(1)
                        elif( answersa[compared_index][i]!=parta_cor[i] and answersa[compared_index][i]>0 ):
                            checka.append(0)
                        else:  # # # if there is'nt any answer/there is no file for this part at all
                            checka.append(-1)
                    
                    total_correct_parta = checka.count(1)
                    total_errors_parta = checka.count(0)
                    # print("Part_A Correct = ", total_correct_parta)
                    # print("Part_A Errors = ", total_errors_parta)


                # cbmB 
                checkb = []
                for i in range(len(answersb[compared_index])):
                    if(answersb[compared_index][i]==partb_cor[i]):
                        checkb.append(1)
                    elif( answersb[compared_index][i]!=partb_cor[i] and answersb[compared_index][i]>0 ):
                        checkb.append(0)
                    else:
                        checkb.append(-1)
                
                total_correct_partb = checkb.count(1)
                total_errors_partb = checkb.count(0)
                # print("Part_B Correct = ", total_correct_partb)
                # print("Part_B Errors = ", total_errors_partb)


                # cbmC
                checkc = []
                for i in range(len(answersc[compared_index])):
                    if(answersc[compared_index][i]==partc_cor[i]):
                        checkc.append(1)
                    elif( answersc[compared_index][i]!=partc_cor[i] and answersc[compared_index][i]>0 ):
                        checkc.append(0)
                    else:
                        checkc.append(-1)
                
                total_correct_partc = checkc.count(1)
                total_errors_partc = checkc.count(0)
                # print("Part_C Correct = ", total_correct_partc)
                # print("Part_C Errors = ", total_errors_partc)


                # Average
                if( compared_index==0 ):
                    correct_average = (total_correct_parta + total_correct_partb + total_correct_partc) / 3
                    errors_average = (total_errors_parta + total_errors_partb + total_errors_partc) / 3

                    score = correct_average - errors_average
                else:
                    correct_average = (total_correct_partb + total_correct_partc) / 2
                    errors_average = (total_errors_partb + total_errors_partc) / 2

                    score = correct_average - errors_average                    
                # print("Mean(correct) - Mean(errors) = ", avg_subtr)

                # # # # # # End of first-statistics # # # # # 



                # # # # # # Write first statistic results into excel # # # # # #
                if( os.path.exists(subspatha) or os.path.exists(subspathb) or os.path.exists(subspathc) ):
                    worksheet.write(countsubs, subjectno_col, sub1)
                    if(compared_index==0):
                        worksheet.write(countsubs, parta_cor_col, total_correct_parta)
                        worksheet.write(countsubs, parta_error_col, total_errors_parta)
                    worksheet.write(countsubs, partb_cor_col, total_correct_partb)
                    worksheet.write(countsubs, partb_error_col, total_errors_partb)
                    worksheet.write(countsubs, partc_cor_col, total_correct_partc)
                    worksheet.write(countsubs, partc_error_col, total_errors_partc)
                    worksheet.write(countsubs, average_subtr, score)
                else:
                    countsubs -= 1
                # # # # # # End of write first statistic results into excel # # # # # #


    workbook.close()

cbm_scoring()