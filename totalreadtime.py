


from asyncio.windows_events import NULL
import time
import xlsxwriter
import os



from globalVars import folder1, folder2
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass



def totalreadtime(sub, file):

    # time START
    pathstart = folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/validation.png'
    ti_m_s = os.path.getmtime(pathstart)
    m_ti_s = time.ctime(ti_m_s)
    t_obj_s = time.strptime(m_ti_s)
    T_stamp_s = time.strftime("%Y-%m-%d %H:%M:%S", t_obj_s)

    year = t_obj_s[0]
    month = t_obj_s[1]
    day = t_obj_s[2]

    hour_s = t_obj_s[3]
    minutes_s = t_obj_s[4]
    seconds_s = t_obj_s[5]

    # time END
    pathend = folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/validationEnd.png'
    ti_m_e = os.path.getmtime(pathend)
    m_ti_e = time.ctime(ti_m_e)
    t_obj_e = time.strptime(m_ti_e)

    year = t_obj_e[0]
    month = t_obj_e[1]
    day = t_obj_e[2]

    hour_e = t_obj_e[3]
    minutes_e = t_obj_e[4]
    seconds_e = t_obj_e[5]

    T_stamp_e = time.strftime("%Y-%m-%d %H:%M:%S", t_obj_e)

    total_hours = hour_e - hour_s
    hours_in_minutes = total_hours*60

    total_minutes = minutes_e - minutes_s
    total_minutes += hours_in_minutes

    # total_seconds = seconds_e - seconds_s

    return total_minutes
    




def main():
    path = folder1 + folder2 + 'RADAR_totalreadtime.xlsx'
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet() 

    worksheet.write(0, 0, "ID")
    worksheet.write(0, 1, "VISIT")
    worksheet.write(0, 2, "ZOO")
    worksheet.write(0, 3, "ZEBRA")
    worksheet.write(0, 4, "VISITLOUD")
    worksheet.write(0, 5, "TOTAL")
    count = 1


    subs = [x for x in range(11512, 11554)]
    texts = ['visit', 'zoo', 'efeyreseis', 'visitloud']

    for sub in subs:
        search1 = getGazesFoldersandClass(sub)   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/
        if( search1 == NULL ):
            print("Subject= ", sub, "doesn't exist")
            continue
        
        print("Sub = ", sub)
        timelist = []
        for text in texts:
            from_runcrashes = False

            gazesfolders1, subclass, subexam = search1[0], search1[1], search1[2]   # gazesfolders1 : ta keimena pou brethikan mesa sto individual
            gazesfolders = gazesfolders1 
            gazesfolders = list(dict.fromkeys(gazesfolders))               

            file = getGazesFolderbyText(sub, subexam, text, gazesfolders, subclass, from_runcrashes)
            if(file==NULL):
                # print("There is no data for this text")
                timelist.append(0)
                continue

            time = totalreadtime(sub, file)
            timelist.append(time)
            # print("Total time for text = ", text, "is time = ", time)
            f = open(folder1 + folder2 + 'subject_' + str(sub) + '/' + file + '/totalreadtime.txt', "w")
            f.write(str(time))
            f.close()

        timelist.append( sum(timelist) )
        worksheet.write(count, 0, sub)
        worksheet.write_row(count, 1, timelist)   
        count += 1

    workbook.close()


main()



