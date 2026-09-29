


from asyncio.windows_events import NULL
import os
import time
import statistics
import math
import numpy
import xlsxwriter
import matplotlib.pyplot as plt
from datetime import datetime

# from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)


from globalVars import folder1, folder2, pyimagepath
from loaduncutdata_horizontal_eyeposition import loaduncutdata_horizontal_eyeposition
from eyeposition_changeLine_clear import eyeposition_changeLine_clear
from eyeposition_finalindex_clear import eyeposition_finalindex_clear
from eyeposition_trackLoss_clear import eyeposition_trackLoss_sideclear, eyeposition_trackLoss_bothclear
from disparitywindow import disparitywindow
from load_subs_initial_data import load_subs_initial_data
from make_textfolder_struct import make_textfolder_struct


def eyeposition_Procedure(subs, texts, firstchoices, bypass, hardcases, onlylefteye, onlyrighteye):

    # Get Subject's Data from an Input Dialogue  

    global from_runcrashes, disparitywsh1, disparitywsh2, disparitywsh3, disparitywsh4, disparitycounter1, disparitycounter2, disparitycounter3, disparitycounter4
    
    from_runcrashes = False
    disparitycounter1 = -1
    disparitycounter2 = -1
    disparitycounter3 = -1
    disparitycounter4 = -1
    
    # Date timestamp
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y_%H-%M-%S")  # format date in the way i want,like: dd-mm-YY  H-M-S


    # Orizw se poia exam einai to kathe subject
    exam = 1
    
    
    # Create appropriate structure/folder for all statistical data to be stored
    statistical_results_folder = 'statistical_data/'
    disparitywb1 = xlsxwriter.Workbook(folder1 + folder2 + statistical_results_folder + 'horizontal_disparityInfo_' + str(timestamp) + '.xlsx')
    disparitywsh1 = disparitywb1.add_worksheet()
        
    disparitywb2 = xlsxwriter.Workbook(folder1 + folder2 + statistical_results_folder + 'vertical_disparityInfo_' + str(timestamp) + '.xlsx')
    disparitywsh2 = disparitywb2.add_worksheet()

    disparitywb3 = xlsxwriter.Workbook(folder1 + folder2 + statistical_results_folder + 'diagonal_disparityInfo_' + str(timestamp) + '.xlsx')
    disparitywsh3 = disparitywb3.add_worksheet()
    
    disparitywb4 = xlsxwriter.Workbook(folder1 + folder2 + statistical_results_folder + 'diagonal_statistical_analysis_' + str(timestamp) + '.xlsx')
    disparitywsh4 = disparitywb4.add_worksheet()
    

    # Kuria while loop gia na trexoun ola ta subject pou thelw ( trexw 1h loop gia ta subject kai 2h eswterikh loop gia ta texts tou subject )
    for i in range(len(subs)): 
        disparitycounter1 += 1
        disparitycounter2 += 1
        disparitycounter3 += 1
        disparitycounter4 += 1
        
    
        # load subjects data, i.e if subject exist and which texts has this subject
        gazesfolders, analysis_texts, textanalysisfiles = load_subs_initial_data(subs[i], exam, texts, from_runcrashes)      
        if( gazesfolders == NULL ):
            continue        
        
        
        for j in range (len(analysis_texts)):
            text = analysis_texts[j]
            file = textanalysisfiles[j]
            
            # Make the folders (if not exist) that i will use to store graphs and data for my texts
            make_textfolder_struct(subs[i], exam, text)
    

            Start_Text_Procedure(file, subs[i], exam, text, onlylefteye, onlyrighteye)  # Main procedure of the programme for each text
            # disparitycounter1 += 1
            # disparitycounter2 += 1
            # disparitycounter3 += 1
            # disparitycounter4 += 1
            
            
        
        if( analysis_texts==[] ):
            print("\nΝo texts were found for Subject = %d " % subs[i])
            time.sleep(3)
        
         
              
    #Delete unneeded .txts 
    for file in os.listdir():
        if( file.endswith(".txt") ):
            if( os.stat(file).st_size==0 ):
                os.remove(file)
    
    disparitywb1.close()
    disparitywb2.close()
    disparitywb3.close()
    disparitywb4.close()




