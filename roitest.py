

import pandas as pd
import xlsxwriter
import os


from globalVars import folder1, textends, textpos
from matplotlib import patches, pyplot as plt


def make_roiboundsextra(text, pages):
    # texts = ['efeyreseis', 'island', 'morning', 'olympia', 'psaras', 'visit', 'zebra', 'zoo']
    
    roisdata = pd.read_excel(folder1 + 'texts/' + text + textends + '/ΣΦ2 ' + text + '.xlsx', sheet_name="Sheet1")
    
    previndex = 0
    for i in range(pages):
        roisdata = pd.read_excel(folder1 + 'texts/' + text + textends + '/py/ROIbounds/mytext.page_' + str(i+1) + '.ROIbounds.xlsx', sheet_name="Sheet1")
        roix = roisdata.iloc[:,0].dropna().to_list()
        roiy = roisdata.iloc[:,1].dropna().to_list()
        width = roisdata.iloc[:,2].dropna().to_list()
        height = roisdata.iloc[:,3].dropna().to_list()
        
        syllabes = pd.read_excel(folder1 + 'texts/' + text + textends + '/ΣΦ2 visit.xlsx', sheet_name="Sheet1")
        numberofsyllabes = syllabes.iloc[:,2].dropna().to_list()
        numberofsyllabes = numberofsyllabes[previndex: previndex+len(roix)]
        
        headers = ["X", "Y", "WIDTH", "HEIGHT", "Αριθμός συλλαβών"]
        
        workbook =  xlsxwriter.Workbook(folder1 + 'texts/' + text + '_1920/roiboundsextra' + str(i+1) + '.xlsx')
        worksheet = workbook.add_worksheet()
        
        worksheet.write_row(0, 0, headers)
        worksheet.write_column(1, 0, roix)
        worksheet.write_column(1, 1, roiy)
        worksheet.write_column(1, 2, width)
        worksheet.write_column(1, 3, height)
        worksheet.write_column(1, 4, numberofsyllabes)
        
        previndex += len(roix)
        
        workbook.close()
    



def drawExtraRect(text, pages, cutoff1, cutoff2, cutoff3):
    for pageno in range(pages):
        f, ax = plt.subplots(1)
        f.set_figwidth(9)
        f.set_figheight(7)
        
        imagepath = folder1 + textpos + text + textends + '/Slide' + str(pageno+1) + '.PNG'
        img = plt.imread(imagepath)
        plt.imshow(img)
        plt.axis('off')
        
        roisdataextra = pd.read_excel(folder1 + 'texts/' + text + '_1920/roiboundsextra' + str(pageno+1) + '.xlsx', sheet_name="Sheet1")
        roix = roisdataextra.iloc[:,0].dropna().to_list()
        roiy = roisdataextra.iloc[:,1].dropna().to_list()
        roiwidth = roisdataextra.iloc[:,2].dropna().to_list()
        roiheight = roisdataextra.iloc[:,3].dropna().to_list()
        numberofsyllabes = roisdataextra.iloc[:,4].dropna().to_list()
        
        for j in range(len(roix)):
            roi_x = float(roix[j])
            roi_y = float(roiy[j])
            
            if( j<len(roix)-1 and roi_y!=float(roiy[j+1]) ):
                roiwidth[j] -= cutoff1
            
            if( j==len(roix)-1 ):
                roiwidth[-1] -= cutoff2
            
            if( j==0 ):
                roi_x += cutoff3
                roiwidth[j] -= cutoff3
                
            if( 2<j<len(roix)-1 and roi_y!=float(roiy[j-1]) ):
                roi_x += cutoff3
                roiwidth[j] -= cutoff3
                
            x_step = roiwidth[j]/numberofsyllabes[j]
                
            # for k in range(numberofsyllabes[j]):
            #     rect = patches.Rectangle((roi_x, roiy[j]), x_step, roiheight[j], edgecolor='r', facecolor="none")
            #     ax.add_patch(rect)
            #     roi_x += x_step
            
            plt.vlines(x=roi_x, ymin=roiy[j], ymax=roiy[j]+roiheight[j], colors='green', ls=':', lw=4)

                   
        for j in range(len(roix)):
            rect = patches.Rectangle((roix[j], roiy[j]), roiwidth[j], roiheight[j], edgecolor='r', facecolor="none")
            ax.add_patch(rect)
                
        
        plt.savefig(folder1+ textpos + text + textends + '/Slidegraph_roi_syllabes' + str(pageno+1) + '.jpg')
        # plt.show()
        plt.close('all')



def main_draw_roi_extra():
    texts = ['visit']
    
    #cut some pixels in the end of the word, in order to reduce pixels to fit the rectangle within the word
    cutoff1 = 80
    cutoff2 = 100
    catoff3 = 40
    
    for text in texts:
        
        pagesfile = open(folder1 + "texts/" + text + textends + "/py/pages/pages.txt", "r")
        pages = int(pagesfile.read(1))
        
        for pageno in range(pages):
            if not os.path.exists(folder1 + 'texts/' + text + '_1920/roiboundsextra' + str(pageno+1) + '.xlsx'):
                make_roiboundsextra(text, pages)
                break
        
        drawExtraRect(text, pages, cutoff1, cutoff2, catoff3)
            
                     
      

                    
main_draw_roi_extra()         
            