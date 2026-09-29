import pandas as pd
import math
import os
import math
from collections import Counter
import numpy as np
import glob
import xlsxwriter
from find_date_executed import find_date_executed
from find_dob import find_dob
from datetime import datetime

import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from auto_adjust_column_width_xlsx import auto_adjust_column_width_xlsx
from export_to_pdf import export_to_pdf

#######################################
#
# APOKORONAS ANALYSIS 2025 + STUDENT CARD (BEAUTIFY EXCEL FILE)
#
########################################




# Function to extract specific cells from each sheet
def extract_from_sheet(main_folder, sub_path, file_path, sheet_ranges, custom_headers, cell_positions, start_date, subno):
    # Load the Excel file
    xls = pd.ExcelFile(file_path)
    
    # Set up the writer and add the "ExecutiveSheet" sheet
    output_path = os.path.join(sub_path, f"executive_sheet_{subno}.xlsx")
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
        pink_font = workbook.add_format({
                        'align': 'center',
                        'valign': 'vcenter',
                        'font_color': 'pink'
                    })
        darkblue_font = workbook.add_format({
                        'align': 'center',
                        'valign': 'vcenter',
                        'font_color': 'blue'
                    })

        # Beautify Excel file
        beautify_filepath = os.path.join(sub_path, f"beautify_executive_sheet_{subno}.xlsx")
        bworkbook = xlsxwriter.Workbook(beautify_filepath)
        beautify_sheet_name = 'Student Card'
        bworksheet = bworkbook.add_worksheet(beautify_sheet_name)
        
        # Loop through each sheet and the corresponding cell ranges
        for sheet_name, cell_ranges in sheet_ranges.items():
            print(f"Processing sheet: {sheet_name}")
            
            # Get specified cell position for the sheet in the executive sheet
            start_row, start_col = cell_positions.get(sheet_name, (0, 0))  # Default to top-left if not specified
            
            # Write the custom header at the specified starting row and column
            executive_sheet.write(start_row, start_col, custom_headers.get(sheet_name, sheet_name))
            
            # Write beautify header
            bworksheet.write(0, 0, 'Raven') 

            # Special case for 'raven' sheet to compare answers
            if sheet_name == 'raven':
                # Correct answers vector for 'raven' sheet comparison
                correct_answers_raven = [4,5,1,2,6,3,6,2,1,3,4,5,4,5,1,6,2,1,3,4,6,3,5,2,2,6,1,2,1,3,5,6,4,3,4,5]
                data_start_row = start_row
                
                # Read the answers from the range A2:A37 with skiprows=0
                raven_df = pd.read_excel(file_path, sheet_name=sheet_name, usecols="A", skiprows=0, nrows=36)
                your_answers = raven_df.iloc[:, 0].tolist()  # Extract as list
                print(f"Your answers: {your_answers}")
                
                # See if bate of birth exist else dont take into consideration the raven test
                dob_str = age_years_months_decimal(subno, sub_path)
                
                # Handle NaN or special value condition
                if( your_answers==[] ):
                    print(subno)
                    exit()
                    
                if( your_answers[0] == 100  or dob_str==''):
                    data_start_row += 1
                    bworksheet.write(0, 1, 100)
                    executive_sheet.write(data_start_row, start_col, 100)
                    correct_score = -1
                    child_year = -1
                    child_year_true = -1
                    final_raven_score = -1
                    

                else:
                    # Compare with the correct answers
                    correct_score = sum(1 for your_ans, correct_ans in zip(your_answers, correct_answers_raven) if your_ans == correct_ans)
                    print(f"Your correct score for RAVEN is: {correct_score}")
                    
                    final_raven_score, child_year, child_year_true = identify_raven_score(subno, main_folder, sub_path, correct_score)
                    

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
                
                # Raven beautify
                bworksheet.write(0,1, str(correct_score) + '/' + str(len(correct_answers_raven)))
                bworksheet.write(0,2, 'Score:' + str(int(final_raven_score)))
                bworksheet.write(0,3, 'RA' + ':' + str(child_year))
                bworksheet.write(0,4, 'TA' + ':' + str(child_year_true))
                
           
           
            
            elif sheet_name == 'memoryshortauditverb':
                # Write the custom header for this sheet at the specified starting row and column
                header_text = custom_headers.get(sheet_name, sheet_name)
                executive_sheet.write(start_row, start_col, header_text)
                memory_df = pd.read_excel(file_path, sheet_name=sheet_name)

                
                # Write beautify header
                bworksheet.write(1, 0, 'Μνήμη Ακουστική Λεκτική')
                bworksheet.write(15, 0, 'Μνήμη Ακουστική Λεκτική')
                bworksheet.write(2, 0, 'Μνήμη Ακουστική Φωνολογική')  

                # Set data start row just below the header
                data_start_row = start_row

                # Calculate how many examples I have in this test and in which column is located the 'Ans21' 
                column_names = list(memory_df.loc[:, ~memory_df.columns.str.contains('Unnamed')])
                total_examples = len(column_names)
                part2_column_index = column_names.index('Ans21')
                
                correct_values_memoryshortauditverb_part1 = [
                    ['τόξο', 'γάτα', 'δέντρο'],
                    ['δώρο', 'μαλλιά', 'καρδιά', 'παιδί'],
                    ['μάτι', 'πλοίο', 'χώμα', 'ουρά'],
                    ['χάρτης', 'γλώσσα', 'μέλι', 'φύλλο', 'βροχή'],
                    ['δρόμος', 'αυλή', 'ελιά', 'στόμα', 'ήλιος'],
                    ['γάλα', 'ψάρι', 'τζάκι', 'νερό', 'τρένο', 'πόρτα'],
                    ['λάδι', 'σπίτι', 'γιαγιά', 'τυρί', 'νησί', 'βουνό', 'παπί']
                ]
                
                correct_values_memoryshortauditverb_part2 = [
                    [1],
                    [1],
                    [1],
                    [1],
                    [1],
                    [1],
                    [1],
                    [1],
                    [1],
                    [1]
                ]
                
                common_count_list = []
                
                max_column_length_correct_values = max( [len(correct_values_memoryshortauditverb_part1[i]) for i in range(len(correct_values_memoryshortauditverb_part1))] )
                
                # Handle NaN or special value (100) condition
                if(memory_df['Ans11'][0] == 100 and memory_df['Ans21'][0] == 100):
                    executive_sheet.write(data_start_row+1, start_col, 100, green_font)
                    executive_sheet.write(data_start_row+1, part2_column_index+9, 100, green_font)    # +9 vasilis addition for paging
                    bworksheet.write(1, 1, 100)
                    bworksheet.write(2, 1, 100)
                    continue
                elif(memory_df['Ans11'][0] == 100 and memory_df['Ans21'][0] != 100):
                    executive_sheet.write(data_start_row+1, start_col, 100, green_font)
                    bworksheet.write(1, 1, 100)
                elif(memory_df['Ans11'][0] != 100 and memory_df['Ans21'][0] == 100):
                    executive_sheet.write(data_start_row+1, part2_column_index+9, 100, green_font)   # +9 vasilis addition for paging
                    bworksheet.write(2, 1, 100)
                    
                # Check if null exist in answers Ans11
                if not (memory_df['Ans11'][0] == 100 ):
                    # all_answers = memory_df.iloc[0, :len(correct_values_memoryshortauditverb_part1)+len(correct_values_memoryshortauditverb_part2)]
                    all_answers = memory_df.iloc[0, 0:len(correct_values_memoryshortauditverb_part1)]
                    for ans in all_answers:
                        if isinstance(ans, float) and np.isnan(ans):
                            print("Null cells in ", sheet_name)
                            exit()
                
                # Check if null exist in answers Ans21
                if not ( memory_df['Ans21'][0] == 100):
                    # all_answers = memory_df.iloc[0, :len(correct_values_memoryshortauditverb_part1)+len(correct_values_memoryshortauditverb_part2)]
                    start = len(correct_values_memoryshortauditverb_part1)
                    end = start + len(correct_values_memoryshortauditverb_part2)
                    all_answers = memory_df.iloc[0, start:end]
                    for ans in all_answers:
                        if isinstance(ans, float) and np.isnan(ans):
                            print("Null cells in ", sheet_name)
                            exit()            
                
                
                # PART 1
                total_common_count_part1 = 0
                for i in range(len(correct_values_memoryshortauditverb_part1)):
                    answered_value = memory_df.iloc[:, i].dropna().tolist()   # Offset by 1 as values start from A2
                    start_row = data_start_row + 1

                    # Step 1: Convert the lists to dictionaries to remove duplicates
                    answered_values_dict = {item: None for item in answered_value}
                    correct_values_dict = {item: None for item in correct_values_memoryshortauditverb_part1[i]}
                    
                    # Step 2: Find the common items between the two dictionaries
                    common_items = answered_values_dict.keys() & correct_values_dict.keys()  # Intersection of keys

                    # Step 3: Count how many common items there are
                    common_count = len(common_items)
                    
                    # Adds-on: New Score in Memory
                    if(common_count==len(correct_values_memoryshortauditverb_part1[i])):
                        common_count_list.append(common_count)
                    # # # # #
                    
                    for j in range(len(answered_value)):
                        if(answered_value[j] in common_items):
                            executive_sheet.write(start_row, i, answered_value[j], center_format)
                        else:
                            executive_sheet.write(start_row, i, answered_value[j], red_font)
                        start_row+=1
                      
                    executive_sheet.write(data_start_row+max_column_length_correct_values+1, i, common_count, center_format)
                    bworksheet.write(16, i, str(common_count) + '/' + str(len(correct_values_memoryshortauditverb_part1[i])))
                    total_common_count_part1 += common_count
                
                new_score = max(common_count_list) if common_count_list!=[] else 0
                if memory_df['Ans11'][0] != 100:
                    # bworksheet.write(1, 1, str(total_common_count_part1) + '/' + str(sum(len(lst) for lst in correct_values_memoryshortauditverb_part1)))
                    bworksheet.write(1,1, str(new_score) + '/' + str(len(correct_values_memoryshortauditverb_part1[-1])))
                    executive_sheet.write(data_start_row+max_column_length_correct_values+2, 0, str(new_score), center_format)
                
                # PART 2
                total_common_count_part2 = 0
                for i in range(part2_column_index, part2_column_index+len(correct_values_memoryshortauditverb_part2)):
                    answered_value = memory_df.iloc[0, i]
                    correct_value = correct_values_memoryshortauditverb_part2[i-part2_column_index][0]
                    
                    start_row = data_start_row + 1

                    if(answered_value==correct_value):
                        executive_sheet.write(start_row, i, answered_value, center_format)
                        common_count = 1
                    elif(answered_value==0 or answered_value=='ΔΑ'):
                        executive_sheet.write(start_row, i, answered_value, red_font)
                        common_count = 0
                    else:
                        executive_sheet.write(start_row, i, answered_value, red_font)
                        common_count = 0
                                                
                    executive_sheet.write(data_start_row+max_column_length_correct_values+1, i, common_count, center_format)
                    total_common_count_part2 += common_count
                
                if memory_df['Ans21'][0] != 100:
                    bworksheet.write(2, 1, str(total_common_count_part2) + '/' + str(len(correct_values_memoryshortauditverb_part2)))
                    executive_sheet.write(data_start_row+max_column_length_correct_values+2, 1, str(total_common_count_part2), center_format)
            
            
            elif sheet_name == 'memoryworkauditverb':
                # Write the custom header for this sheet at the specified starting row and column
                header_text = custom_headers.get(sheet_name, sheet_name)
                executive_sheet.write(start_row, start_col, header_text)
                memorywork_df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Write beautify header
                bworksheet.write(3, 0, 'Μνήμη Εργαζόμενη')
                bworksheet.write(19, 0, 'Μνήμη Εργαζόμενη')

                # Set data start row just below the header
                data_start_row = start_row    
                          
                # Define correct values for comparison for memoryworkauditverb
                correct_values_memoryworkauditverb = [
                    [1,4,5],
                    [1,2,7,9],
                    [1,3,6,6,7],
                    [4,5,6,8,9],
                    [1,2,3,3,5,7],
                    [2,3,4,4,6,6,7],
                    [2,3,5,6,7,8,9]
                ]
                

                common_count_list = []
                
                max_column_length_correct_values = max( [len(correct_values_memoryworkauditverb[i]) for i in range(len(correct_values_memoryworkauditverb))] )
                

                # Handle NaN or special value (100) condition
                if(memorywork_df.iloc[0, 0] == 100):
                    executive_sheet.write(data_start_row+1, start_col, 100, green_font)
                    bworksheet.write(3, 1, 100)
                    continue

                # Check if null exist in answers
                all_answers = memorywork_df.iloc[0, :len(correct_values_memoryworkauditverb)]
                for ans in all_answers:
                    if isinstance(ans, float) and np.isnan(ans):
                        print("Null cells in ", sheet_name)
                        exit()
                
                total_unordered_counter = 0    
                for i in range(len(correct_values_memoryworkauditverb)):
                    answered_value = memorywork_df.iloc[:, i].dropna().tolist()   # Offset by 1 as values start from A2
                    start_row = data_start_row + 1
                    
                    if len(correct_values_memoryworkauditverb[i])>len(answered_value):
                        answered_value += [float('nan') for _ in range(len(answered_value), len(correct_values_memoryworkauditverb[i]))]
                    elif( len(correct_values_memoryworkauditverb[i])<len(answered_value) ):
                        correct_values_memoryworkauditverb[i] += [float('nan') for _ in range(len(correct_values_memoryworkauditverb[i]), len(answered_value))]
                        
                    # # # # # Count in order items # # # # #
                    inorder_counter = 0
                    max_loop_counter = max(len(correct_values_memoryworkauditverb[i]),len(answered_value))
                    for j in range(max_loop_counter):
                        if(correct_values_memoryworkauditverb[i][j]==answered_value[j]):
                            inorder_counter += 1
                            executive_sheet.write(start_row, i, answered_value[j], center_format)
                        else:
                            if not math.isnan(answered_value[j]):
                                executive_sheet.write(start_row, i, answered_value[j], red_font)
                        start_row+=1

                    # Adds-on: New Score in Memory
                    if(inorder_counter==len(correct_values_memoryworkauditverb[i])):
                        common_count_list.append(inorder_counter)
                    # # # # #
                    
                    # # # # # Count unordered items # # # # #
                    unordered_counter = 0
                    # Step 1: Count the occurrences of each item in both lists
                    counter_answered = Counter(answered_value)
                    counter_correct = Counter(correct_values_memoryworkauditverb[i])

                    # Step 2: Find the common items and count how many times they appear in both lists
                    common_items = counter_answered & counter_correct  # This returns the intersection (common items with min counts)
                    
                    # Step 3: Get the total count of common items
                    unordered_counter = sum(common_items.values())
                
                    executive_sheet.write(data_start_row+max_column_length_correct_values+1, i, str(inorder_counter) + "," + str(unordered_counter), center_format)
                    bworksheet.write(20, i, str(unordered_counter) + '/' + str(np.sum(~np.isnan(correct_values_memoryworkauditverb[i]))))
                    total_unordered_counter += unordered_counter

                    new_score = max(common_count_list) if common_count_list!=[] else 0
                    # bworksheet.write(3, 1, str(total_unordered_counter) + '/' + str(sum(len(lst) for lst in correct_values_memoryworkauditverb)))
                    bworksheet.write(3, 1,  str(new_score) + '/' + str(len(correct_values_memoryworkauditverb[-1])))
                    executive_sheet.write(data_start_row+max_column_length_correct_values+2, 0, str(new_score), center_format)
            
            
            
            
            elif sheet_name == 'phonolrhymes':
                # Write the custom header for this sheet at the specified starting row and column
                header_text = custom_headers.get(sheet_name, sheet_name)
                executive_sheet.write(start_row, start_col, header_text)
                phonolrhymes_df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Write beautify header
                bworksheet.write(4, 0, 'Ρίμες')

                # Set data start row just below the header
                data_start_row = start_row

                # Define correct values for comparison for phonolrhymes
                correct_values_phonolrhymes = [2,1,2,4,3,1,3,4,3,2]
                
                answered_value = phonolrhymes_df.iloc[0, :].dropna().tolist()   # Offset by 1 as values start from A2
                
                
                # Handle NaN or special value (100) condition
                if(phonolrhymes_df.iloc[0, 0] == 100):
                    executive_sheet.write(data_start_row+1, start_col, 100, green_font)
                    bworksheet.write(4, 1, 100)
                    continue

                # Check if null exist in answers
                all_answers = phonolrhymes_df.iloc[0, :len(correct_values_phonolrhymes)]
                for ans in all_answers:
                    if isinstance(ans, float) and np.isnan(ans):
                        print("Null cells in ", sheet_name)
                        exit()
                        
                
                phonolrhymes_score = 0
                for i in range(len(correct_values_phonolrhymes)):
                    if(answered_value[i]==correct_values_phonolrhymes[i]):
                        phonolrhymes_score += 1
                  
                    if answered_value[i]!=correct_values_phonolrhymes[i]:
                        # Write incorrect value in red
                        executive_sheet.write(data_start_row+1, i, answered_value[i], red_font)
                    else:
                        # Write correct value as a number
                        executive_sheet.write_number(data_start_row+1, i, correct_values_phonolrhymes[i])  
                
                executive_sheet.write(data_start_row + 2, start_col, phonolrhymes_score)   
                print(f"Your correct score in phonolrhymes is: {phonolrhymes_score} out of 10")
                
                if phonolrhymes_df.iloc[0, 0] != 100:
                    bworksheet.write(4, 1, str(phonolrhymes_score) + '/' + str(len(correct_values_phonolrhymes)))
            
            
            
            
            elif sheet_name == 'phonolsyllables':
                # Write the custom header for this sheet at the specified starting row and column
                header_text = custom_headers.get(sheet_name, sheet_name)
                executive_sheet.write(start_row, start_col, header_text)
                phonolsyllables_df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Write beautify header
                bworksheet.write(5, 0, 'Σύλλαβες')

                # Set data start row just below the header
                data_start_row = start_row
                
                # Calculate how many examples I have in this test 
                column_names = list(phonolsyllables_df.loc[:, ~phonolsyllables_df.columns.str.contains('Unnamed')])
                total_examples = len(column_names)

                # Define correct values for comparison for phonolsyllables
                correct_values_phonolsyllables = [1,1,1,1,1,1,1,1,1,1]

                answered_value = phonolsyllables_df.iloc[0, :total_examples].dropna().tolist()   # Offset by 1 as values start from A2

                
                # Handle NaN or special value (100) condition
                if(phonolsyllables_df.iloc[0, 0] == 100):
                    executive_sheet.write(data_start_row+1, start_col, 100, green_font)
                    bworksheet.write(5, 1, 100)
                    continue
                
                # Check if null exist in answers
                all_answers = phonolsyllables_df.iloc[0, :len(correct_values_phonolsyllables)]
                for ans in all_answers:
                    if isinstance(ans, float) and np.isnan(ans):
                        print("Null cells in ", sheet_name)
                        exit()
                        

                phonolsyllables_score = answered_value.count(1)
                
                for i in range(len(correct_values_phonolsyllables)):
                        # Compare answered value with correct value
                        if answered_value[i] != correct_values_phonolsyllables[i]:
                            # Write incorrect value in red
                            executive_sheet.write(data_start_row+1, i, answered_value[i], red_font)
                        else:
                            # Write correct value as a number
                            executive_sheet.write_number(data_start_row+1, i, correct_values_phonolsyllables[i])
                
                executive_sheet.write(data_start_row+2, start_col, phonolsyllables_score)      
                print(f"Your correct score in phonolsyllables is: {phonolsyllables_score} out of 8")                  

                if phonolsyllables_df.iloc[0, 0] != 100:
                    bworksheet.write(5, 1, str(phonolsyllables_score) + '/' + str(len(correct_values_phonolsyllables)))




            elif sheet_name == 'phonolphonemes':
                # Write the custom header for this sheet at the specified starting row and column
                header_text = custom_headers.get(sheet_name, sheet_name)
                executive_sheet.write(start_row, start_col, header_text)
                phonolphonemes_df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Write beautify header
                bworksheet.write(6, 0, 'Φωνήματα')

                # Set data start row just below the header
                data_start_row = start_row

                # Calculate how many examples I have in this test 
                column_names = list(phonolphonemes_df.loc[:, ~phonolphonemes_df.columns.str.contains('Unnamed')])
                total_examples = len(column_names)

                # Define correct values for comparison for phonolphonemes
                correct_values_phonolphonemes = [1,1,1,1,1,1]
                
                answered_value = phonolphonemes_df.iloc[0, :total_examples].dropna().tolist()   # Offset by 1 as values start from A2

                # Handle NaN or special value (100) condition
                if(phonolphonemes_df.iloc[0, 0] == 100):
                    executive_sheet.write(data_start_row+1, start_col, 100, green_font)
                    bworksheet.write(6, 1, 100)
                    continue
                
                # Check if null exist in answers
                all_answers = phonolphonemes_df.iloc[0, :len(correct_values_phonolphonemes)]
                for ans in all_answers:
                    if isinstance(ans, float) and np.isnan(ans):
                        print("Null cells in ", sheet_name)
                        exit()
                        

                phonolphonemes_score = answered_value.count(1)
                
                # Iterate through the correct values and compare
                for i in range(len(correct_values_phonolphonemes)):
                        # Compare answered value with correct value
                        if answered_value[i] != correct_values_phonolphonemes[i]:
                            # Write incorrect value in red
                            executive_sheet.write(data_start_row+1, i, answered_value[i], red_font)
                        else:
                            # Write correct value as a number
                            executive_sheet.write_number(data_start_row+1, i, correct_values_phonolphonemes[i])
                                      
                executive_sheet.write(data_start_row+2, start_col, phonolphonemes_score)      
                print(f"Your correct score in phonolphonemes is: {phonolphonemes_score} out of 6")
                
                if phonolphonemes_df.iloc[0, 0] != 100:
                    bworksheet.write(6, 1, str(phonolphonemes_score) + '/' + str(len(correct_values_phonolphonemes)))   
                
                
                

            elif sheet_name == 'decodewordspseudo':
                # Write the custom header for this sheet at the specified starting row and column
                header_text = custom_headers.get(sheet_name, sheet_name)
                executive_sheet.write(start_row, start_col, header_text)
                decodewordspseudo_df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Write beautify header
                bworksheet.write(7, 0, 'Ανάγνωση Πραγματικών Λέξεων')
                bworksheet.write(8, 0, 'Ανάγνωση Ψευδολέξεων')

                # Set data start row just below the header
                data_start_row = start_row

                # Define correct values for comparison for decodewordspseudo
                realwords = ['ποίημα', 'λουλούδια', 'σκουπίδια', 'πρόσκληση', 'τήβεννος', 'αλάτια', 'δεσμεύω', 'εγκλείει', 'περιβάλλον', 'υπεύθυνος', 'εκπαίδευση', 'ηλεκτρική', 'βοοειδές', 'παυσίπονο', 'αρδευτικός', 'μετεγγραφές', 'επιχειρήματα', 'ταξιδεύουμε', 'δραστηριότητες', 'συμπληρώσουμε', 'ακαδημαϊκά', 'αυθαιρεσίες', 'σταφιδιασμένα', 'εκσυγχρονισμένος']
                pseudowords = ['άπηζε', 'θάισσε', 'μιούφαχο', 'οίφλατο', 'τζαλικιού', 'βριψίγκες', 'πουμπλάζει', 'μπρεστικά', 'νεπακίζω', 'ψειδικόμος', 'αυγετάλια', 'μπαθιλένα', 'ντιλεγοτιά', 'τραγγεθούμε', 'στραδημένος', 'χρουλαγκρίκι', 'ξερηχολόγος', 'οικιλειπιχάνων', 'ζουνιαλεκάει', 'κτουληνυσίζω', 'εργανουδάκια', 'αφαπληρωσμένο', 'ταζαμπρεγάγει', 'εγδατιντρόμενο']
                
                answered_value_realwords = decodewordspseudo_df.iloc[:, 0].dropna().tolist()   
                answered_realwords = decodewordspseudo_df.iloc[:, 3].dropna().tolist()   
                answered_value_pseudowords = decodewordspseudo_df.iloc[:, 1].dropna().tolist()   
                answered_pseudowords = decodewordspseudo_df.iloc[:, 4].dropna().tolist()  
                
                
                # Handle NaN or special value (100) condition
                if(decodewordspseudo_df['Ans11'][0] == 100 and decodewordspseudo_df['Ans21'][0] == 100):
                    executive_sheet.write(data_start_row+1, start_col, 100, green_font)
                    bworksheet.write(7, 1, 100)
                    bworksheet.write(8, 1, 100)
                    continue
                elif(decodewordspseudo_df['Ans11'][0] == 100 and decodewordspseudo_df['Ans21'][0] != 100):
                    executive_sheet.write(data_start_row+1, start_col, 100, green_font)
                    bworksheet.write(7, 1, 100)
                elif(decodewordspseudo_df['Ans11'][0] != 100 and decodewordspseudo_df['Ans21'][0] == 100):
                    executive_sheet.write(data_start_row+1, start_col+1, 100, green_font)
                    bworksheet.write(8, 1, 100)
                    
                # Check if null exist in answers
                all_answers = pd.concat([decodewordspseudo_df.iloc[:len(realwords), 3], decodewordspseudo_df.iloc[:len(pseudowords), 4]], ignore_index=True)
                for ans in all_answers:
                    if isinstance(ans, float) and np.isnan(ans):
                        print("Null cells in ", sheet_name)
                        exit()
                        
                
                real_words_score = -1 if (decodewordspseudo_df.iloc[1, 0] == 100) else 0
                pseudo_words_score = -1 if (decodewordspseudo_df.iloc[1, 1] == 100) else 0
                value_is_two = 0
                value_is_three = 0
                
                # Calculate correct real words
                if( decodewordspseudo_df['Ans11'][0] != 100 ):
                    for i in range(len(answered_value_realwords)):
                        if(answered_value_realwords[i]==1):
                            real_words_score += 1
                            executive_sheet.write(data_start_row+1+i, start_col, answered_value_realwords[i], center_format)
                            executive_sheet.write(data_start_row+1+i, start_col+3, answered_realwords[i], center_format)
                        elif(answered_value_realwords[i]=='T'):
                            value_is_two += 1
                            executive_sheet.write(data_start_row+1+i, start_col, answered_value_realwords[i], pink_font)
                            executive_sheet.write(data_start_row+1+i, start_col+3, answered_realwords[i], pink_font)
                        elif(answered_value_realwords[i]==3):
                            value_is_three += 1
                            executive_sheet.write(data_start_row+1+i, start_col, answered_value_realwords[i], darkblue_font)
                            executive_sheet.write(data_start_row+1+i, start_col+3, answered_realwords[i], darkblue_font)
                        elif(answered_value_realwords[i]==0):
                            executive_sheet.write(data_start_row+1+i, start_col, answered_value_realwords[i], red_font)
                            executive_sheet.write(data_start_row+1+i, start_col+3, answered_realwords[i], red_font)
                        else:
                            executive_sheet.write(data_start_row+1+i, start_col, answered_value_realwords[i], red_font)
                            executive_sheet.write(data_start_row+1+i, start_col+3, answered_realwords[i], red_font)                            
                
                    executive_sheet.write(data_start_row+1+i+1, start_col, real_words_score, center_format)
                    bworksheet.write(7, 1, str(real_words_score) + '/' + str(len(realwords)))
                    
                # Calculate correct preudo words
                if( decodewordspseudo_df['Ans21'][0] != 100 ):
                    for i in range(len(answered_value_pseudowords)):
                        if(answered_value_pseudowords[i]==1):
                            pseudo_words_score += 1
                            executive_sheet.write(data_start_row+1+i, start_col+1, answered_value_pseudowords[i], center_format)
                            executive_sheet.write(data_start_row+1+i, start_col+4, answered_pseudowords[i], center_format)
                        elif(answered_value_pseudowords[i]=='T'):
                            value_is_two += 1
                            executive_sheet.write(data_start_row+1+i, start_col+1, answered_value_pseudowords[i], pink_font)
                            executive_sheet.write(data_start_row+1+i, start_col+4, answered_pseudowords[i], pink_font)
                        elif(answered_value_pseudowords[i]==3):
                            value_is_three += 1
                            executive_sheet.write(data_start_row+1+i, start_col+1, answered_value_pseudowords[i], darkblue_font)
                            executive_sheet.write(data_start_row+1+i, start_col+4, answered_pseudowords[i], darkblue_font)
                        elif(answered_value_pseudowords[i]==0):
                            executive_sheet.write(data_start_row+1+i, start_col+1, answered_value_pseudowords[i], red_font)
                            executive_sheet.write(data_start_row+1+i, start_col+4, answered_pseudowords[i], red_font)
                        else:
                            executive_sheet.write(data_start_row+1+i, start_col+1, answered_value_pseudowords[i], red_font)
                            executive_sheet.write(data_start_row+1+i, start_col+4, answered_pseudowords[i], red_font)
                
                    executive_sheet.write(data_start_row+1+i+1, start_col+1, pseudo_words_score, center_format)
                    bworksheet.write(8, 1, str(pseudo_words_score) + '/' + str(len(pseudowords)))
                    
                value_is_two_str = "Error 2: " + str(value_is_two)
                value_is_three_str = "Error 3: " + str(value_is_three)
                executive_sheet.write(data_start_row+1+i+1, start_col+2+1, value_is_two_str, center_format)
                executive_sheet.write(data_start_row+1+i+1, start_col+3+1, value_is_three_str, center_format)    
                 
                # executive_sheet.write(data_start_row+1+i+1, start_col+2, value_is_two, center_format)
                # executive_sheet.write(data_start_row+1+i+1, start_col+3, value_is_three, center_format)            
                                  
                                 
                print(f"Your correct score in decoding real words is: {real_words_score} out of 24")
                print(f"Your correct score in decoding pseudo words is: {pseudo_words_score} out of 24")
                print(f"Your had {value_is_two} number 2 errors in decoding")
                print(f"Your had {value_is_three} number 3 errors in decoding")
                  
            
               
               
            elif sheet_name == 'visualorthogrecogn':
                # Write the custom header for this sheet at the specified starting row and column
                header_text = custom_headers.get(sheet_name, sheet_name)
                executive_sheet.write(start_row, start_col, header_text)
                visualorthogrecogn_df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Write beautify header
                bworksheet.write(9, 0, 'Οπτική Αναγνώριση (αναγραμματισμοί)')
                bworksheet.write(10, 0, 'Οπτική Αναγνώριση (ορθογραφία και τονισμός)')

                # Set data start row just below the header
                data_start_row = start_row
                
                # Calculate how many examples I have in this test and in which column is located the 'Ans21' 
                column_names = list(visualorthogrecogn_df.loc[:, ~visualorthogrecogn_df.columns.str.contains('Unnamed')])
                total_examples = len(column_names)
                part2_column_index = column_names.index('Ans21')
                
                # Define correct values for comparison for visualorthogrecogn
                correct_values_visualorthogrecogn_part1 = [2, 5, 2, 4, 5, 5, 3, 4, 5, 4]
                correct_values_visualorthogrecogn_part2 = [3, 2, 1, 5, 4, 3, 5, 2, 3, 2]
                
                sound_value_visualorthogrecogn = visualorthogrecogn_df.iloc[0, :total_examples].dropna().tolist()
                answered_value_visualorthogrecogn = visualorthogrecogn_df.iloc[1, :total_examples].dropna().tolist()

                
                # Handle NaN or special value (100) condition
                if(visualorthogrecogn_df['Ans11'][0] == 100 and visualorthogrecogn_df['Ans21'][0] == 100):
                    executive_sheet.write(data_start_row+1, start_col, 100, green_font)
                    bworksheet.write(9, 1, 100)
                    bworksheet.write(10, 1, 100)
                    continue
                elif(visualorthogrecogn_df['Ans11'][0] == 100 and visualorthogrecogn_df['Ans21'][0] != 100):
                    executive_sheet.write(data_start_row+1, start_col, 100, green_font)
                    bworksheet.write(9, 1, 100)
                elif(visualorthogrecogn_df['Ans11'][0] != 100 and visualorthogrecogn_df['Ans21'][0] == 100):
                    executive_sheet.write(data_start_row+1, part2_column_index, 100, green_font)
                    bworksheet.write(10, 1, 100)
                        
                
                sound_correct_orthogrecogn_score_part1 = -1 if (visualorthogrecogn_df.iloc[1, 0] == 100) else 0
                answered_correct_orthogrecogn_score_part1 = -1 if (visualorthogrecogn_df.iloc[1, 0] == 100) else 0
                sound_correct_orthogrecogn_score_part2 = -1 if (visualorthogrecogn_df.iloc[1, 0] == 100) else 0
                answered_correct_orthogrecogn_score_part2 = -1 if (visualorthogrecogn_df.iloc[1, 0] == 100) else 0
                
                # Iterate through each cell in correct_values_visualorthogrecogn and compare
                
                # # # PART 1
                for i in range(len(correct_values_visualorthogrecogn_part1)):
                    if(sound_value_visualorthogrecogn[i]==1):
                        sound_correct_orthogrecogn_score_part1 += 1
                        executive_sheet.write(data_start_row+1, start_col+i, sound_value_visualorthogrecogn[i], center_format)
                    elif(sound_value_visualorthogrecogn[i]==0):
                        executive_sheet.write(data_start_row+1, start_col+i, sound_value_visualorthogrecogn[i], red_font)
                    elif(sound_value_visualorthogrecogn[i]=='T'):
                        executive_sheet.write(data_start_row+1, start_col+i, sound_value_visualorthogrecogn[i], pink_font)
                    else:
                        executive_sheet.write(data_start_row+1, start_col+i, sound_value_visualorthogrecogn[i], red_font)
                        
                    if(answered_value_visualorthogrecogn[i]==correct_values_visualorthogrecogn_part1[i]):
                        answered_correct_orthogrecogn_score_part1 += 1
                        executive_sheet.write(data_start_row+2, start_col+i, answered_value_visualorthogrecogn[i], center_format)
                    elif(answered_value_visualorthogrecogn[i]!=correct_values_visualorthogrecogn_part1[i]):
                        executive_sheet.write(data_start_row+2, start_col+i, answered_value_visualorthogrecogn[i], red_font)
                            
                
                # # # PART 2
                for i in range(len(correct_values_visualorthogrecogn_part2)):
                    if(sound_value_visualorthogrecogn[i+part2_column_index]==1):
                        sound_correct_orthogrecogn_score_part2 += 1
                        executive_sheet.write(data_start_row+1, start_col+part2_column_index+i, sound_value_visualorthogrecogn[i+part2_column_index], center_format)
                    elif(sound_value_visualorthogrecogn[i+part2_column_index]==0):
                        executive_sheet.write(data_start_row+1, start_col+part2_column_index+i, sound_value_visualorthogrecogn[i+part2_column_index], red_font)
                    elif(sound_value_visualorthogrecogn[i+part2_column_index]=='T'):
                        executive_sheet.write(data_start_row+1, start_col+part2_column_index+i, sound_value_visualorthogrecogn[i+part2_column_index], pink_font)
                    else:
                        executive_sheet.write(data_start_row+1, start_col+part2_column_index+i, sound_value_visualorthogrecogn[i+part2_column_index], red_font)
                        
                    if(answered_value_visualorthogrecogn[i+part2_column_index]==correct_values_visualorthogrecogn_part2[i]):
                        answered_correct_orthogrecogn_score_part2 += 1            
                        executive_sheet.write(data_start_row+2, start_col+part2_column_index+i, answered_value_visualorthogrecogn[i+part2_column_index], center_format)
                    elif(answered_value_visualorthogrecogn[i+part2_column_index]!=correct_values_visualorthogrecogn_part2[i]):
                        executive_sheet.write(data_start_row+2, start_col+part2_column_index+i, answered_value_visualorthogrecogn[i+part2_column_index], red_font)

                executive_sheet.write(data_start_row+3, start_col, str(sound_correct_orthogrecogn_score_part1) + ", " + str(answered_correct_orthogrecogn_score_part1), center_format)   
                executive_sheet.write(data_start_row+3, start_col+1, str(sound_correct_orthogrecogn_score_part2) + ", " + str(answered_correct_orthogrecogn_score_part2), center_format)           
                
                if visualorthogrecogn_df['Ans11'][0] != 100:
                    bworksheet.write(9, 1, str(answered_correct_orthogrecogn_score_part1) + '/' + str(len(correct_values_visualorthogrecogn_part1)))
                if visualorthogrecogn_df['Ans21'][0] != 100:
                    bworksheet.write(10, 1, str(answered_correct_orthogrecogn_score_part2) + '/' + str(len(correct_values_visualorthogrecogn_part2)))
                
                
            elif sheet_name == 'decodesentences':
                # Write the custom header for this sheet at the specified starting row and column
                header_text = custom_headers.get(sheet_name, sheet_name)
                executive_sheet.write(start_row, start_col, header_text)
                decodesentences_df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Write beautify header
                bworksheet.write(11, 0, 'Κατανόηση Προτάσεων')

                # Set data start row just below the header
                data_start_row = start_row
                
                # Calculate how many examples I have in this test 
                column_names = list(decodesentences_df.loc[:, ~decodesentences_df.columns.str.contains('Unnamed')])
                total_examples = len(column_names)

                # Define correct values for comparison for decodesentences
                if(subno in range(14301, 14437)): # APOKORONAS
                    correct_values_decodesentences = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                else:
                    correct_values_decodesentences = [2, 3, 2, 1, 3, 3, 1, 2, 3, 1]
                
                answered_value = decodesentences_df.iloc[0, :total_examples].dropna().tolist()   # Offset by 1 as values start from A2

                
                # Handle NaN or special value (100) condition
                if(decodesentences_df['Ans11'][0] == 100):
                    executive_sheet.write(data_start_row+1, start_col, 100, green_font)
                    bworksheet.write(11, 1, 100)
                    continue 
                
                sentences_score = -1 if (decodesentences_df.iloc[0, 0] == 100) else 0
                
                # Iterate through the correct values and compare
                for i in range(len(correct_values_decodesentences)):
                    if(answered_value[i]==correct_values_decodesentences[i]):
                        sentences_score += 1
                        executive_sheet.write(data_start_row+1, start_col+i, answered_value[i], center_format)
                    else:
                        executive_sheet.write(data_start_row+1, start_col+i, answered_value[i], red_font)
                        
                
                executive_sheet.write(data_start_row + 2, start_col, sentences_score, center_format)  
                 
                if decodesentences_df.iloc[0, 0] != 100:          
                    bworksheet.write(11, 1, str(sentences_score) + '/' + str(len(correct_values_decodesentences)))
            
               
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

    
    
    bworkbook.close()
    auto_adjust_column_width_xlsx(beautify_filepath, beautify_sheet_name)
    export_to_pdf(beautify_filepath, sub_path, f"beautify_executive_sheet_{subno}.pdf")
    
    print(f"Executive sheet saved as {output_path}")
     # Export the Excel sheet to PDF
    export_to_pdf(output_path, sub_path, f"executive_sheet_{subno}.pdf")
    
    
