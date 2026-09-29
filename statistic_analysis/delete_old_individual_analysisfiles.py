

import os

def delete_old_individual_analysisfiles(subno, subjectpath):
    # Delete older analysis files
    report_excel_path = f"{subjectpath}/individual_analysis_{subno}.xlsx"
    report_pdf_path = f"{subjectpath}/individual_analysis_{subno}.pdf"
    if os.path.exists(report_excel_path):
        os.remove(report_excel_path)
    if os.path.exists(report_pdf_path):
        os.remove(report_pdf_path)