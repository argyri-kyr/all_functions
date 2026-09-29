



from asyncio.windows_events import NULL
import xlsxwriter
import wave



from globalVars import folder1, folder2
from GetSomeInitialData import getGazesFolderbyText, getGazesFoldersandClass



def sort_and_format_time(time_list):
    # Convert hour, minute, and second values to integers
    hour = int(time_list[0])
    minute = int(time_list[1])
    second = int(time_list[2])

    # Calculate the total time in seconds
    total_time = hour * 3600 + minute * 60 + second

    # Return the time value in the desired format
    return [hour, minute, second]




def totalreadingtime(sub, allsubtexts):
    path = folder1 + folder2 + 'subject_' + str(sub) + '/' + 'total_working_time.xlsx'
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet() 


    ##############################################################################################################
    # Count .wav duration for each text
    wav_durations = {}
    for i in range(len(allsubtexts)):
        textname = allsubtexts[i].split("_")[3]
        audiopath = folder1 + folder2 + 'subject_' + str(sub) + '/' + allsubtexts[i] + '/AudioRecording.wav'
        with wave.open(audiopath) as mywav:
            total_length = mywav.getnframes() / mywav.getframerate()
            wav_durations[textname] = total_length
            worksheet.write(0, i, textname)
            worksheet.write(1, i, total_length)
    ##############################################################################################################
    
    
    # Ftiaxnw tis listes me tous xronous. Apo tin onomasia tou fakelou pairnw to timestamp tou kathe fakelou
    # pou einai kai o xronos dimiourgias tou fakelou ara kai o akribis xronos gia to pote arxise to peirama
    file_creations = []
    for i in range(len(allsubtexts)):
        x = allsubtexts[i].split("-")
        y = x[-1].split(".")
        z = [int(a) for a in y]
        if(z[0]==1):
            z[0]=13
        file_creations.append(z)
        
    # Sort the list of time values using the custom key function and format the returned values
    sorted_time_list = sorted(file_creations, key=sort_and_format_time)
    formatted_sorted_time_list = [sort_and_format_time(item) for item in sorted_time_list]
    
   ##############################################################################################################
   
   
    # Find first and last text that is done
    sorted_text_creations = {}
    for i in range(len(formatted_sorted_time_list)):
        for j in range(len(allsubtexts)):
            x = allsubtexts[j].split("-")
            y = x[-1].split(".")
            z = [int(a) for a in y]
            if(z[0]==1):
                z[0]=13
            textname = allsubtexts[j].split("_")[3]
            
            if( z == formatted_sorted_time_list[i] ):
                sorted_text_creations[textname] = formatted_sorted_time_list[i]
    
        
    # 
    lasttextdone = next(reversed(sorted_text_creations))
    firsttextdone = next(iter(sorted_text_creations.items()))[0]
    
    ##############################################################################################################
    
    
    # What i will do in the following code, in general:
    # I will go to the last file creation time and i will add the audio time,
    # in order to find the total time that this experiment takes to complete.
    # After this i will subtract the first file creation time from this time and i will have the total experiment time
    
    # find hours, minutes, seconds from the last audio
    duration = wav_durations[lasttextdone] 
    
    hours = int(duration/3600)
    duration -= hours*3600
    
    minutes = int(duration/60)
    duration -= minutes*60
    
    seconds = duration
    
    # add audio duration in file creation's time
    textend_hours = sorted_text_creations[lasttextdone][0] + hours
    textend_minutes = sorted_text_creations[lasttextdone][1] + minutes
    textend_seconds = sorted_text_creations[lasttextdone][2] + seconds
    
    # subtract start and end 
    total_hour = textend_hours - sorted_text_creations[firsttextdone][0]
    total_minutes = textend_minutes - sorted_text_creations[firsttextdone][1]
    total_seconds = textend_seconds - sorted_text_creations[firsttextdone][2]
    
    
    # # In general:  
    # convert all these to seconds and then again to hours, minutes and seconds
    # # Explanation:  
    # if i have a starttime like: 12:05:40 and an endtime like: 12:06:10 ,
    # then with the above calculation i will have: 
    # 0 hours, 1 minutes, -30 seconds
    # that is not true, actually it is kind of true because the only thing that it needs is to subtract from minutes the seconds 
    # so in the following calculation i will convert them all to secolnds and i will add them, so after that i will have:
    # 0 hours = 0 seconds
    # 1 minutes = 60 seconds
    # -30 seconds = -20 seconds
    # final seconds = 0 + 60 - 20 = 40 seconds 
    # and in the end i will convert the final seconds into the actuall time, like:
    # 0 hours, 0 minutes, 40 seconds
    seconds_conversion = total_hour * 3600 + total_minutes * 60 + total_seconds
    allin_seconds = seconds_conversion
    
    final_hours = int(seconds_conversion/3600)
    seconds_conversion -= final_hours*3600
    
    final_minutes = int(seconds_conversion/60)
    seconds_conversion -= final_minutes*60
    
    final_seconds = seconds_conversion
    
    final_experiment_duration = [final_hours, final_minutes, final_seconds]
    
    # Print Results
    print("\nAudio durations in seconds:")
    print(wav_durations)
    
    # Total Seconds
    print("\nAll time in seconds: ", allin_seconds)
    
    # Total time takes the experiment in this sub
    print("\nHours: ", final_hours)
    print("Minutes: ", final_minutes)
    print("Seconds: ", final_seconds)

    worksheet.write(3, 0, "Hours")
    worksheet.write(3, 1, final_hours)
    worksheet.write(4, 0, "Minutes")
    worksheet.write(4, 1, final_minutes)
    worksheet.write(5, 0, "Seconds")
    worksheet.write(5, 1, final_seconds)
    workbook.close()
    
    return wav_durations, allin_seconds



