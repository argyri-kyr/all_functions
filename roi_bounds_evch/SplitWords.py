
import xlrd
from globalVars import folder1, textpos
import xlsxwriter

# Python program to read
# file word by word

# Sinarthsh opou upologizei kai epistrefei ta dedomena: allwordspure, letternumberpure, wordSnumber, allwordinfo
def split(text):
    number = 0
    purestr = ""
    allwords = []
    allwordspure = []
    letternumberpure = []
    wordSnumber = []
    allwordinfo = []    # lista opou ta stoixeia ths einai epimerous listes opoy periexoun ws prwto stoixeio th lexi, ws deftero stoixeio to arithmo ths lexis kai ws trito stoixeio ton arithmo twn grammatwn ths lexis



    # Make the allwords list which contains the words with punctuation.Also store all the text into a string ,in order to use it below to find allwordspure list
    with open(folder1 + textpos + text + '/alltext.txt','r') as file:      # opening the text file
        for line in file:                                                   # reading each line	
            for word in line.split():                                       # reading each word
                purestr += " " + word                                       #string to keep all text, in order to make a split punctuation below, in split_into_words(line) function
                allwords.append(word)                                       #allwords list to keep all words with punctuation

    # make mytext.allwords
    path = folder1 + textpos + text +'/py/mytext/allwords.xlsx'
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    for i in range(len(allwords)):
        worksheet.write(i, 0, allwords[i])

    workbook.close()


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    # Make the allwordspure list which contains the list with words without punctuation
    punc = '''!()-[]{};:'"\,<>«».“/”?@#$%^&*_~'''
    allwordspure = allwords
    for i in range(len(allwordspure)):
        for ele in allwordspure[i]:
            if ele in punc:
                allwordspure[i] = allwordspure[i].replace(ele, "")
    
    # make mytext.allwordspure
    path = folder1 + textpos + text +'/py/mytext/allwordspure.xlsx'
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    for i in range(len(allwordspure)):
        worksheet.write(i, 0, allwordspure[i])
    
    workbook.close()


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    # Make the letternumberpure list which contains the number of letters in words without punctuation,Also i will make wordSnumber list whick store word's number
    for i in range(len(allwordspure)):
        length = 0
        number += 1
        wordSnumber.append(number)

        for j in range(len(allwordspure[i])):
            if(allwordspure[i][j] !=  '’'):
                length += 1
        
        letternumberpure.append(length)
    
    # make mytext.letternumberpure
    path = folder1 + textpos + text +'/py/mytext/letternumberpure.xlsx'
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    for i in range(len(letternumberpure)):
        worksheet.write(i, 0, letternumberpure[i])
    
    workbook.close()

    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    # Here i will make the allwordinfo list
    for i in range(len(allwordspure)):
        allwordinfo.append( [ allwordspure[i], wordSnumber[i], letternumberpure[i] ] )


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    max = 0
    for i in range(len(allwordspure)):
        if( letternumberpure[i] > max ):
            max = letternumberpure[i]

    letterwords = []

    for i in range(max):
        letterwords.append([])

    for i in range(len(letternumberpure)):
        position = letternumberpure[i]-1
        letterwords[position] += [ wordSnumber[i] ]
    
    # make mytext.values
    path = folder1 + textpos + text +'/py/mytext/letterwords.xlsx'
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    for i in range(len(letterwords)):
        worksheet.write(0, i, "letters_" + str(i+1))
        worksheet.write_column(1, i, letterwords[i])

    workbook.close()

    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    
    # Total Wordnumber in all Text
    wordnumber = len(wordSnumber)

    # make mytext.wordnumber
    wordnumbertxt = folder1 + textpos + text + '/py/mytext/wordnumber.txt'
    wordnumberfile = open(wordnumbertxt, 'w')
    wordnumberfile.write(str(wordnumber))
    wordnumberfile.close()

    
    return allwords, allwordspure, letternumberpure, wordSnumber, wordnumber, allwordinfo