#Procedure's args ={ (text : text i will analyze), (folder : main folder), (sub1 : subject's id), (sub1class : subject's class) }
def Start_Text_Procedure(file, sub1,  exam, text, onlylefteye, onlyrighteye):
    global disparitycounter1, disparitycounter2, disparitycounter3, disparitycounter4
    

    # Load Gazes Data 
    uncutgazesraw, uncutgazes, oneeyeindexes = loaduncutdata_horizontal_eyeposition(text, file, sub1, onlylefteye, onlyrighteye)


    index, leftx, lefty, leftvalid, rightx, righty, rightvalid, timestamp = uncutgazesraw[0], uncutgazesraw[1], uncutgazesraw[2], uncutgazesraw[3], uncutgazesraw[4], uncutgazesraw[5], uncutgazesraw[6], uncutgazesraw[7]
    
    
    #Temporary lists that will save the cutgazes data per page
    pageno = -1             #page number, assumption pageno=-1
    
    tempindex = []
    templeftx = []
    templefty = []
    templeftvalid = []
    
    temprightx = []
    temprighty = []
    temprightvalid = []
    
    temptimestamp = []
    
    # counter for gazes lines
    i=-1  


    while( i<len(index) ):
        i+=1
        if(  ( i<len(index) and index[i] == 1 )  or  ( i == len(index) )  ):
            pageno+=1

            if(pageno>0) :
                
                print("\nsubject %d, text %s, page %d " %(sub1, text, pageno))          #Βρισκω τα ROIbounds του κειμενου

            if( len(tempindex) != 0 ):                  #Οταν φτασω στο τελος της 1ης σελιδας και εχω συλλεξει τα δεδομενα μου      
                finalindexes = []                                                         
                if( uncutgazesraw!= [] ):
                    finalindexespath = folder1 + folder2 + '/subject_' + str(sub1) + '/' + file + '/py/finalindexes_page' + str(pageno) + '.txt'
                    f = open(finalindexespath, 'r')
                    for line in f.readlines():
                        fields = line.split('\n')
                        finalindexes.append(int(float(fields[0])))
                    
                    # FIRST: clear(None) vergence data from start finalindex till end finalindex
                    vergenceindex, vergenceleftx_clean1, vergencerightx_clean1, vergencelefty_clean1, vergencerighty_clean1, vergenceleftvalid, vergencerightvalid = eyeposition_finalindex_clear(tempindex, templeftx, temprightx, templefty, temprighty, templeftvalid, temprightvalid, finalindexes)
                    
                    
                    # SECOND: clear(None) vergence data line by line 
                    vergenceindex, vergenceleftx_clean2, vergencerightx_clean2, vergencelefty_clean2, vergencerighty_clean2, vergenceleftvalid, vergencerightvalid = eyeposition_changeLine_clear(sub1, file, pageno, vergenceindex, vergenceleftx_clean1, vergencerightx_clean1, vergencelefty_clean1, vergencerighty_clean1, vergenceleftvalid, vergencerightvalid, finalindexes)
                    
                    
                    # # # # # # # # # # # # # # # # # # # # VERGENCE ANALYSIS PROCESS # # # # # # # # # # # # # # # # # # #
                    
                
                    # clear(None) vergence data from track Loss
                    vergenceleftx_clean3, vergencerightx_clean3 = eyeposition_trackLoss_sideclear(vergenceindex, vergenceleftx_clean2, vergencerightx_clean2)
                    standar_deviation1, mean1, spikescounter1 = horizontal_eyeposition(sub1, exam, text, pageno, vergenceleftx_clean3, vergencerightx_clean3, finalindexes)
                    disparitywsh1.write_row(disparitycounter1, 0, [sub1, standar_deviation1, mean1, spikescounter1])
                    disparitycounter1 += 1
                    
                    
                    vergencelefty_clean3, vergencerighty_clean3 = eyeposition_trackLoss_sideclear(vergenceindex, vergencelefty_clean2, vergencerighty_clean2)
                    standar_deviation2, mean2, spikescounter2 = vertical_eyeposition(sub1, exam, text, pageno, vergencelefty_clean3, vergencerighty_clean3 ,finalindexes)
                    disparitywsh2.write_row(disparitycounter2, 0, [sub1, standar_deviation2, mean2, spikescounter2])
                    disparitycounter2 += 1
                    
                
                    
                    vergenceleftx_clean4, vergencerightx_clean4, vergencelefty_clean4, vergencerighty_clean4, only_track_loss = eyeposition_trackLoss_bothclear(vergenceindex, vergenceleftx_clean2, vergencerightx_clean2, vergencelefty_clean2, vergencerighty_clean2, vergenceleftvalid, vergencerightvalid)
                    standar_deviation3, mean3, spikescounter31, spikescounter32, spikescounter33, disparity = diagonal_eyeposition(sub1, exam, text, pageno, vergenceleftx_clean4, vergencerightx_clean4, vergencelefty_clean4, vergencerighty_clean4, finalindexes, only_track_loss)
                    disparitywsh3.write_row(disparitycounter3, 0, [sub1, standar_deviation3, mean3, spikescounter31, spikescounter32, spikescounter33])
                    disparitycounter3 += 1
                    
                    
                    pososto = diagonal_statistical_analysis(disparity, standar_deviation3, mean3)
                    disparitywsh4.write_row(disparitycounter4, 0, [sub1, text, pososto])
                    disparitycounter4 += 1
                    
                    
                    standar_deviations = standar_deviation_plot(sub1, exam, text, pageno, disparity)
                    
                    windowlen = 50
                    disparitywindowmean = disparitywindow(sub1, exam, text, pageno, windowlen, disparity)
                    
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    
                    
                    


            #Αδειαζω τις λιστες που περιεχουν τα δεδομενα της σελιδας που επεξεργαστηκα, ωστε να αποθηκευσω τα νεα δεδομενα της επομενης σελιδας
            
            tempindex = []
            templeftx = []
            templefty = []
            templeftvalid = []
            
            temprightx = []
            temprighty = []
            temprightvalid = []
            
            temptimestamp = []

            
            plt.close('all')
        

        #Εδω δημιουργω τις λιστες των δεδομενων ανα σελιδα   
        if( i != len(index) ):

            if( uncutgazesraw!=[] ):
                tempindex.append( index[i] )
                templeftx.append( leftx[i] )
                templefty.append( lefty[i] )
                templeftvalid.append( leftvalid[i] )
                temprightx.append( rightx[i] )  
                temprighty.append( righty[i] ) 
                temprightvalid.append( rightvalid[i] )  
                temptimestamp.append( timestamp[i] )        

    


