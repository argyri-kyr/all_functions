

import xlsxwriter
from asyncio.windows_events import NULL
import calendar
import time


from a_grade import a_grade
from b_grade import b_grade
from c_grade import c_grade
from d_grade import d_grade
from e_grade import e_grade
from f_grade import f_grade
from ek import ek
from ec import ec
from indicator import indicator


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import folder1, folder2
from GetSomeInitialData import getGazesFoldersandClass



def main():
    # subs = [13170]
    subs = [subno for subno in range(13001, 13276)]

    timestamp = calendar.timegm(time.gmtime())

    missingsubpath = folder1 + 'not_scored_subs_' + str(timestamp) + '.xlsx'
    missingsubsworkbook = xlsxwriter.Workbook(missingsubpath)
    missingsubsworksheet = missingsubsworkbook.add_worksheet() 
    misscount = 0

    fullsubpath = folder1 + 'scored_subs_' + str(timestamp) + '.xlsx'
    fullsubsworkbook = xlsxwriter.Workbook(fullsubpath)
    fullsubsworksheet = fullsubsworkbook.add_worksheet() 
    fullcount = 0


    score1path = folder1 + 'score1.xlsx'
    score1workbook = xlsxwriter.Workbook(score1path)
    score1worksheet = score1workbook.add_worksheet() 

    score2path = folder1 + 'score2.xlsx'
    score2workbook = xlsxwriter.Workbook(score2path)
    score2worksheet = score2workbook.add_worksheet() 

    score3path = folder1 + 'score3.xlsx'
    score3workbook = xlsxwriter.Workbook(score3path)
    score3worksheet = score3workbook.add_worksheet() 

    score4path = folder1 + 'score4.xlsx'
    score4workbook = xlsxwriter.Workbook(score4path)
    score4worksheet = score4workbook.add_worksheet() 

    score5path = folder1 + 'score5.xlsx'
    score5workbook = xlsxwriter.Workbook(score5path)
    score5worksheet = score5workbook.add_worksheet() 


    separatexlsxpath = folder1 + 'testa_scores_per_exercise.xlsx'
    sepworkbook = xlsxwriter.Workbook(separatexlsxpath)
    sepworksheet = sepworkbook.add_worksheet() 
    
    scorecounter = 0


    for sub in subs:
        search1 = getGazesFoldersandClass(sub)   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/

        if( search1 == NULL ):
            print("Subject= ", sub, "doesn't exist")
            continue
        print("Sub = ", sub)
        # first scores
        a1_score, a2_score = a_grade(sub)
        b1_score, b2_score = b_grade(sub)
        c_score = c_grade(sub)
        d1_score, d2_score = d_grade(sub)
        e1_score, e2_score = e_grade(sub)
        f_score = f_grade(sub)

        if( a1_score==-1 or b1_score==-1 or c_score==-1 or d1_score==-1 or e1_score==-1 or f_score==-1 ):
            print("Missing Answers.xlsx or other data from one or more parts of testa. Check your data. So sub = ", sub, "can't have a score")
            if( a1_score==-1 and b1_score==-1 and c_score==-1 and d1_score==-1 and e1_score==-1 and f_score==-1 ):
                continue
            else:
                missingsubsworksheet.write(misscount, 0, sub)
                misscount+=1
                continue

        scorelist = [a1_score+a2_score+b1_score, c_score, b2_score+d1_score+d2_score+e1_score, e2_score+f_score]

        
        # find ek(ekatostimorio) according to these scores
        eklist = ek(sub, scorelist)

        # find ec(equivalent class) according to these scores
        eclist = ec(sub, scorelist)

        # find indicator according to these scores
        final_indicator, ek_mean = indicator(sub, eklist)

        xlsxpath = folder1 + folder2 + 'subject_' + str(sub) + '/testa_score.xlsx'
        workbook = xlsxwriter.Workbook(xlsxpath)
        worksheet = workbook.add_worksheet() 
        worksheet.write_row(0, 0, scorelist)
        worksheet.write_row(1, 0, eklist)
        worksheet.write_row(2, 0, eclist)
        worksheet.write(3, 0, ek_mean)
        worksheet.write(4, 0, final_indicator)
        workbook.close()

        score1worksheet.write_row(scorecounter, 0, scorelist)
        score2worksheet.write_row(scorecounter, 0, eklist)
        score3worksheet.write_row(scorecounter, 0, eclist)
        score4worksheet.write(scorecounter, 0, ek_mean)
        score5worksheet.write(scorecounter, 0, final_indicator)
        sepworksheet.write_row(scorecounter, 0, [a1_score, a2_score, b1_score, b2_score, c_score, d1_score, d2_score, e1_score, e2_score, f_score])

        scorecounter += 1


        fullsubsworksheet.write(fullcount, 0, sub)
        fullcount += 1
        


    missingsubsworkbook.close()
    fullsubsworkbook.close()

    score1workbook.close()
    score2workbook.close()
    score3workbook.close()
    score4workbook.close()
    score5workbook.close()
    sepworkbook.close()


main()