def shortbyletternumber(text, allwordinfo, astr, bstr, cstr, dstr):

    chara, charb, charc, chard = [], [], [], []
    charaindex, charbindex, charcindex, chardindex = [], [], [], []

    for i in range(len(allwordinfo)):
        if( allwordinfo[i][2] <= int(astr[-1]) ):
            chara.append(allwordinfo[i][0])
            charaindex.append(int(allwordinfo[i][1]))

        elif( int(bstr[0]) <= allwordinfo[i][2] <= int(bstr[-1]) ):
            charb.append(allwordinfo[i][0])
            charbindex.append(int(allwordinfo[i][1]))

        elif( int(cstr[0]) <= allwordinfo[i][2] <= int(cstr[-1]) ):
            charc.append(allwordinfo[i][0])
            charcindex.append(int(allwordinfo[i][1]))

        elif( allwordinfo[i][2] >= int(dstr[-1]) ):
            chard.append(allwordinfo[i][0])
            chardindex.append(int(allwordinfo[i][1]))


    # make mytext.astr_bstr_cstr_dstr
    path = folder1 + textpos + text +'/py/mytext/astr_bstr_cstr_dstr.xlsx'
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "astr")
    worksheet.write(1, 0, astr)
    worksheet.write(0, 1, "bstr")
    worksheet.write(1, 1, bstr)
    worksheet.write(0, 2, "cstr")
    worksheet.write(1, 2, cstr)
    worksheet.write(0, 3, "dstr")
    worksheet.write(1, 3, dstr)
    workbook.close()

    # make mytext.chara_charb_charc_chard
    path = folder1 + textpos + text +'/py/mytext/chara_charb_charc_chard.xlsx'
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "chara")
    worksheet.write_column(1, 0, charaindex)
    worksheet.write(0, 1, "charb")
    worksheet.write_column(1, 1, charbindex)
    worksheet.write(0, 2, "charc")
    worksheet.write_column(1, 2, charcindex)
    worksheet.write(0, 3, "chard")
    worksheet.write_column(1, 3, chardindex)
    workbook.close()


    # make mytext.chara
    path = folder1 + textpos + text +'/py/mytext/chara.xlsx'
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    worksheet.write_column(0, 0, chara)
    worksheet.write_column(0, 1, charaindex)
    workbook.close()

    # make mytext.charb
    path = folder1 + textpos + text +'/py/mytext/charb.xlsx'
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    worksheet.write_column(0, 0, charb)
    worksheet.write_column(0, 1, charbindex)
    workbook.close()

    # make mytext.charc
    path = folder1 + textpos + text +'/py/mytext/charc.xlsx'
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    worksheet.write_column(0, 0, charc)
    worksheet.write_column(0, 1, charcindex)
    workbook.close()

    # make mytext.chard
    path = folder1 + textpos + text +'/py/mytext/chard.xlsx'
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    worksheet.write_column(0, 0, chard)
    worksheet.write_column(0, 1, chardindex)
    workbook.close() 


    return astr, bstr, cstr, dstr, chara, charb, charc, chard


def find_lineno(text):
    # find total pages
    pagespath = folder1 + textpos + text +'/py/pages/pages.txt'
    pages = open(pagespath, "r").read()
    pages = int(pages)


    # find lines per page
    linesperpage = []
    for pageno in range(1,pages+1):
        linespath = folder1 + textpos + text +'/py/lines/mytext.page(' + str(pageno) + ').lines.xlsx'
        wb = xlrd.open_workbook(linespath)
        sheet = wb.sheet_by_index(0)
        linesperpage.append(sheet.cell_value(1, 0))

    
    # find total lines
    lines = 0
    for li in linesperpage:
        lines += int(li)

    # make mytext.lineno
    linenotxt = folder1 + textpos + text + '/py/mytext/lineno.txt'
    linenofile = open(linenotxt, 'w')
    linenofile.write(str(lines))
    linenofile.close() 


    return pages, linesperpage, lines



def mainSplit(text, astr, bstr, cstr, dstr):

    s = split(text)
    allwordinfo = s[5]

    x = shortbyletternumber(text, allwordinfo, astr, bstr, cstr, dstr)

    f = find_lineno(text)