def horizontal_eyeposition(sub1, exam, text, pageno, vergenceleftx_clean, vergencerightx_clean, finalindexes):
    # left plot
    f1, ax1 = plt.subplots()
    f1.set_figwidth(18)
    f1.set_figheight(4)
    ax1.plot(vergenceleftx_clean)
    # title and labels, setting initial sizes
    f1.suptitle(str(sub1) + '  ' + 'Horizontal left eye position', fontsize=11, fontweight ="bold")
    ax1.set_xlabel('Time', fontsize=11)
    ax1.set_ylabel('X position(pixels)', fontsize=11) 
    ax1.margins(x=0.005)
    ax1.grid()
    f1.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/extra_plots/horizontal_left_eyeposition' + str(pageno) + '.png', dpi=100)



    # right plot
    f2, ax2 = plt.subplots()
    f2.set_figwidth(18)
    f2.set_figheight(4)
    ax2.plot(vergencerightx_clean)
    # title and labels, setting initial sizes
    f2.suptitle(str(sub1) + '  ' + 'Horizontal right eye position', fontsize=11, fontweight ="bold")
    ax2.set_xlabel('Time', fontsize=11)
    ax2.set_ylabel('X position(pixels)', fontsize=11)
    ax2.margins(x=0.005)
    ax2.grid() 
    f2.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/extra_plots/horizontal_right_eyeposition' + str(pageno) + '.png', dpi=100)
    


    # both plot
    f3, ax3 = plt.subplots()
    f3.set_figwidth(18)
    f3.set_figheight(4)
    ax3.plot(vergenceleftx_clean, 'r')
    ax3.plot(vergencerightx_clean)
    # title and labels, setting initial sizes
    f3.suptitle(str(sub1) + '  ' + 'Horizontal eye position', fontsize=11, fontweight ="bold")
    ax3.set_xlabel('Time', fontsize=11)
    ax3.set_ylabel('X position(pixels)', fontsize=11)
    ax3.margins(x=0.005) 
    ax3.grid()
    f3.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/extra_plots/horizontal_eyeposition' + str(pageno) + '.png', dpi=100)



    # disparity plot
    f4, ax4 = plt.subplots()
    f4.set_figwidth(18)
    f4.set_figheight(4)
    
    
    # calculate disprity
    disparity = []
    for i in range(len(vergenceleftx_clean)):
        if( vergenceleftx_clean[i]!=None and vergencerightx_clean[i]!=None ):
            disparity.append( vergenceleftx_clean[i] - vergencerightx_clean[i] )
        else:
            disparity.append( None )
    
    clear_disparity = [x for x in disparity if x!=None]
    
    # calculate max value
    absdisparity = [abs(clear_disparity[i]) for i in range(len(clear_disparity))]
    max_X = max(absdisparity)
    
    # disparity Info (stdev, mean)
    standar_deviation = numpy.std(clear_disparity)
    mean = statistics.mean(clear_disparity)

    disparityinfopath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + '/py/extra_plots/disparityInfo' + str(pageno) + '.txt' 
    disparityinfofile = open(disparityinfopath, 'w')
    disparityinfofile.write(str(standar_deviation))
    disparityinfofile.write("\n")
    disparityinfofile.write(str(mean))

    # spikes Info
    spikescounter = 0
    spikex1 = []
    spikex2 = []
    spikespath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + '/py/extra_plots/spikesdisparity' + str(pageno) + '.txt' 
    spikesfile = open(spikespath, 'w')
    for i in range(len(disparity)):
        if( disparity[i]!=None ):
            if(  disparity[i]<mean-3*standar_deviation or disparity[i]>mean+3*standar_deviation ):
                spikescounter+=1
                spikesfile.write(str(vergenceleftx_clean[i]) + "\n")
                spikesfile.write(str(vergencerightx_clean[i]) + "\n")
                spikesfile.write(str(disparity[i]) + "\n\n")
                spikex1.append(disparity[i])
                spikex2.append(i)
            else:
                continue
            
    
    # plot disparity (disparity-mean)
    # disparity = [disparity[x]-mean for x in range(len(disparity))]
    ax4.plot(disparity)
    ax4.plot(spikex2, spikex1, 'ro', markersize=3)
    ax4.vlines(finalindexes, mean-10*standar_deviation, mean+10*standar_deviation, linestyles='dashed', colors='red')
    ax4.hlines([mean-3*standar_deviation,mean+3*standar_deviation], xmin=0, xmax=len(disparity), linewidth=1, color='orange')
    
    # title and labels, setting initial sizes, limits
    f4.suptitle(str(sub1) + '  ' + 'Horizontal disparity panel', fontsize=11, fontweight ="bold")
    ax4.set_xlabel('Time', fontsize=11)
    ax4.set_ylabel('Phoria', fontsize=11)
    ax4.margins(x=0.005) 
    
    ax4.set_xlim([0, 1500])
    ax4.set_ylim([-500, 500])
    
    ax4.grid()
    f4.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/extra_plots/horizontal_disparity_panel' + str(pageno) + '.png', dpi=100)

    return standar_deviation, mean, spikescounter



