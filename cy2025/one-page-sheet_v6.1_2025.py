import pandas as pd
import os
import math
from win32com import client as win32
import numpy as np
from spire.xls import *
from spire.xls.common import *
import openpyxl
from xlsx2html import xlsx2html
import pdfkit


#######################################
#
# This file is for Cyprus profile cards
#
########################################



# Function to extract specific cells from each sheet
def extract_from_sheet(main_folder, file_path, sheet_ranges, custom_headers, cell_positions, current_raven_DB_filename, start_date, subno, save_directory=None):
    # Load the Excel file
    xls = pd.ExcelFile(file_path)
    
    # Set up the writer and add the "ExecutiveSheet" sheet
    if not save_directory:
        save_directory = os.getcwd()
    output_path = os.path.join(save_directory, f"executive_sheet_{subno}.xlsx")
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        # Create the "ExecutiveSheet"
        workbook = writer.book
        executive_sheet = workbook.add_worksheet("ExecutiveSheet")
        
        # Define the format for center alignment
        center_format = workbook.add_format({
                        'align': 'center',
                        'valign': 'vcenter'
                    })
        
        # Set the page layout to landscape
        executive_sheet.set_landscape()
        # Fit to 3 pages height (vertical scaling) and 1 page width (horizontal scaling)
        executive_sheet.fit_to_pages(1, 3)
        # Set printing margins to narrow
        executive_sheet.set_margins(left=0.25, right=0.25, top=0.25, bottom=0.25)
        
        # Set the width of columns A, B, and C in "ExecutiveSheet"
        executive_sheet.set_column('D:D', 14.43)  # eg Set column A width to 20
        executive_sheet.set_column('G:G', 6)  # eg Set column A width to 20
        executive_sheet.set_column('H:G', 6)  # eg Set column A width to 20
        executive_sheet.set_column('I:I', 6)  # eg Set column A width to 20
        executive_sheet.set_column('J:J', 7.43)  # eg Set column A width to 20
        executive_sheet.set_column('Q:Q', 17)  # eg Set column A width to 20
        executive_sheet.set_column('R:R', 14.75)  # eg Set column A width to 20
        executive_sheet.set_column('S:S', 3)  # eg Set column A width to 20
        executive_sheet.set_column('T:AC', 3)  # eg Set column A width to 20
        
        writer.sheets["ExecutiveSheet"] = executive_sheet

        # Font color for incorrect values
        red_font = workbook.add_format({
                        'align': 'center',
                        'valign': 'vcenter',
                        'font_color': 'red'
                    })
        green_font = workbook.add_format({
                        'align': 'center',
                        'valign': 'vcenter',
                        'font_color': 'green'
                    })
        purple_font = workbook.add_format({
                        'align': 'center',
                        'valign': 'vcenter',
                        'font_color': 'purple'
                    })
        darkblue_font = workbook.add_format({
                        'align': 'center',
                        'valign': 'vcenter',
                        'font_color': 'blue'
                    })
        
        global_start_row = 0

        # Loop through each sheet and the corresponding cell ranges
        for sheet_name, cell_ranges in sheet_ranges.items():
            print(f"Processing sheet: {sheet_name}")
            
            # Get specified cell position for the sheet in the executive sheet
            start_row, start_col = cell_positions.get(sheet_name, (0, 0))  # Default to top-left if not specified
            
           
            # Special case for 'raven' sheet to compare answers
            if sheet_name == 'raven':
                # Correct answers vector for 'raven' sheet comparison
                correct_answers_raven = [4,5,1,2,6,3,6,2,1,3,4,5,4,5,1,6,2,1,3,4,6,3,5,2,2,6,1,2,1,3,5,6,4,3,4,5]
                data_start_row = start_row
                
                # Read the answers from the range A2:A37 with skiprows=0
                raven_df = pd.read_excel(file_path, sheet_name=sheet_name, usecols="A", skiprows=0, nrows=36)
                your_answers = raven_df.iloc[:, 0].tolist()  # Extract as list
                print(f"Your answers: {your_answers}")
                
                # Handle NaN or special value condition
                if( your_answers==[] ):
                    print(subno)
                    exit()
                    
                if( your_answers[0] == 100 ):
                    data_start_row += 1
                    executive_sheet.write(data_start_row, start_col, 100)
                    correct_score = -1
                    child_year = -1
                    child_year_true = -1
                    final_raven_score = -1
                    

                else:
                    # Compare with the correct answers
                    correct_score = sum(1 for your_ans, correct_ans in zip(your_answers, correct_answers_raven) if your_ans == correct_ans)
                    print(f"Your correct score for RAVEN is: {correct_score}")
                    
                    final_raven_score, child_year, child_year_true = identify_raven_score(main_folder, current_raven_DB_filename, start_date, subno, correct_score)
                    

                # Write the custom header and score to the specified cell
                data_start_row += 1 
                executive_sheet.write(start_row, start_col, custom_headers.get(sheet_name, 'Raven Score'))
                executive_sheet.write(data_start_row, start_col, final_raven_score, center_format)
                executive_sheet.write(data_start_row, start_col+1, child_year, center_format)
                executive_sheet.write(data_start_row, start_col+2, child_year_true, center_format)
                executive_sheet.write(data_start_row, start_col+3, correct_score, center_format)
                executive_sheet.write(data_start_row+1, start_col, 'score', center_format)
                executive_sheet.write(data_start_row+1, start_col+1, 'raven age', center_format)
                executive_sheet.write(data_start_row+1, start_col+2, 'true age', center_format)
                executive_sheet.write(data_start_row+1, start_col+3, 'correct score', center_format)
                
                global_start_row = data_start_row+2
                
           

            elif sheet_name == 'partA':
                partAdone = True
            
                # Set data start row just below the header
                start_row, start_col = global_start_row + 2, 0
                
                # Write the custom header for this sheet at the specified starting row and column
                header_text = custom_headers.get(sheet_name, sheet_name)
                executive_sheet.write(start_row, start_col, header_text)
                partA_df = pd.read_excel(file_path, sheet_name=sheet_name)

                # Define correct values for comparison for partA
                realwords = ['ποίημα', 'λουλούδια', 'σκουπίδια', 'πρόσκληση', 'τήβεννος', 'αλάτια', 'δεσμεύω', 'εγκλείει', 'περιβάλλον', 'υπεύθυνος', 'εκπαίδευση', 'ηλεκτρική', 'βοοειδές', 'παυσίπονο', 'αρδευτικός', 'μετεγγραφές', 'επιχειρήματα', 'ταξιδεύουμε', 'δραστηριότητες', 'συμπληρώσουμε', 'ακαδημαϊκά', 'αυθαιρεσίες', 'σταφιδιασμένα', 'εκσυγχρονισμένος']
                pseudowords = ['άπηζε', 'θάισσε', 'μιούφαχο', 'οίφλατο', 'τζαλικιού', 'βριψίγκες', 'πουμπλάζει', 'μπρεστικά', 'νεπακίζω', 'ψειδικόμος', 'αυγετάλια', 'μπαθιλένα', 'ντιλεγοτιά', 'τραγγεθούμε', 'στραδημένος', 'χρουλαγκρίκι', 'ξερηχολόγος', 'οικιλειπιχάνων', 'ζουνιαλεκάει', 'κτουληνυσίζω', 'εργανουδάκια', 'αφαπληρωσμένο', 'ταζαμπρεγάγει', 'εγδατιντρόμενο']
                
                answered_value_realwords = partA_df.iloc[:, 0].dropna().tolist()   
                answered_realwords = partA_df.iloc[:, 3].dropna().tolist()   
                answered_value_pseudowords = partA_df.iloc[:, 1].dropna().tolist()   
                answered_pseudowords = partA_df.iloc[:, 4].dropna().tolist()  
                
                
                # Handle NaN or special value (100) condition
                if(partA_df['Ans11'][0] == 100 and partA_df['Ans21'][0] == 100):
                    partAdone = False
                    global_start_row += 4
                    executive_sheet.write(start_row+1, start_col, 100, green_font)
                    continue
                elif(partA_df['Ans11'][0] == 100 and partA_df['Ans21'][0] != 100):
                    partAdone = False
                    executive_sheet.write(start_row+1, start_col, 100, green_font)
                elif(partA_df['Ans11'][0] != 100 and partA_df['Ans21'][0] == 100):
                    partAdone = False
                    executive_sheet.write(start_row+1, start_col+1, 100, green_font)
                    
                # Check if null exist in answers
                all_answers = pd.concat([partA_df.iloc[:len(realwords), 3], partA_df.iloc[:len(pseudowords), 4]], ignore_index=True)
                for ans in all_answers:
                    if isinstance(ans, float) and np.isnan(ans):
                        print("Null cells in ", sheet_name)
                        exit()
                        
                
                real_words_score = -1 if (partA_df.iloc[1, 0] == 100) else 0
                pseudo_words_score = -1 if (partA_df.iloc[1, 1] == 100) else 0
                value_is_two = -1 if (partA_df.iloc[1, 0] == 100) else 0
                value_is_three = -1 if (partA_df.iloc[1, 0] == 100) else 0
                
                # Calculate correct real words
                if( partA_df['Ans11'][0] != 100 ):
                    for i in range(len(answered_value_realwords)):
                        if(i>3 and (answered_value_realwords[i-4]==0 or answered_value_realwords[i-4]==2) and (answered_value_realwords[i-3]==0 or answered_value_realwords[i-3]==2) and (answered_value_realwords[i-2]==0 or answered_value_realwords[i-2]==2) and (answered_value_realwords[i-1]==0 or answered_value_realwords[i-1]==2) and (answered_value_realwords[i]==0 or answered_value_realwords[i]==2)):
                            break
                        if(answered_value_realwords[i]==1):
                            real_words_score += 1
                        elif(answered_value_realwords[i]==2):
                            value_is_two += 1
                        elif(answered_value_realwords[i]==3):
                            value_is_three += 1

                            
                if( partA_df['Ans11'][0] != 100 ):
                    for i in range(len(answered_value_realwords)):
                        if(answered_value_realwords[i]==1):
                            executive_sheet.write(start_row+1+i, start_col, answered_value_realwords[i], center_format)
                            executive_sheet.write(start_row+1+i, start_col+3, answered_realwords[i], center_format)
                        elif(answered_value_realwords[i]==2):
                            executive_sheet.write(start_row+1+i, start_col, answered_value_realwords[i], purple_font)
                            executive_sheet.write(start_row+1+i, start_col+3, answered_realwords[i], purple_font)
                        elif(answered_value_realwords[i]==3):
                            executive_sheet.write(start_row+1+i, start_col, answered_value_realwords[i], darkblue_font)
                            executive_sheet.write(start_row+1+i, start_col+3, answered_realwords[i], darkblue_font)
                        else:
                            executive_sheet.write(start_row+1+i, start_col, answered_value_realwords[i], red_font)
                            executive_sheet.write(start_row+1+i, start_col+3, answered_realwords[i], red_font)
                
                    executive_sheet.write(start_row+1+i+1, start_col, real_words_score, center_format)
                
                    
                # Calculate correct preudo words
                stoprulea2 = 0
                if( partA_df['Ans21'][0] != 100 ):
                    for i in range(len(answered_value_pseudowords)):
                        if(i>3 and (answered_value_pseudowords[i-4]==0 or answered_value_pseudowords[i-4]==2) and (answered_value_pseudowords[i-3]==0 or answered_value_pseudowords[i-3]==2) and (answered_value_pseudowords[i-2]==0 or answered_value_pseudowords[i-2]==2) and (answered_value_pseudowords[i-1]==0 or answered_value_pseudowords[i-1]==2) and (answered_value_pseudowords[i]==0 or answered_value_pseudowords[i]==2)):
                            break
                        if(answered_value_pseudowords[i]==1):
                            pseudo_words_score += 1
                        elif(answered_value_pseudowords[i]==2):
                            value_is_two += 1
                            stoprulea2 += 1
                        elif(answered_value_pseudowords[i]==3):
                            value_is_three += 1
                            
                            
                if( partA_df['Ans21'][0] != 100 ):
                    for i in range(len(answered_value_pseudowords)):
                        if(answered_value_pseudowords[i]==1):
                            executive_sheet.write(start_row+1+i, start_col+1, answered_value_pseudowords[i], center_format)
                            executive_sheet.write(start_row+1+i, start_col+4, answered_pseudowords[i], center_format)
                        elif(answered_value_pseudowords[i]==2):
                            executive_sheet.write(start_row+1+i, start_col+1, answered_value_pseudowords[i], purple_font)
                            executive_sheet.write(start_row+1+i, start_col+4, answered_pseudowords[i], purple_font)
                        elif(answered_value_pseudowords[i]==3):
                            executive_sheet.write(start_row+1+i, start_col+1, answered_value_pseudowords[i], darkblue_font)
                            executive_sheet.write(start_row+1+i, start_col+4, answered_pseudowords[i], darkblue_font)
                        else:
                            executive_sheet.write(start_row+1+i, start_col+1, answered_value_pseudowords[i], red_font)
                            executive_sheet.write(start_row+1+i, start_col+4, answered_pseudowords[i], red_font)
                
                    executive_sheet.write(start_row+1+i+1, start_col+1, pseudo_words_score, center_format)
                
                value_is_two_str = "Error 2: " + str(value_is_two)
                value_is_three_str = "Error 3: " + str(value_is_three)
                executive_sheet.write(start_row+1+i+1, start_col+2+1, value_is_two_str, center_format)
                executive_sheet.write(start_row+1+i+1, start_col+3+1, value_is_three_str, center_format)    
                 
                start_row = start_row+1+i+1
                 
                # executive_sheet.write(start_row+1+i+1, start_col+2, value_is_two, center_format)
                # executive_sheet.write(start_row+1+i+1, start_col+3, value_is_three, center_format)            
                                  
                                 
                print(f"Your correct score in decoding real words is: {real_words_score} out of 24")
                print(f"Your correct score in decoding pseudo words is: {pseudo_words_score} out of 24")
                print(f"Your had {value_is_two} number 2 errors in decoding")
                print(f"Your had {value_is_three} number 3 errors in decoding")
            
                global_start_row = start_row + 1
            
                       
            elif sheet_name == 'partB exerc3':      
                partB3done = True      
                        
                # Set data start row just below the header
                start_row, start_col = global_start_row + 2, 0
                header_text = custom_headers.get(sheet_name, sheet_name)
                executive_sheet.write(start_row, start_col, header_text)
                
                correct_partB3_1 = [0,0,1]   
                correct_partB3_2 = [0,1,0]
                correct_partB3_3 = [1,0,1]
                correct_partB3_4 = [1,0,1,1]
                correct_partB3_5 = [0,1,1,0]
                correct_partB3_6 = [1,0,0,1]
                correct_partB3_7 = [0,1,0,1,1]
                correct_partB3_8 = [1,0,1,0,1]
                correct_partB3_9 = [1,0,1,1,0]
                
                total_correct_ans = [correct_partB3_1, correct_partB3_2, correct_partB3_3, correct_partB3_4, correct_partB3_5, correct_partB3_6, correct_partB3_7, correct_partB3_8, correct_partB3_9]
                
                partB3_df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[0, 1, 2], header=None)
                    
                clean_columns = {}
                for col in partB3_df.columns:
                    clean_columns[col] = partB3_df[col].dropna().tolist()

                donePart = [True if 1 in clean_columns[1] else False]
                if not donePart[0]:
                    partB3done = False
                    global_start_row += 4
                    executive_sheet.write(start_row+1, start_col, 100, green_font)
                    continue
                    
                given_answers = clean_columns[1]
                given_answers_1 = given_answers[:3]
                given_answers_2 = given_answers[3:6]
                given_answers_3 = given_answers[6:9]
                given_answers_4 = given_answers[9:13]
                given_answers_5 = given_answers[13:17]
                given_answers_6 = given_answers[17:21]
                given_answers_7 = given_answers[21:26]
                given_answers_8 = given_answers[26:31]
                given_answers_9 = given_answers[31:36]
                
                total_given_answers = [given_answers_1, given_answers_2, given_answers_3, given_answers_4, given_answers_5, given_answers_6, given_answers_7, given_answers_8, given_answers_9]
                
                # # # # # # # # # # # Score and Stop Rule # # # # # # # # # # #
                
                # # Find row and index/column where I have to stop according to the stop rule
                stoprow = len(total_correct_ans)-1
                real1 = False
                real2 = False
                real3 = False
                for i in range(len(total_correct_ans)-2):
                    real1 = False
                    real2 = False
                    real3 = False
                    # first row
                    for j in range(len(total_correct_ans[i])):
                        if(total_correct_ans[i][j]==1 and total_given_answers[i][j]==1):
                            real1 = True
                            break
                           
                    # second row
                    for j in range(len(total_correct_ans[i+1])):
                        if(total_correct_ans[i+1][j]==1 and total_given_answers[i+1][j]==1):
                            real2 = True
                            break
                            
                    # third row
                    for j in range(len(total_correct_ans[i+2])):
                        if(total_correct_ans[i+2][j]==1 and total_given_answers[i+2][j]==1):
                            real3 = True
                            break
                    
                    if real1:
                        continue
                    
                    if(real1==False and real2==False and real3==False):
                        stoprow = i+2
                        
                # # Find score until stop row, index/column 
                scoreb3 = 0
                
                # Count score before stop row
                for i in range(stoprow+1):
                    for j in range(len(total_correct_ans[i])):
                        if(total_correct_ans[i][j]==total_given_answers[i][j]):
                            scoreb3+=1
                            
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                
                executive_sheet.write_column(start_row+1, start_col, clean_columns[0], center_format)
                executive_sheet.write_column(start_row+1, start_col+1, given_answers, center_format)
                executive_sheet.write_column(start_row+1, start_col+2, correct_partB3_1+correct_partB3_2+correct_partB3_3+correct_partB3_4+correct_partB3_5+correct_partB3_6+correct_partB3_7+correct_partB3_8+correct_partB3_9, center_format)
                executive_sheet.write(start_row+1, start_col+3, scoreb3, center_format)
                
                global_start_row = start_row + len(clean_columns[0]) + 1


            elif sheet_name == 'partB exerc4':
                partB4done = True
                
                # Set data start row just below the header
                start_row, start_col = global_start_row + 2, 0
                header_text = custom_headers.get(sheet_name, sheet_name)
                executive_sheet.write(start_row, start_col, header_text)

                partB4_df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[0, 1, 2], header=None)
                    
                clean_columns = {}
                for col in partB4_df.columns:
                    # Get the column as a list
                    column_data = partB4_df[col].tolist()

                    # Apply the conversion from NaN/Inf to None to each item in the list
                    cleaned_column_data = [
                        None if pd.isna(x) or (isinstance(x, (float, np.float_)) and np.isinf(x)) else x
                        for x in column_data
                    ]

                    clean_columns[col] = cleaned_column_data
                
                clean_columns[0] = [x for x in clean_columns[0] if x!=None]
                
                given_answers = clean_columns[1]

                if(given_answers[0] == 100):
                    partB4done = False
                    global_start_row += 4
                    executive_sheet.write(start_row+1, start_col, 100, green_font)
                    continue
                    
                # # # # # # # # # # # Score and Stop Rule # # # # # # # # # # # 
                scoreb4 = 0
                for i in range(len(given_answers)):
                    if(given_answers[i]==0):
                        if(i<len(given_answers)-2 and given_answers[i]==0 and given_answers[i+1]==0 and given_answers[i+2]==0):
                            break
                        
                    elif(given_answers[i]==1):
                        scoreb4+=1

                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                
                executive_sheet.write_column(start_row+1, start_col, clean_columns[0], center_format)
                executive_sheet.write_column(start_row+1, start_col+1, given_answers, center_format)
                executive_sheet.write_column(start_row+1, start_col+2, clean_columns[2], center_format)
                executive_sheet.write(start_row+1, start_col+3, scoreb4, center_format)
                
                global_start_row = start_row + len(clean_columns[0]) + 1

            
            
            elif sheet_name == 'partC':
                partCdone = True
                
                # Set data start row just below the header
                start_row, start_col = global_start_row + 2, 0
                header_text = custom_headers.get(sheet_name, sheet_name)
                executive_sheet.write(start_row, start_col, header_text)
                
                partC_df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[0, 1, 3], header=None)
                
                clean_columns = {}
                for col in partC_df.columns:
                    clean_columns[col] = partC_df[col].dropna().tolist()
                
                if(clean_columns[3]==[]):
                    partCdone = False
                    global_start_row += 4
                    executive_sheet.write(start_row+1, start_col, 100, green_font)
                    continue
                
                index = int(clean_columns[3][0])
                
                given_answers = clean_columns[1]
                
                # # # # # # # # # # # Score and Stop Rule # # # # # # # # # # # 
                scorec = given_answers[:index].count(1)
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                
                executive_sheet.write_column(start_row+1, start_col, clean_columns[0], center_format)
                executive_sheet.write_column(start_row+1, start_col+1, given_answers, center_format)
                executive_sheet.write(start_row+1, start_col+2, index, center_format)
                executive_sheet.write(start_row+1, start_col+3, scorec, center_format) 
                
                global_start_row = start_row + max(len(clean_columns[0]), len(given_answers)) + 1


            elif sheet_name == 'partD exerc6':
                partD6done = True
                
                # Set data start row just below the header
                start_row, start_col = global_start_row + 2, 0
                header_text = custom_headers.get(sheet_name, sheet_name)
                executive_sheet.write(start_row, start_col, header_text)
                
                partD6_df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[0, 1, 2], header=None)
                
                clean_columns = {}
                for col in partD6_df.columns:
                    # Get the column as a list
                    column_data = partD6_df[col].tolist()
                    
                    # Apply the conversion from NaN/Inf to None to each item in the list
                    cleaned_column_data = [
                        None if pd.isna(x) or (isinstance(x, (float, np.float_)) and np.isinf(x)) else x
                        for x in column_data
                    ]

                    clean_columns[col] = cleaned_column_data
                
                clean_columns[0] = [x for x in clean_columns[0] if x!=None]
                
                given_answers = clean_columns[1]

                if(given_answers[0] == 100):
                    partD6done = False
                    global_start_row += 4
                    executive_sheet.write(start_row+1, start_col, 100, green_font)
                    continue
                
                # # # # # # # # # # # Score and Stop Rule # # # # # # # # # # # 
                scored6 = 0
                for i in range(len(given_answers)):
                    if(given_answers[i]==0):
                        if(i<len(given_answers)-2 and given_answers[i]==0 and given_answers[i+1]==0 and given_answers[i+2]==0):
                            break
                        
                    elif(given_answers[i]==1):
                        scored6+=1

                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

                executive_sheet.write_column(start_row+1, start_col, clean_columns[0], center_format)
                executive_sheet.write_column(start_row+1, start_col+1, given_answers, center_format)
                executive_sheet.write_column(start_row+1, start_col+2, clean_columns[2], center_format)
                executive_sheet.write(start_row+1, start_col+3, scored6, center_format)
                
                global_start_row = start_row + len(clean_columns[0]) + 1
                
                
            elif sheet_name == 'partD exerc7':
                partD7done = True
                
                # Set data start row just below the header
                start_row, start_col = global_start_row + 2, 0
                header_text = custom_headers.get(sheet_name, sheet_name)
                executive_sheet.write(start_row, start_col, header_text)
                
                startrowd7 = start_row
                
                partD7_df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[0, 1, 2], header=None)
                
                clean_columns = {}
                for col in partD7_df.columns:
                    # Get the column as a list
                    column_data = partD7_df[col].tolist()
                    
                    # Apply the conversion from NaN/Inf to None to each item in the list
                    cleaned_column_data = [
                        None if pd.isna(x) or (isinstance(x, (float, np.float_)) and np.isinf(x)) else x
                        for x in column_data
                    ]

                    clean_columns[col] = cleaned_column_data
                
                clean_columns[0] = [x for x in clean_columns[0] if x!=None]

                given_answers = clean_columns[1]

                if(given_answers[0] == 100):
                    partD7done = False
                    global_start_row += 4
                    executive_sheet.write(start_row+1, start_col, 100, green_font)
                    continue

                # # # # # # # # # # # Score and Stop Rule # # # # # # # # # # # 
                scored7 = 0
                for i in range(len(given_answers)):
                    if(given_answers[i]==0):
                        if(i<len(given_answers)-2 and given_answers[i]==0 and given_answers[i+1]==0 and given_answers[i+2]==0):
                            break
                        
                    elif(given_answers[i]==1):
                        scored7+=1

                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

                executive_sheet.write_column(start_row+1, start_col, clean_columns[0], center_format)
                executive_sheet.write_column(start_row+1, start_col+1, given_answers, center_format)
                executive_sheet.write_column(start_row+1, start_col+2, clean_columns[2], center_format)
                executive_sheet.write(start_row+1, start_col+3, scored7, center_format)
                
                global_start_row = start_row + len(clean_columns[0]) + 1
                
                
                
            elif sheet_name == 'partΕ exerc8':
                partE8done = True
                
                # Set data start row just below the header
                start_row, start_col = global_start_row + 2, 0
                header_text = custom_headers.get(sheet_name, sheet_name)
                executive_sheet.write(start_row, start_col, header_text)
                
                partE8_df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[0, 1, 2], header=None)
                
                clean_columns = {}
                for col in partE8_df.columns:
                    # Get the column as a list
                    column_data = partE8_df[col].tolist()
                    
                    # Apply the conversion from NaN/Inf to None to each item in the list
                    cleaned_column_data = [
                        None if pd.isna(x) or (isinstance(x, (float, np.float_)) and np.isinf(x)) else x
                        for x in column_data
                    ]

                    clean_columns[col] = cleaned_column_data
                
                clean_columns[0] = [x for x in clean_columns[0] if x!=None]
                
                given_answers = clean_columns[1]

                if(given_answers[0] == 100):
                    partE8done = False
                    global_start_row += 4
                    executive_sheet.write(start_row+1, start_col, 100, green_font)
                    continue
                
                # # # # # # # # # # # Score and Stop Rule # # # # # # # # # # # 
                scoree8 = 0
                for i in range(len(given_answers)):
                    if(given_answers[i]==0):
                        if(i<len(given_answers)-2 and given_answers[i]==0 and given_answers[i+1]==0 and given_answers[i+2]==0):
                            break
                        
                    elif(given_answers[i]==1):
                        scoree8+=1

                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

                executive_sheet.write_column(start_row+1, start_col, clean_columns[0], center_format)
                executive_sheet.write_column(start_row+1, start_col+1, given_answers, center_format)
                executive_sheet.write_column(start_row+1, start_col+2, clean_columns[2], center_format)
                executive_sheet.write(start_row+1, start_col+3, scoree8, center_format)       
                
                global_start_row = start_row + len(clean_columns[0]) + 1


            elif sheet_name == 'partΕ exerc9':
                partE9done = True
                
                # Set data start row just below the header
                start_row, start_col = global_start_row + 2, 0
                header_text = custom_headers.get(sheet_name, sheet_name)
                executive_sheet.write(start_row, start_col, header_text)
                
                correct_partE9_ans = [35, 25, 24, 25]
                
                partE9_df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[0, 1, 2], header=None)
                
                condition = partE9_df[2].notna()

                partE9_df.loc[condition, 1] = (partE9_df.loc[condition, 1].fillna(0).astype(int).astype(str) +
                               partE9_df.loc[condition, 2].fillna(0).astype(int).astype(str)).astype(float)
                
                clean_columns = {
                    0: partE9_df[0].tolist(),
                    1: partE9_df[1].tolist(), # This column now contains the concatenated values or original values
                    2: partE9_df[2].tolist()  # This column remains unchanged
                }
                
                clean_columns[0] = [x for x in clean_columns[0] if not pd.isna(x)]
                clean_columns[1] = [x if not pd.isna(x) else None for x in clean_columns[1]]
                clean_columns[2] = [x if not pd.isna(x) else None for x in clean_columns[2]]
                
                given_answers = [int(x) for x in clean_columns[1] if not pd.isna(x)]
                if(given_answers[0] == 100):
                    partE9done = False
                    global_start_row += 4
                    executive_sheet.write(start_row+1, start_col, 100, green_font)
                    continue
                
                check_equal = [1 if given_answers[i] == correct_partE9_ans[i] else 0 for i in range(len(given_answers))]

                # # # # # # # # # # # Score and Stop Rule # # # # # # # # # # # 
                scoree9 = 0
                for i in range(len(check_equal)):
                    if(check_equal[i]==0):
                        if(i<len(check_equal)-2 and check_equal[i]==0 and check_equal[i+1]==0 and check_equal[i+2]==0):
                            break
                        
                    elif(check_equal[i]==1):
                        scoree9+=1

                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

                executive_sheet.write_column(start_row+1, start_col, clean_columns[0], center_format)
                executive_sheet.write_column(start_row+1, start_col+1, given_answers, center_format)
                executive_sheet.write_column(start_row+1, start_col+2, clean_columns[2], center_format)
                executive_sheet.write(start_row+1, start_col+3, scoree9, center_format)
                
                global_start_row = start_row + len(clean_columns[0]) + 1


            elif sheet_name == 'partST exerc10':
                partST10done = True
                
                # Set data start row just below the header
                start_row, start_col = global_start_row + 2, 0
                header_text = custom_headers.get(sheet_name, sheet_name)
                executive_sheet.write(start_row, start_col, header_text)
                
                correct_partST10_1_ans = [4,2,4,1,1,2,3]   
                correct_partST10_2_ans = [4,2,1,1,3,2,3]   
                correct_partST10_3_ans = [4,2,4,1,3,1,3]  
                
                total_correct_answers = correct_partST10_1_ans + correct_partST10_2_ans + correct_partST10_3_ans
                
                partST_df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[0, 1], header=None)
                
                grouped_data = partST_df.groupby(0)[1].apply(list).to_dict()

                # Now, you can access your lists by the unique elements from column 0
                explore_answers = grouped_data['Η εξερευνηση']
                alexander_answers = grouped_data['Ο Μ. Αλεξανδρος']
                maya_answers = grouped_data['Οι Μάγια']

                if(explore_answers[0]==100):
                    partST10done = False
                    global_start_row += 4
                    executive_sheet.write(start_row+1, start_col, 100, green_font)
                    continue
                
                scorest10 = 0
                
                # # # # # # # # # # # Score and Stop Rule # # # # # # # # # # # 

                # Explorer Text
                zeros1 = 0
                for i in range(len(explore_answers)):
                    if(explore_answers[i]!=correct_partST10_1_ans[i]):
                        zeros1 += 1
                        if(zeros1==5):
                            break
                    else:
                        scorest10+=1
                
                # Alexander Text
                zeros2 = 0
                if(zeros1<5):
                    for i in range(len(alexander_answers)):
                        if(alexander_answers[i]!=correct_partST10_2_ans[i]):
                            zeros2 += 1
                            if(zeros2==5):
                                break
                        else:
                            scorest10+=1                

                # Maya Text
                zeros3 = 0
                if(zeros1<5 and zeros2<5):
                    for i in range(len(maya_answers)):
                        if(maya_answers[i]!=correct_partST10_3_ans[i]):
                            zeros3 += 1
                            if(zeros3==5):
                                break
                        else:
                            scorest10+=1  
                
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                
                
                partST_df.to_excel(writer, sheet_name="ExecutiveSheet",
                                startrow=start_row+1,
                                startcol=start_col,
                                index=False, # Do not write the DataFrame index
                                header=False) # Write the DataFrame headers (column names)
        
                executive_sheet.write_column(start_row+1, start_col+2, total_correct_answers, center_format)
                executive_sheet.write(start_row+1, start_col+3, scorest10, center_format)
                
                global_start_row = start_row + len(total_correct_answers) + 1
                
      
            else:
                # For other sheets, proceed as usual
                sheet_df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

                # Create a temporary DataFrame for the selected cells
                temp_df = pd.DataFrame()

                # Extract data from the specified ranges
                for cell_range in cell_ranges:
                    start_cell, end_cell = cell_range.split(':')
                    
                    # Convert cell addresses to row and column indices
                    start_row_df, start_col_df = convert_cell_to_index(start_cell)
                    end_row_df, end_col_df = convert_cell_to_index(end_cell)
                    
                    # Select the range and append it to the temporary DataFrame
                    temp_df = pd.concat([temp_df, sheet_df.iloc[start_row_df:end_row_df+1, start_col_df:end_col_df+1]], axis=1)

                # Write the custom header and data at the specified position
                executive_sheet.write(start_row, start_col, custom_headers.get(sheet_name, sheet_name))
                temp_df.to_excel(writer, sheet_name="ExecutiveSheet", startrow=start_row + 1, startcol=start_col, index=False, header=False)
    
    
        # Complete Total Scores
        start_row = global_start_row + 5
        executive_sheet.write(start_row, 0, 'Total Score 1', center_format)
        if(partAdone and partB3done):
            executive_sheet.write(start_row+1, 0, real_words_score+pseudo_words_score+value_is_three+scoreb3, center_format)
            
        executive_sheet.write(start_row, 1, 'Total Score 2', center_format)
        if(partCdone):
            executive_sheet.write(start_row+1, 1, scorec, center_format)
        
        executive_sheet.write(start_row, 2, 'Total Score 3', center_format)
        if(partB4done and partD6done and partD7done and partE8done):
            executive_sheet.write(start_row+1, 2, scoreb4+scored6+scored7+scoree8, center_format)
            
        executive_sheet.write(start_row, 3, 'Total Score 4', center_format)
        if(partE9done and partST10done):
            executive_sheet.write(start_row+1, 3, scoree9+scorest10, center_format)

        workbook.close()
        
             
    print(f"Executive sheet saved as {output_path}")
    
     # Export the Excel sheet to PDF
    pdf_filename = save_directory + "executive_sheet_" + str(subno) + ".pdf"
    excel_to_pdf(output_path, pdf_filename)
    autofitexcel(output_path, startrowd7)
        