def age_years_months_decimal(subno, filepath):
    dob_str = find_dob(subno, filepath)
    ref_str = find_date_executed(subno, filepath)
    
    # Convert strings → datetime
    if dob_str!='':
        dob = datetime.strptime(dob_str, "%d/%m/%Y")
    else:
        return dob_str
    ref = datetime.strptime(ref_str, "%d/%m/%Y")

    # ---- Years ----
    years = ref.year - dob.year
    if (ref.month, ref.day) < (dob.month, dob.day):
        years -= 1

    # ---- Months ----
    months = ref.month - dob.month
    if ref.day < dob.day:
        months -= 1
    months = months % 12

    # Return as decimal (Y.MM)
    return float(f"{years}.{months}")



def identify_raven_score(subno, main_folder, sub_path, initial_score):
    # Find child's year 
    child_year = age_years_months_decimal(subno, sub_path)
    
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
    
    

# Helper function to convert Excel cell (e.g., 'A1') to row and column indices
def convert_cell_to_index(cell):
    col = ord(cell[0].upper()) - ord('A')  # Convert 'A' to 0, 'B' to 1, etc.
    row = int(cell[1:]) - 1  # Convert '1' to 0, '2' to 1, etc.
    return row, col



# Main function to let the user select the file path and save directory
def create_executive_sheet_main(main_folder, start, end):
  
    # Define sublist of subject numbers
    sublist = []
    for i in range(start, end+1):  # +1 because range is exclusive at the end
        sublist.append(i)
    
    # Define the range of subject numbers
    for subno in sublist: 
        # Define subject's path
        sub_path = main_folder + 'subject_' + str(subno) + '/'
        if not os.path.exists(sub_path):
            print(f"Subject path does not exist: {sub_path}. Skipping subject number: {subno}")
            continue
        
        # Define file path for each subject number
        file_path = ''
        for file in glob.glob(sub_path + '*.xlsx', recursive=True):
            filename = file.split("\\")[-1]
            if filename.startswith(str(subno)):
                file_path = sub_path + filename
                break
        
        # Find date tests executed
        start_date = find_date_executed(subno, sub_path) #"28/11/2025"
        
        
        # Print a message to indicate the current subject being processed
        print(f"Processing subject number: {subno}")
        
        
        # Define the cell ranges to extract for each sheet
        sheet_ranges = {
            'raven': ['A2:A37'],  
            'memoryshortauditverb': ['A2:Q3'],      
            'memoryworkauditverb': ['A2:E8'],      
            'phonolrhymes': ['A2:3'],      
            'phonolsyllables': ['A2:J3'],      
            'phonolphonemes': ['A2:E3'],      
            'decodewordspseudo': ['A2:E25'],      
            'visualorthogrecogn': ['A2:T3'],      
            'decodesentences': ['A2:J2'],            
        }

        # Define custom headers for each sheet
        custom_headers = {
            'raven': 'Raven Score',
            'memoryshortauditverb': 'Memory Short Audit Verb (Black:True, Red: False)',
            'memoryworkauditverb': 'Memory Work Audit Verb (Black:True, Red: False)',
            'phonolrhymes': 'Phonological Rhymes (Black:True, Red: False)',
            'phonolsyllables': 'Phonological Syllables (1:True, 0: False, 2nd row: subject`s answer)',
            'phonolphonemes': 'Phonological Phonemes (1:True, 0: False, 2nd row: subject`s answer)',
            'decodewordspseudo': 'Decode Words Pseudo (1:True, 0: False)',
            'visualorthogrecogn': 'Visual Orthographic Rec. (1st row: 1:Sounded right, 0:False // 2nd row:answers)',
            'decodesentences': 'Decode Sentences (Black:True, Red: False)',
        }

        # Define specific cell positions for each sheet in the executive sheet
        cell_positions = {
            'raven': (0, 0),
            'memoryshortauditverb': (5, 0),
            'memoryworkauditverb': (17, 0),
            'phonolrhymes': (29, 0),
            'phonolsyllables': (34, 0),
            'phonolphonemes': (39, 0),
            'decodewordspseudo': (44, 0),
            'visualorthogrecogn': (73, 0),
            'decodesentences': (79, 0),
        }
        
       # Check if the file exists before processing
        if os.path.exists(file_path):
            print(f"Processing subject number: {subno}")
            extract_from_sheet(main_folder, sub_path, file_path, sheet_ranges, custom_headers, cell_positions, start_date, subno)
        else:
            print(f"His answers file not found into his folder,for subject number: {subno}. Skipping...")
        
        # Optional: You can add a brief delay if needed to prevent issues with large batch processing
        # time.sleep(1)  # Uncomment if delay is desired
