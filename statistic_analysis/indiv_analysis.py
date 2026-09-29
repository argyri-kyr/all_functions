

import xlsxwriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from tqdm import tqdm


from collect_population_results import collect_population_results
from plot_graphs import plot_results_hist
from define_recommendations import define_recommendation
from calculate_stats import calculate_stats
from define_answers import define_answers
from build_excel_report import build_excel_report_main
from excel_to_pdf_one_page_per_sheet import excel_to_pdf_one_page_per_sheet
from auto_adjust_column_width_xlsx_v2 import auto_adjust_column_width_xlsx_v2
from define_score import define_score
from generate_beautify_report_per_page import beautify_pdf_main
from draw_cover_page import draw_cover_page
from define_titles import define_titles


def indiv_analysis(subno, sub_dataframes, class_mapping, target_class, exercises, subjectpath, plotspath, font_sizes_pdf):
    # ---- CREATE EXCEL ONCE ----
    report_excel_path = f"{subjectpath}/individual_analysis_{subno}.xlsx"
    workbook = xlsxwriter.Workbook(report_excel_path) 
    sheets = []

    # ---- CREATE PDF ONCE ----
    report_pdf_path = f"{subjectpath}/individual_analysis_{subno}.pdf"
    c = canvas.Canvas(report_pdf_path, pagesize=A4)

    # ---- PAGE 1: COVER ----
    draw_cover_page(c, subno)

    # ---- PAGE 2+: EXERCISES ----
    
    # ---- VARIABLES ----
    recommendations = {}
    scores = {}
    stats = {}
    answers = {}
    for index, exercise in enumerate(tqdm(exercises.keys(), desc="Processing exercises")):
        
        results_collection1, results_collection2 = collect_population_results(sub_dataframes, exercises, exercise)
        
        figurepath1, figurepath2 = plot_results_hist(subno, exercises, exercise, results_collection1, results_collection2, plotspath)
        
        score = define_score(subno, exercises, exercise, sub_dataframes, results_collection1, results_collection2)
        scores[exercise] = score
        
        
        recommendation = define_recommendation(subno, exercises, exercise, sub_dataframes, results_collection1, results_collection2)
        recommendations[exercise] = recommendation
    

        stat = calculate_stats(subno, class_mapping, target_class, exercises, exercise, results_collection1, results_collection2)
        stats[exercise] = stat


        answer = define_answers(subno, sub_dataframes, exercises, exercise, results_collection1, results_collection2)
        if(answer==None):  
            print(f"\n\n No answers defined for exercise {exercise}. Probably '?' exists in the data.\n")
            # sys.exit()
            return subno
        answers[exercise] = answer
        
        
        sheet_name = build_excel_report_main(subno, exercise, workbook, results_collection1, results_collection2, figurepath1, figurepath2, score, recommendation, stat, answer)
        sheets.append(sheet_name)
        
        title = define_titles(exercise)
        beautify_pdf_main(subno, exercise, title, results_collection1, results_collection2, c, figurepath1, figurepath2, recommendation, stat, score, answer)
        
        
    workbook.close()
    auto_adjust_column_width_xlsx_v2(report_excel_path)
    # excel_to_pdf_one_page_per_sheet(report_excel_path, report_pdf_path, font_sizes_pdf)

    # ---- CLOSE PDF ONCE ----
    c.save()

    print("✅ PDF created successfully for subno = ", subno)
    print()
    
 
    
    