# Helper function to convert Excel cell (e.g., 'A1') to row and column indices
def convert_cell_to_index(cell):
    col = ord(cell[0].upper()) - ord('A')  # Convert 'A' to 0, 'B' to 1, etc.
    row = int(cell[1:]) - 1  # Convert '1' to 0, '2' to 1, etc.
    return row, col

   
def identify_raven_score(main_folder, current_raven_DB_filename, start_date, subno, initial_score):
    # Read date of birth and id of all children
    dataframe1 = pd.read_excel(main_folder+current_raven_DB_filename) 
    df1_ID = [idno for idno in dataframe1["ID"].dropna().tolist()]
    
    start_date = '-'.join(reversed(start_date.split("/")))
    
    # Convert format of year(y) and month(m) in a suitable one, like '11y3m' -> '11.3' and after convert if to float like 11.3
    df1_years = dataframe1[pd.to_datetime(start_date)].tolist()
    for yearno in range(len(df1_years)):
        if not pd.isna(df1_years[yearno]) :
            df1_years[yearno] = df1_years[yearno].replace("y", ".")
            df1_years[yearno]= df1_years[yearno].replace("m", "")
            df1_years[yearno] = float(df1_years[yearno])
    
    # Find child's year 
    for ino in range(len(df1_ID)):
        if(df1_ID[ino]==subno):
            child_year = df1_years[ino]
    
    # Keep the childs true age for reference
    child_year_true = child_year
    
    # Raven is only for students until 12 years old, so if you find someone older than this then consider he is 12 years old
    if( child_year > 11 ):
        child_year = 11
        
    # convert child's year into a raven's year formulation
    child_year = floor_half_round(child_year)  
    
    # Read ages from raven (i.e the 4, 4.5, 5, 5.5, etc....)
    dataframe2 = pd.read_excel(main_folder+'raven_score_norms.xlsx')
    ages = dataframe2.iloc[0,:].tolist()
    
    # Convert nan to something comparable with integers, but not valid (i.e convert it to -1)
    for i in range(len(ages)):
        if  pd.isna(ages[i]) :
            ages[i] = -1
    
    # Find in which age block the child belongs to, make a match between his age and rave's ages and keep the index of the column that exist a matching
    for i in range(len(ages)):
        if(ages[i] == child_year):
            column_no = i
    
    # Find according to child's initial score (i.e how many answers he has answer correct) the raven's score
    temporary_scores = dataframe2.iloc[1:, column_no].dropna().tolist()
    final_scores = dataframe2.iloc[1:, column_no-1].dropna().tolist()
    for i in range(len(temporary_scores)):
        if(initial_score==temporary_scores[i]):
            final_score = final_scores[i]
    
    return final_score, child_year, child_year_true
    
    

