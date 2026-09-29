
from globalVars import folder1, folder2, textends
import os
from asyncio.windows_events import NULL
from os.path import exists
import shutil


# subs = [sno for sno in range(13780, 13901)]
subs = [13802]
exam = 1
text = 'phonolrhymes2v'


def main():
    filename1 = 'cutgazes'
    filename2 =  'fixations'
    for sno in subs:
        if os.path.exists(folder1 + folder2 + 'subject_' + str(sno) + '/all_data/' + text + str(exam)):
            pagesfile = open(folder1 + "texts/" + text + textends + "/py/pages/pages.txt", "r")
            pages = pagesfile.read()

            #Create cutgazes.txt file
            cutgazestxt = folder1 + folder2 + 'subject_' + str(sno) + '/all_data/' + text + str(exam) + '/' + filename1 + '.txt'
            cutgazesfile = open(cutgazestxt,"w")
            cutgazesfile.close()

            #Create fixations.txt file
            fixationstxt = folder1 + folder2 + 'subject_' + str(sno) + '/all_data/' + text + str(exam) + '/' + filename2 + '.txt' #Αυτο το αρχειο ειναι το αντιστοιχο του fixationsFF που δημιουργει το matlab με προσθετη στηλη στο τελος τη στηλη του timestampend
            fixationsfile = open(fixationstxt,'w')
            fixationsfile.close()
            
            # Create a copy of 1st page in order to process correct in the following procedure
            pageno = 1
            # cutgazes
            cutgazespagetxt = folder1 + folder2 + 'subject_' + str(sno) + '/all_data/' + text + str(exam) + '/' + filename1 + str(pageno) + '.txt'
            cutgazespagetxt_final = folder1 + folder2 + 'subject_' + str(sno) + '/all_data/' + text + str(exam) + '/' + filename1 + 'py' + str(pageno) + '.txt'
            shutil.copyfile(cutgazespagetxt_final, cutgazespagetxt)
            # fixations
            fixationspagetxt = folder1 + folder2 + 'subject_' + str(sno) + '/all_data/' + text + str(exam) + '/' + filename2 + str(pageno) + '.txt'
            fixationspagetxt_final = folder1 + folder2 + 'subject_' + str(sno) + '/all_data/' + text + str(exam) + '/' + filename2 + 'py' + str(pageno) + '.txt'
            shutil.copyfile(fixationspagetxt_final, fixationspagetxt)

            for pageno in range(1, int(pages)+1):
                cutgazespagetxt = folder1 + folder2 + 'subject_' + str(sno) + '/all_data/' + text + str(exam) + '/' + filename1 + str(pageno) + '.txt'
                fixationspagetxt = folder1 + folder2 + 'subject_' + str(sno) + '/all_data/' + text + str(exam) + '/' + filename2 + str(pageno) + '.txt'

                if( not exists( cutgazespagetxt ) ):
                    print("File  C:%s not found" % (cutgazespagetxt))
                    break
                if( not exists( fixationspagetxt ) ):
                    print("File  C:%s not found" % (fixationspagetxt))
                    break        

                # # append page number into cutgazes.txt
                cutgazeslist = [l for l in open(cutgazespagetxt).readlines()]
                for cl in range(len(cutgazeslist)):
                    cgrow = cutgazeslist[cl].split('\t')
                    cgrow.insert(5, str(pageno))
                    cgrow = "\t".join(cgrow)
                    cutgazeslist[cl] = cgrow
                # # end of append page number

                open(cutgazestxt, 'a').writelines(cutgazeslist)

                open(fixationstxt, 'a').writelines([l for l in open(fixationspagetxt).readlines()])
                
            
                cutgazespagetxt_final = folder1 + folder2 + 'subject_' + str(sno) + '/all_data/' + text + str(exam) + '/' + filename1 + 'py' + str(pageno) + '.txt'
                shutil.copyfile(cutgazespagetxt, cutgazespagetxt_final)
                
                fixationspagetxt_final = folder1 + folder2 + 'subject_' + str(sno) + '/all_data/' + text + str(exam) + '/' + filename2 + 'py' + str(pageno) + '.txt'
                shutil.copyfile(fixationspagetxt, fixationspagetxt_final)

                os.remove(cutgazespagetxt)
                os.remove(fixationspagetxt)
            
                if( pageno == int(pages) ):
                    print("\nProcess done for subject = ", sno)


main()

        