def vertical_eyeposition(sub1, exam, text, pageno, vergencelefty_clean, vergencerighty_clean, finalindexes):
    # left plot
    f1, ax1 = plt.subplots()
    f1.set_figwidth(18)
    f1.set_figheight(4)
    ax1.plot(vergencelefty_clean)
    # title and labels, setting initial sizes
    f1.suptitle(str(sub1) + '  ' + 'Vertical left eye position', fontsize=11, fontweight ="bold")
    ax1.set_xlabel('Time', fontsize=11)
    ax1.set_ylabel('X position(pixels)', fontsize=11) 
    ax1.margins(x=0.005)
    ax1.grid()
    f1.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/extra_plots/vertical_left_eyeposition' + str(pageno) + '.png', dpi=100)



    # right plot
    f2, ax2 = plt.subplots()
    f2.set_figwidth(18)
    f2.set_figheight(4)
    ax2.plot(vergencerighty_clean)
    # title and labels, setting initial sizes
    f2.suptitle(str(sub1) + '  ' + 'Vertical right eye position', fontsize=11, fontweight ="bold")
    ax2.set_xlabel('Time', fontsize=11)
    ax2.set_ylabel('X position(pixels)', fontsize=11)
    ax2.margins(x=0.005)
    ax2.grid() 
    f2.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/extra_plots/vertical_right_eyeposition' + str(pageno) + '.png', dpi=100)
    


    # both plot
    f3, ax3 = plt.subplots()
    f3.set_figwidth(18)
    f3.set_figheight(4)
    ax3.plot(vergencelefty_clean, 'r')
    ax3.plot(vergencerighty_clean)
    # title and labels, setting initial sizes
    f3.suptitle(str(sub1) + '  ' + 'Vertical eye position', fontsize=11, fontweight ="bold")
    ax3.set_xlabel('Time', fontsize=11)
    ax3.set_ylabel('X position(pixels)', fontsize=11)
    ax3.margins(x=0.005) 
    ax3.grid()
    f3.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/extra_plots/vertical_eyeposition' + str(pageno) + '.png', dpi=100)



    # disparity plot
    f4, ax4 = plt.subplots()
    f4.set_figwidth(18)
    f4.set_figheight(4)
    
    
    # calculate disprity
    disparity = []
    for i in range(len(vergencelefty_clean)):
        if(vergencelefty_clean[i]!=None and vergencerighty_clean[i]!=None ):
            disparity.append( vergencelefty_clean[i] - vergencerighty_clean[i] )
        else:
            disparity.append(None)
    
    clear_disparity = [x for x in disparity if x!=None]

    # calculate max value
    absdisparity = [abs(clear_disparity[i]) for i in range(len(clear_disparity))]
    max_X = max(absdisparity)
    
    # disparity Info (stdev, mean)
    standar_deviation = numpy.std(clear_disparity)
    mean = statistics.mean(clear_disparity)

    disparityinfopath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + '/py/extra_plots/disparityInfo_vertical' + str(pageno) + '.txt' 
    disparityinfofile = open(disparityinfopath, 'w')
    disparityinfofile.write(str(standar_deviation))
    disparityinfofile.write("\n")
    disparityinfofile.write(str(mean))

    # spikes Info
    spikescounter = 0
    spikex1 = []
    spikex2 = []
    spikespath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + '/py/extra_plots/spikesdisparity_vertical' + str(pageno) + '.txt' 
    spikesfile = open(spikespath, 'w')
    for i in range(len(disparity)):
        if( disparity[i]!=None ):
            if( disparity[i]<mean-3*standar_deviation or disparity[i]>mean+3*standar_deviation ):
                spikescounter+=1
                spikesfile.write(str(vergencelefty_clean[i]) + "\n")
                spikesfile.write(str(vergencerighty_clean[i]) + "\n")
                spikesfile.write(str(disparity[i]) + "\n\n")
                spikex1.append(disparity[i])
                spikex2.append(i)
        else:
            continue
            
    
    # plot disparity (disparity-mean)
    # disparity = [disparity[x]-mean for x in range(len(disparity))]
    ax4.plot(disparity)
    ax4.plot(spikex2, spikex1, 'ro', markersize=3)
    ax4.vlines(finalindexes, mean-10*standar_deviation, mean+10*standar_deviation, linestyles='dashed', colors='red')
    ax4.hlines([mean-3*standar_deviation,mean+3*standar_deviation], xmin=0, xmax=len(disparity), linewidth=1, color='orange')
    
    # title and labels, setting initial sizes, limits
    f4.suptitle(str(sub1) + '  ' + 'Vertical disparity panel', fontsize=11, fontweight ="bold")
    ax4.set_xlabel('Time', fontsize=11)
    ax4.set_ylabel('Phoria', fontsize=11)
    ax4.margins(x=0.005) 
    
    ax4.set_xlim([0, 1500])
    ax4.set_ylim([-500, 500])
    
    ax4.grid()
    f4.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/extra_plots/vertical_disparity_panel_' + str(pageno) + '.png', dpi=100)

    return standar_deviation, mean, spikescounter