def floor_half_round(number):
    if( number < 7 ):
        # Find the integer part
        integer_part = math.floor(number)
        # Determine if the number is closer to the nearest half
        if number - integer_part >= 0.5:
            return integer_part + 0.5
        else:
            return integer_part
    else:
        return math.floor(number)



def autofitexcel(output_path, startrowd7):
    # Now, open the saved workbook with openpyxl and apply auto-fit
    try:
        wb = openpyxl.load_workbook(output_path)
        ws = wb["ExecutiveSheet"] # Get the specific worksheet

        # Define the row ranges to skip for max_length calculation (1-indexed)
        # Each tuple represents (start_row, end_row)
        skip_row_ranges = [
            (startrowd7,startrowd7+10)
        ]

        for col_idx, col in enumerate(ws.columns):
            max_length = 0
            column_letter = col[0].column_letter # Get the column letter (e.g., 'A')

            for cell in col:
                current_row = cell.row

                # Check if the current row falls within ANY of the skip ranges
                skip_this_row = False
                for start_row, end_row in skip_row_ranges:
                    if start_row <= current_row <= end_row:
                        skip_this_row = True
                        break # Found a match, no need to check other ranges for this row
                
                if skip_this_row:
                    continue # Skip to the next cell in this column

                try:
                    cell_value_str = str(cell.value) if cell.value is not None else ""
                    if len(cell_value_str) > max_length:
                        max_length = len(cell_value_str)
                except TypeError:
                    pass

            # Ensure a minimum width even if all cells are empty or skipped
            if max_length == 0:
                adjusted_width = 5 # Default width for empty columns, adjust as needed
            else:
                adjusted_width = (max_length + 2) * 1.2 # Add a small buffer

            ws.column_dimensions[column_letter].width = adjusted_width

        wb.save(output_path)
        print(f"Workbook saved and columns auto-fitted to: {output_path}")

    except Exception as e:
        print(f"Error during auto-fitting with openpyxl: {e}")
        
        
        
