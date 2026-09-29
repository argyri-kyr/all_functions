


from win32com import client as win32
import os
import sys


def export_to_pdf(excel_path, save_directory, pdf_filename):
    try:
        # Validate input paths
        if not os.path.isfile(excel_path):
            raise FileNotFoundError(f"The Excel file does not exist: {excel_path}")
        
        if not os.path.isdir(save_directory):
            os.makedirs(save_directory)  # Create the directory if it doesn't exist
        
        # Specify the PDF file path
        pdf_path = os.path.join(save_directory, pdf_filename)
        
        # Check if PDF already exists and try to delete it
        if os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
            except Exception as delete_error:
                raise Exception(f"Could not delete the old PDF. Check if it is open some where.")

        
        # Initialize Excel application
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False  # Run Excel in the background
        excel.DisplayAlerts = False  # Suppress alerts

        # Open the Excel file
        workbook = excel.Workbooks.Open(excel_path)

        # Export the workbook to PDF
        workbook.ExportAsFixedFormat(0, pdf_path)

        print(f"PDF successfully saved at {pdf_path}")

    except Exception as e:
        print(f"An error occurred during PDF export: {e}")
        print("Exiting....")
        sys.exit()
    
    finally:
        # Ensure proper cleanup
        try:
            if 'workbook' in locals():
                workbook.Close(SaveChanges=False)
            if 'excel' in locals():
                excel.Quit()
        except Exception as cleanup_error:
            print(f"An error occurred during cleanup: {cleanup_error}")