def main():
    path = folder1 + folder2 + 'mean_working_duration.xlsx'
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet() 

    wav_list = []
    seconds_list = []
    
    
    subs = [13312, 13332]
    # subs = [i for i in range(13001, 13041)]
    texts = ['visit', 'zoo', 'visitloud','olympia', "morning"]

    for sub in subs:
        allsubtexts = []
        search1 = getGazesFoldersandClass(sub)   # Sunarthsh opoy psaxnei ean iparxei to subject mesa sto fakelo  /Radar_Iro_copy/individual/
        if( search1 == NULL ):
            print("\nSubject= ", sub, "doesn't exist")
            continue
        
        print("\nSubject = ", sub)
        for text in texts:
            from_runcrashes = False

            gazesfolders1, subclass, subexam = search1[0], search1[1], search1[2]   # gazesfolders1 : ta keimena pou brethikan mesa sto individual
            gazesfolders = gazesfolders1 
            gazesfolders = list(dict.fromkeys(gazesfolders))               

            file = getGazesFolderbyText(sub, subexam, text, gazesfolders, subclass, from_runcrashes)
            if(file==NULL):
                # print("There is no data for this text")
                continue
            
            allsubtexts.append(file)
            
        wav_durations, allin_seconds = totalreadingtime(sub, allsubtexts)
        
        wav_list.append(wav_durations)
        seconds_list.append(allin_seconds)
    
    
    # calculations for extract mean duration of the whole experiment
    seconds_summ = 0
    for i in range(len(seconds_list)):
        seconds_summ += seconds_list[i]
    
    mean_sec_exper_dur = seconds_summ/len(seconds_list)
    
    mean_hours = int(mean_sec_exper_dur/3600)
    mean_sec_exper_dur -= mean_hours*3600
    
    mean_minutes = int(mean_sec_exper_dur/60)
    mean_sec_exper_dur -= mean_minutes*60
    
    mean_seconds = mean_sec_exper_dur
    
    
    worksheet.write(0, 0, "Mean Experiment Duration")
    
    worksheet.write(2, 0, "Hours")
    worksheet.write(2, 1, mean_hours)

    worksheet.write(3, 0, "Minutes")
    worksheet.write(3, 1, mean_minutes)

    worksheet.write(4, 0, "Seconds")
    worksheet.write(4, 1, mean_seconds)
    
    final_column = 2
    
    
    # calculations for extract mean duration for each of these texts
    for i in range(len(texts)):
        seconds_summ = 0
        textno = 0
        for j in range(len(wav_list)):
            if(texts[i] in wav_list[j]):
                seconds_summ += wav_list[j][texts[i]]
                textno += 1
        
        if( textno == 0 ):
            continue
        
        mean_per_text = seconds_summ/textno
        
        worksheet.write(0, final_column+1, texts[i] + " (/s)")
        worksheet.write(2, final_column+1, mean_per_text)
        
        final_column += 2
    
    
    workbook.close()
 
            
            
main()