def excel_to_pdf(excel_path, output_pdf_path, sheet_name=None):
    temp_html = "temp_output.html"

    # HTML header to ensure UTF-8 and Greek font usage
    html_prefix = '''
    <!DOCTYPE html>
    <html lang="el">
    <head>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: "DejaVu Sans", "Arial", sans-serif;
                font-size: 12px;
                direction: ltr;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                table-layout: fixed;
                word-wrap: break-word;
            }
            th, td {
                border: 1px solid #999;
                padding: 4px;
                text-align: left;
            }
        </style>
    </head>
    <body>
    '''

    html_suffix = '</body></html>'

    # Convert Excel to HTML
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_prefix)
        xlsx2html(excel_path, f, sheet=sheet_name, locale='el')
        f.write(html_suffix)

    # PDF options
    options = {
        'page-size': 'A4',
        'orientation': 'Portrait',
        'encoding': 'UTF-8',
        'margin-top': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        'margin-right': '0.5in',
        'zoom': '1.05',
        'dpi': 300
    }

    # Export HTML to PDF
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_file(temp_html, output_pdf_path, options=options, configuration=config)

    os.remove(temp_html)
    print(f"✅ Greek-compatible PDF exported to: {output_pdf_path}")
    
    

# Main function to let the user select the file path and save directory
def main():
    
    ############## Needed initial info #############
    
    # main_folder = 'E:/_MyPatients/'
    # main_folder = 'W:/'
    main_folder = 'U:/'
    
    current_raven_DB_filename = 'CYPRUS_LIST_2025_v1.xlsx'
    
    start_date = "8/6/2025"
       
    # For one or many subjects
    start = 14001
    end = 14001
    # end = 14258
    sublist = []
    ##################################################
    
    for i in range(start, end + 1):  # +1 because range is exclusive at the end
        sublist.append(i)
    
    # Define the range of subject numbers
    for subno in sublist:  # 13501 to 13520 inclusive
        # Define file path for each subject number
        file_path = main_folder + 'subject_' + str(subno) + '/testa.xlsx'
        # Define the directory to save results
        # save_directory = r'C:\_Iro_analysis_tobii7_HD\individual_CHERSO'
        
        # save_directory = r'E:/_MyPatients/'
        # save_directory = r'E:\_MyPatients_CHERSO\Executive sheets'
        save_directory = main_folder + 'subject_' + str(subno) + '/'
        
        
        # Print a message to indicate the current subject being processed
        print(f"Processing subject number: {subno}")
        
        
        # Define the cell ranges to extract for each sheet
        # sheet_ranges = {
        #     'raven': ['A2:A37'],  
        #     'memoryshortauditverb': ['A2:J8'],      
        #     'memoryworkauditverb': ['A2:E8'],      
        #     'phonolrhymes': ['A2:E2'],      
        #     'phonolsyllables': ['A2:J3'],      
        #     'phonolphonemes': ['A2:E3'],      
        #     'partA': ['A2:E54'],      
        #     'visualorthogrecogn': ['A2:J3'],      
        #     'decodesentences': ['A2:E2'],            
        # }
        # Define the cell ranges to extract for each sheet
        sheet_ranges = {
            'raven': ['A2:A37'],       
            'partA': ['A2:E54'],
            'partB exerc3': ['A1:C36'],
            'partB exerc4': ['A1:C8'],
            'partC':['A1:D279'],
            'partD exerc6': ['A1:C8'],
            'partD exerc7': ['A1:C8'],
            'partΕ exerc8': ['A1:C4'],
            'partΕ exerc9': ['A1:C4'],
            'partST exerc10': ['A1:B21']
        }

        # Define custom headers for each sheet
        custom_headers = {
            'raven': 'Raven Score',
            'partA': 'partA Score',
            'partB exerc3': 'partB exerc3 Score',
            'partB exerc4': 'partB exerc4 Score',
            'partC': 'PartC Score',
            'partD exerc6': 'partD exerc6 Score',
            'partD exerc7': 'partD exerc7 Score',
            'partΕ exerc8': 'partΕ exerc8 Score',
            'partΕ exerc9': 'partΕ exerc9 Score',
            'partST exerc10': 'partST exerc10 Score'
        }

        # Define specific cell positions for each sheet in the executive sheet
        cell_positions = {
            'raven': (0, 0),
            'partA' :(5, 0),
            'partB exerc3': (64, 0),
            'partB exerc4': (103, 0),
            'partC': (115, 0),
            'partD exerc6': (398, 0),
            'partD exerc7': (410, 0),
            'partΕ exerc8': (422, 0),
            'partΕ exerc9': (429, 0),
            'partST exerc10': (437,0)
        }
        
       # Check if the file exists before processing
        if os.path.exists(file_path):
            print(f"Processing subject number: {subno}")
            extract_from_sheet(main_folder, file_path, sheet_ranges, custom_headers, cell_positions, current_raven_DB_filename, start_date, subno, save_directory)
        else:
            print(f"File not found for subject number: {subno} at {file_path}. Skipping...")
        
        # Optional: You can add a brief delay if needed to prevent issues with large batch processing
        # time.sleep(1)  # Uncomment if delay is desired
    
    

if __name__ == "__main__":
    main()
