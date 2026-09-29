
import pandas as pd

# # Load the Excel file
# file_path = 'C:/_Iro_analysis_tobii7_HD/individual/subject_13502/13502.xlsx'
# xls = pd.ExcelFile(file_path)

# # Load the specific sheet, assuming the first row contains the headers
# df1 = pd.read_excel(xls, 'memoryshortauditverb', header=0)

# # Check what columns are present in the dataframe
# print("Available columns:", df1.columns)

# # Function to extract columns based on the header
# def extract_columns_by_header(header):
#     # Check if the header exists in the dataframe
#     if header in df1.columns:
#         # Find the index of the given header
#         header_index = df1.columns.get_loc(header)
        
#         # Extract the next three columns starting from the header index
#         columns = df1.iloc[:, header_index:header_index + 3].reset_index(drop=True)
#         return columns
#     else:
#         raise ValueError(f"Header '{header}' not found in the data.")

# # Example usage: Extract columns for 'Ans11' and 'Ans12'
# Ans11_columns = extract_columns_by_header('Ans11').dropna()
# Ans12_columns = extract_columns_by_header('Ans12')

file_path = 'C:/_Iro_analysis_tobii7_HD/individual/subject_13502/13502.xlsx'
df = pd.read_excel(file_path, 'memoryshortauditverb') # using first and second row as headers (pandas count rows from 0).

totalDataA11 = []
numberCol = df.columns.get_loc('Ans11')

totalCols = [numberCol+i for i in range(3)]
for i in totalCols:
    column = df.iloc[:, i].dropna().tolist()
    totalDataA11.append(column)

correctIndecesA11 = []
for i in range(len(totalDataA11[0])):
    if(totalDataA11[2][i]==1):
        correctIndecesA11.append(int(totalDataA11[0][i]))
        
print(totalDataA11)