


from asyncio.windows_events import NULL
import xlsxwriter
import os


from globalVars import folder1
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass


def radar_scoring():
    from_runcrashes = False 

    subs = [subno for subno in range(13001, 13276)]
    # subs = [13014]


    radaranswerspath = folder1 + 'radar_answers.xlsx'
    workbook = xlsxwriter.Workbook(radaranswerspath)
    worksheet = workbook.add_worksheet()
    subjectno_col = 0
    visit_cor_col = 1
    visit_error_col = 2
    zoo_cor_col = 3
    zoo_error_col = 4
    zebra_cor_col = 5
    zebra_error_col = 6
    average_subtr = 7
    
    worksheet.write(0, 0, "ID")
    worksheet.write(0, 1, "VISIT CORRECTS")
    worksheet.write(0, 2, "VISIT ERRORS")
    worksheet.write(0, 3, "ZOO CORRECTS")
    worksheet.write(0, 4, "ZOO ERRORS")
    worksheet.write(0, 5, "ZEBRA CORRECTS")
    worksheet.write(0, 6, "ZEBRA ERRORS")
    worksheet.write(0, 7, "SCORING")


    countsubs = 0

    for sub1 in subs:
        print("\nSub = ", sub1)

        total_questions = 7

        # # # Clear  variables # # #
        visitpath = ''
        ansvisit = []

        zoopath = ''
        anszoo = []

        zebrapath = ''
        anszebra = []

        # # # end of clear # # #

        
        # # # # # # # # # # # # # #  Check if cbma, cbmb, cbmc exists, in order to start main process  # # # # # # # # # # # # # #

        search1 = getGazesFoldersandClass(sub1)
        
        if( search1 != NULL ): # # if subject exists 
            
            gazesfolders, sub1class, subexam = search1[0], search1[1], search1[2]

            text = 'visit'
            file1 = getGazesFolderbyText(sub1, subexam, text, gazesfolders, sub1class, from_runcrashes)
        
            text = 'zoo'
            file2 = getGazesFolderbyText(sub1, subexam, text, gazesfolders, sub1class, from_runcrashes)

            text = 'zebra'
            file3 = getGazesFolderbyText(sub1, subexam, text, gazesfolders, sub1class, from_runcrashes)


            if( file1!=NULL or file2!=NULL or file3!=NULL ):
                countsubs += 1

                # # # # Read & Collect data for all parts # # # #

                if(file1!=NULL):
                    visitpath = folder1 + 'subject_' + str(sub1) + "/" + file1 + '/Answers.txt'
                if(file2!=NULL):
                    zoopath = folder1 + 'subject_' + str(sub1) + "/" + file2 + '/Answers.txt'
                if(file3!=NULL):
                    zebrapath = folder1 + 'subject_' + str(sub1) + "/" + file3 + '/Answers.txt'

                

                # for visit
                if(file1!=NULL and os.path.exists(visitpath)):
                    subsfile = open(visitpath , 'r', encoding="utf8")
                    Lines = subsfile.readlines()

                    for line in Lines:
                        if(line.strip()):
                            s = line.strip()
                    ansvisit.append( int(s))
                
                # for zoo
                if( file2!=NULL and os.path.exists(zoopath)):
                    subsfile = open(zoopath , 'r', encoding="utf8")
                    Lines = subsfile.readlines()

                    for line in Lines:
                        if(line.strip()):
                            s = line.strip()
                    anszoo.append( int(s) )

                # for zebra
                if(file3!=NULL and os.path.exists(zebrapath)):
                    subsfile = open(zebrapath , 'r', encoding="utf8")
                    Lines = subsfile.readlines()

                    for line in Lines:
                        if(line.strip()):
                            s = line.strip()
                    anszebra.append( int(s))

                # # # #  End-of read & collect data # # # #



                # # Handle Case: One of the files doesn't exist # #
                if( (file1==NULL) or (file1!=NULL and not os.path.exists(visitpath)) ):
                    ansvisit = [-1]
                
                if( (file2==NULL) or (file2!=NULL and not os.path.exists(zoopath)) ):
                    anszoo = [-1]
                
                if( (file3==NULL) or (file3!=NULL and not os.path.exists(zebrapath)) ):
                    anszebra = [-1]

                # # End of Handle Case # #


                # print("ansvisit = ", ansvisit)
                # print("anszoo = ", anszoo)
                # print("anszebra = ", anszebra)

                # # # # # End of Collect Data # # # # #



                # # # # # # # First Statistics # # # # # #

                # visit
                if( ansvisit[0] >= 0 ):
                    total_correct_visit = ansvisit[0]
                    total_errors_visit = total_questions - total_correct_visit
                else:
                    total_correct_visit = 0
                    total_errors_visit = 0
                # print("Visit Correct = ", total_correct_visit)
                # print("Visit Errors = ", total_errors_visit)


                # zoo 
                if( anszoo[0] >= 0 ):
                    total_correct_zoo = anszoo[0]
                    total_errors_zoo = total_questions - total_correct_zoo
                else:
                    total_correct_zoo = 0
                    total_errors_zoo = 0                
                # print("Zoo Correct = ", total_correct_zoo)
                # print("Zoo Errors = ", total_errors_zoo)


                # zebra
                if( anszebra[0] >= 0 ):
                    total_correct_zebra = anszebra[0]
                    total_errors_zebra = total_questions - total_correct_zebra
                else:
                    total_correct_zebra = 0
                    total_errors_zebra = 0                
                # print("Zebra Correct = ", total_correct_zebra)
                # print("Zebra Errors = ", total_errors_zebra)


                # Average
                correct_average = (total_correct_visit + total_correct_zoo + total_correct_zebra) / 3
                errors_average = (total_errors_visit + total_errors_zoo + total_errors_zebra) / 3

                score = correct_average - errors_average
                # print("Mean(correct) - Mean(errors) = ", avg_subtr)

                # # # # # # End of first-statistics # # # # # 



                # # # # # # Write first statistic results into excel # # # # # #
                if( os.path.exists(visitpath) and os.path.exists(zoopath) and os.path.exists(zebrapath) ):
                    worksheet.write(countsubs, subjectno_col, sub1)
                    worksheet.write(countsubs, visit_cor_col, total_correct_visit)
                    worksheet.write(countsubs, visit_error_col, total_errors_visit)
                    worksheet.write(countsubs, zoo_cor_col, total_correct_zoo)
                    worksheet.write(countsubs, zoo_error_col, total_errors_zoo)
                    worksheet.write(countsubs, zebra_cor_col, total_correct_zebra)
                    worksheet.write(countsubs, zebra_error_col, total_errors_zebra)
                    worksheet.write(countsubs, average_subtr, score)
                else:
                    countsubs -= 1
                # # # # # # End of write first statistic results into excel # # # # # #


    workbook.close()

radar_scoring()