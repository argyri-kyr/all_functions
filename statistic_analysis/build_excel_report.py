


def build_excel_report_main(subno, exercise, workbook, results_collection1, results_collection2, figurepath1, figurepath2, score, recommendation, stat, answer):                 
    # BUILD EXCEL
    
    # SOME REFINEMENTS IF SOMETHING EMPTY
    if(recommendation==[]):
        recommendation.append('')
        # print("My recommendation is EMPTY for exercise = ", exercise)
    if(answer==[]):
        answer.append([])
        # print("My answer is EMPTY for exercise = ", exercise)
    if(score==[]):
        score.append('')
    
    sheet_name = exercise
    
    # BUILD SHEET PER EXERCISE
    if(exercise=='Memory Short Audit Verb'):
        if(subno in results_collection1.keys() and subno in results_collection2.keys()):
            if(subno in results_collection1.keys()):
                sheet_name = "Memory Words"
                build_exercise_sheet(workbook, sheet_name, exercise, figurepath1, score[0], recommendation[0], stat[0], answer[0])
            if(subno in results_collection2.keys()):
                sheet_name = "Memory Pseudo Words"
                build_exercise_sheet(workbook, sheet_name, exercise, figurepath2, score[1], recommendation[1], stat[1], answer[0])
        elif(subno in results_collection1.keys() or subno in results_collection2.keys()):
            if(subno in results_collection1.keys()):
                sheet_name = "Memory Words"
            if(subno in results_collection2.keys()):
                sheet_name = "Memory Pseudo Words"
            build_exercise_sheet(workbook, sheet_name, exercise, figurepath1, score[0], recommendation[0], stat[0], answer[0])

            
        
    elif(exercise=='Decode Words Pseudo'):
        if(subno in results_collection1.keys() and subno in results_collection2.keys()):
            if(subno in results_collection1.keys()):
                sheet_name = "Decode Real Words"
                build_exercise_sheet(workbook, sheet_name, exercise, figurepath1, score[0], recommendation[0], stat[0], answer[0])
            if(subno in results_collection2.keys()):
                sheet_name = "Decode Pseudo Words"
                build_exercise_sheet(workbook, sheet_name, exercise, figurepath2, score[1], recommendation[1], stat[1], answer[1])
        elif(subno in results_collection1.keys() or subno in results_collection2.keys()):
            if(subno in results_collection1.keys()):
                sheet_name = "Decode Real Words"
            if(subno in results_collection2.keys()):
                sheet_name = "Decode Pseudo Words"
            build_exercise_sheet(workbook, sheet_name, exercise, figurepath1, score[0], recommendation[0], stat[0], answer[0])
            
                
    elif(exercise=='Visual Orthographic Rec'):
        if(subno in results_collection1.keys() and subno in results_collection2.keys()):
            if(subno in results_collection1.keys()):
                sheet_name = "Visual Recognition"
                build_exercise_sheet(workbook, sheet_name, exercise, figurepath1, score[0], recommendation[0], stat[0], answer[0])
            if(subno in results_collection2.keys()):
                sheet_name = "Visual Orthography"
                build_exercise_sheet(workbook, sheet_name, exercise, figurepath2, score[1], recommendation[1], stat[1], answer[1])
        elif(subno in results_collection1.keys() or subno in results_collection2.keys()):
            if(subno in results_collection1.keys()):
                sheet_name = "Visual Recognition"
            if(subno in results_collection2.keys()):
                sheet_name = "Visual Orthography"
            build_exercise_sheet(workbook, sheet_name, exercise, figurepath1, score[0], recommendation[0], stat[0], answer[0])
        
    else:
        sheet_name = exercise
        if(subno in results_collection1.keys()):
            build_exercise_sheet(workbook, sheet_name, exercise, figurepath1, score[0], recommendation[0], stat[0], answer[0])

    return sheet_name
        


def build_exercise_sheet(workbook, sheet_name, exercise, figurepath, score, recommendation, stat, answer):
    sheet = workbook.add_worksheet(sheet_name)

    # formats
    wrap = workbook.add_format({'text_wrap': True, 'valign': 'top'})
    no_wrap = workbook.add_format({'text_wrap': False, 'valign': 'top'})

    row = 0

    # --- image file (NO WRAP in column A or B) ---
    if figurepath != '':
        sheet.write(row, 0, 'imageFile', no_wrap)
        sheet.write(row, 1, figurepath, no_wrap)
        row += 2
    
    # --- score ---
    if score !='':
        sheet.write(row, 0, 'score', no_wrap)
        if score.count('\n') > 0:
            scores = score.split('\n')
            sheet.write_column(row, 1, scores, wrap)
            row += len(scores) + 1
        else:
            sheet.write(row, 1, score, wrap)   # optional: wrap if long
            row += 2

    # --- recommendation (wrap ONLY column B) ---
    if recommendation != '':
        sheet.write(row, 0, 'recommendation', no_wrap)   # column A no wrap
        sheet.write(row, 1, recommendation, wrap)        # column B wrap

        n_lines = recommendation.count('\n') + 1
        sheet.set_row(row, 15 * n_lines)
        row += 2

    # --- stats (no wrap unless you want it) ---
    if stat != '':
        sheet.write(row, 0, 'stats', no_wrap)
        sheet.write(row, 1, stat, wrap)   # optional: wrap if long
        row += 2

    # --- answers ---
    if len(answer) > 0:
        for key, value in answer.items():
            sheet.write(row, 0, key, no_wrap)

            if (exercise=='Phonological Rhymes' or exercise=='Visual Orthographic Rec' or exercise=='Decode Words Pseudo'):
                sheet.write_column(row, 1, value, no_wrap)
                row += len(value) + 1
            else:
                sheet.write_row(row, 1, value, no_wrap)
                row += 2
        
        
