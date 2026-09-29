


import glob
import os
from openpyxl import load_workbook


# Main function to let the user select the file path and save directory
def main():
    
    ############## Needed initial info #############
    
    # main_folder = 'E:/_MyPatients/'
    main_folder = 'P:/'
    # main_folder = 'E:/_MyPatients/'
    # main_folder = 'C:/_Iro_analysis_tobii7_HD/individual/'
    

       
    # For one or many subjects
    start = 13543
    end = 13543
    sublist = []
    ##################################################
    
    for i in range(start, end+1):  # +1 because range is exclusive at the end
        sublist.append(i)
    
   
    for subno in sublist:  
        file_path = ''
        for file in glob.glob(main_folder + 'subject_' + str(subno) + '/'+ '*.xlsx', recursive=True):
            filename = file.split("\\")[-1]
            if filename.startswith(str(subno)):
                file_path = main_folder + 'subject_' + str(subno) + '/' + filename
                break
        
        # Define the directory to save results
        save_directory = main_folder + 'subject_' + str(subno) + '/'
        
        
        # Print a message to indicate the current subject being processed
        print(f"Processing subject number: {subno}")
        
       # Check if the file exists before processing
        if os.path.exists(file_path):
            wb = load_workbook(file_path)
            ws = ws = wb["decodewordspseudo"]
            ws["A1"] = "Ans11"
            ws["B1"] = "Ans21"
            
            wb.save(file_path)


main()