def diagonal_eyeposition(sub1, exam, text, pageno, vergenceleftx_clean, vergencerightx_clean, vergencelefty_clean, vergencerighty_clean, finalindexes, only_track_loss):
    # disparity plot
    f4, ax4 = plt.subplots()
    f4.set_figwidth(18)
    f4.set_figheight(4)
            
    
    # calculate disparity
    disparity = []
    for i in range(len(vergenceleftx_clean)):
        if( vergenceleftx_clean[i]!=None and vergencerightx_clean[i]!=None and vergencelefty_clean[i]!=None and vergencerighty_clean[i]!=None ):
            distance = math.sqrt( (vergencerightx_clean[i]-vergenceleftx_clean[i])**2 + (vergencerighty_clean[i]-vergencelefty_clean[i])**2 )
            disparity.append( distance )
        else:
            disparity.append(None)
    
    clear_disparity = [ x for x in disparity if x!=None ]
    
    # calculate max value
    absdisparity = [abs(clear_disparity[i]) for i in range(len(clear_disparity))]
    max_X = max(absdisparity)
    
    
    # disparity Info (stdev, mean)
    standar_deviation = numpy.std(clear_disparity)
    mean = statistics.mean(clear_disparity)

    disparityinfopath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + '/py/extra_plots/disparityInfo_diagonal' + str(pageno) + '.txt' 
    disparityinfofile = open(disparityinfopath, 'w')
    disparityinfofile.write(str(standar_deviation))
    disparityinfofile.write("\n")
    disparityinfofile.write(str(mean))

    # spikes Info
    spikescounter1 = 0
    spikescounter2 = 0
    spikescounter3 = 0
    spikex1 = []
    spikex2 = []
    spikespath = folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + '/py/extra_plots/spikesdisparity_diagonal' + str(pageno) + '.txt' 
    spikesfile = open(spikespath, 'w')
    for i in range(len(disparity)):
        if( disparity[i]!=None ):
            if( disparity[i]<mean-3*standar_deviation or disparity[i]>mean+3*standar_deviation ):
                spikescounter1+=1
                spikesfile.write(str(vergencelefty_clean[i]) + "\n")
                spikesfile.write(str(vergencerighty_clean[i]) + "\n")
                spikesfile.write(str(disparity[i]) + "\n\n")
                spikex1.append(disparity[i])
                spikex2.append(i)
            
            if( abs(disparity[i])> abs(mean)+4*standar_deviation ):
                spikescounter2+=1

            if( abs(disparity[i])> abs(mean)+5*standar_deviation ):
                spikescounter3+=1
        else:
            continue


    # find & plot with purple dots where i have track loss
    trackloss_points_x = []
    trackloss_points_y = []
    for j in range(len(only_track_loss)):
        trackloss_points_x.append(only_track_loss[j])
        trackloss_points_y.append(mean)
        
    
    # plot disparity (disparity-mean)
    # disparity = [disparity[x]-mean for x in range(len(disparity))]
    
    ax4.plot(disparity)
    ax4.plot(spikex2, spikex1, 'ro', markersize=2)
    ax4.plot(trackloss_points_x, trackloss_points_y, 'mo', markersize=3)
    ax4.vlines(finalindexes, mean-10*standar_deviation, mean+10*standar_deviation, linestyles='dashed', colors='red')
    ax4.hlines([mean-3*standar_deviation,mean+3*standar_deviation], xmin=0, xmax=len(disparity), linewidth=1, color='orange')

    # title and labels, setting initial sizes, limits
    f4.suptitle(str(sub1) + '  ' + 'Diagonal disparity panel', fontsize=11, fontweight ="bold")
    ax4.set_xlabel('Time', fontsize=11)
    ax4.set_ylabel('Phoria', fontsize=11)
    ax4.margins(x=0.005) 
    
    # ax4.set_xlim([0, 1500])
    # ax4.set_ylim([-500, 500])
    
    ax4.grid()
    f4.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/extra_plots/diagonal_disparity_panel' + str(pageno) + '.png', dpi=100)


    # histogramm plot
    f5, ax5 = plt.subplots()
    f5.set_figwidth(18)
    f5.set_figheight(4)
         
    ax5.hist(clear_disparity, bins=150)
    f5.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/extra_plots/histogram_disparity_panel' + str(pageno) + '.png', dpi=100)
    
    return standar_deviation, mean, spikescounter1, spikescounter2, spikescounter3, disparity
    


