
from datetime import datetime

#Sinarthsh opou kanei save ta crashes se ena arxeio analoga me timeanddate, ta arxeia afta einai ta legomena: "for_runcrashes_<timeanddate>.txt"
def saveCrashList(subject_no, text, crashlist, crashtxt):
    now = datetime.now()
    timeanddate = now.strftime("%d-%m-%Y  %H:%M:%S")

    fid = open(crashtxt, 'a')
    fid.write('%d  %s  %s  %s\n' %(subject_no, text, crashlist, timeanddate))
