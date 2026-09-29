


from globalVars import folder1, folder2, textends


def findgazesmaxwindowlen(sub1, text, file):
    pagesfile = open(folder1 + "texts/" + text + textends + "/py/pages/pages.txt", "r")
    pages = int(pagesfile.read(1))
    
    totaldataperpage = []
    for pagenumber in range(1, pages+1):
        with open(folder1 + folder2 + '/subject_' + str(sub1) + '/' + file + '/py/gazes_page' + str(pagenumber) + '.txt', 'r') as fp:
            linesperpage = len(fp.readlines())
        totaldataperpage.append(linesperpage)
    
    return max(totaldataperpage)