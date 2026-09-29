

import pandas as pd
import xlsxwriter


from globalVars import folder1, textends


def findroiperline(text, pageno):
    roiboundspath = folder1 + 'texts/' + text + '/py/ROIbounds/mytext.page_' + str(pageno) + '.ROIbounds.xlsx'
    roiboundsdata = pd.read_excel(roiboundspath)
    
    roisdata = roiboundsdata.iloc[:,1].values.tolist()
    
    # find what is the first roi in this page, in order to start to count from this roi
    roistartpath = folder1 + 'texts/' + text + '/py/mytext/page(' + str(pageno) + ')/ROIstart/ROIstart.xlsx'
    roistartdata = pd.read_excel(roistartpath, header=None)
    roistart = roistartdata.iloc[:,0].values.tolist()[0]
    
    # 1st element:roi, 2nd index:line belonds the roi
    
    roisLines = {roistart:1}  # add the first roi
    line = 1
    for i in range(1, len(roisdata)):
        if(roisdata[i]==roisdata[i-1]):
            roisLines[roistart+i] = line
        else:
            line+=1
            roisLines[roistart+i] = line

    # create Rois_Lines.xlsx
    workbookpath = folder1 + 'texts/' + text + '/py/mytext/page(' + str(pageno) + ')/Rois_Lines.xlsx'
    workbook = xlsxwriter.Workbook(workbookpath)
    worksheet = workbook.add_worksheet()
    row = 0
    for key in roisLines:
        worksheet.write(row, 0, key)
        worksheet.write(row, 1, roisLines[key])
        row+=1
        
    workbook.close()
    