def diagonal_statistical_analysis(disparity, standar_deviation, mean):
    count1 = 0
    for i in range(len(disparity)):
        if( disparity[i]!=None ):
            # if( disparity[i] <= mean - 3*standar_deviation or disparity[i] >= mean + 3*standar_deviation ):
            # if( disparity[i] >= mean + 4*standar_deviation ):
            if( mean + 2*standar_deviation <= disparity[i] <= mean + 4*standar_deviation ):
                count1 += 1
        else:
            continue
    
    pososto = (count1/len(disparity))*100
    
    return pososto



def standar_deviation_plot(sub1, exam, text, pageno, disparity):
    # my first space is [0,20)
    start = 0
    stop = 20
    standar_deviations = []
    while ( stop <= len(disparity) ):
        tempdisparity = [ x for x in disparity[start:stop] if x!=None ]
        stdev = numpy.std( tempdisparity ) 
        standar_deviations.append( stdev )
        start += 1
        stop += 1
    

    # disparity plot
    f1, ax1 = plt.subplots()
    f1.set_figwidth(18)
    f1.set_figheight(4)
    
    ax1.plot(disparity)
    
    # title and labels, setting initial sizes, limits
    f1.suptitle(str(sub1) + '  ' + 'Standar Deviations Panel', fontsize=11, fontweight ="bold")
    ax1.set_xlabel('Time', fontsize=11)
    ax1.set_ylabel('Phoria', fontsize=11)
    ax1.margins(x=0.005) 
    
    ax1.set_xlim([0, 1500])
    ax1.set_ylim([-500, 500])
    
    ax1.grid()
    f1.savefig(folder1 + folder2 + 'subject_' + str(sub1) + '/all_graphs/' + text + str(exam) + pyimagepath + '/extra_plots/standar_deviations_panel' + str(pageno) + '.png', dpi=100)
    
    return standar_deviations



