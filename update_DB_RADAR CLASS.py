import pandas as pd
import os


def update_radar_class(file_name, sheet_name):
    # 1. Read the Excel file
    try:
        df = pd.read_excel(file_name, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit()
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        exit()

    # 2. Define the exact replacements
    replacements = {
        'Α': 'ae',
        'Β': 'be',
        'Γ': 'ge',
        'Δ': 'de',
        'Ε': 'ee',
        'ΣΤ': 'ste',
        'Α ΓΥΜΝ': 'ag',
        'Β ΓΥΜΝ': 'bg',
        'Γ ΓΥΜΝ': 'gg',
    }

    # 3. Check if the 'RADAR CLASS' column exists and apply replacements
    column_name = 'RADAR CLASS'

    if column_name in df.columns:
        print(f"Modifying '{column_name}' column...")
        
        # Apply the replacements
        df[column_name] = df[column_name].replace(replacements)

        # 4. Save the modified DataFrame back to the ORIGINAL file
        # This overwrites the existing file but preserves all columns/rows
        # on the specified sheet.
        
        # If the file has ONLY ONE sheet, this simple overwrite is fine:
        df.to_excel(file_name, sheet_name=sheet_name if isinstance(sheet_name, str) else None, index=False)
        
        print(f"\n✅ Success! The file '{file_name}' has been updated.")
        
    else:
        print(f"\n⚠️ Warning: Column '{column_name}' not found in sheet '{sheet_name}'. No changes were made.")



def main():
    main_folder = 'Q:/'
    file_name = main_folder + 'APOKORONAS DB_v2.xlsx'
    sheet_name = 'Sheet1'
    update_radar_class(file_name, sheet_name)

main()