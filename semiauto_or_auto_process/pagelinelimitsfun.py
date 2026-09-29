
from asyncio.windows_events import NULL
import copy
from math import floor
import math
from statistics import mean
import numpy as np
import statistics
from scipy.ndimage import median_filter

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from semiauto_or_auto_process.findlastline import findlastline


def pagelinelimitsfun(x, y, pagelines, subject_no, exam, text, pageno, cutsUItxt, errorcrashtxt, runcrashestxt, crashlist, secondRun, firstruncuts):
    global pagestart, startwindow
    pagestart = NULL
    
    numberofcuts = 0

    #set parameters
    # startwindow = 300;  #median window
    winfirstgaze = 3      #window for finding first gaze
    meanmeddiff = 20      #mean-median difference for first gaze
    # gazesteps = 30      #number of gazes to detect line changes
    ylinestep = 60        #y-axis line step
    xlinestep = -500      #x-axis line step
    filterwindow = 40     #half median filter window
    xfilterwindow = 15
    linethreshold = 100
    # lastlinewindow = 200     #window for y-coord of last line
    # linechangelimit = 300    #limit for line change within line read
    epsilon = 50               #window for y coordinate for line revisit
    lastlineendtrap = epsilon
    # gazejump = 35           #forward gaze step after y jump
    # endwindow = 200         #window for backread lastline median
    lastlinegazejump = 20     #forward gaze step after jump to last line
    # bottomywindow = 500     #window for finding the bottomy
    firtlineminimumheight = 20
    newfilterwindow = 0
    
    
    xgazes = copy.deepcopy(x)
    ygazes = copy.deepcopy(y)
    
    # Trim Gazes
    if( np.nonzero(ygazes)[0].tolist() == [] ):
        lastNonZeroyIndex = float('inf')
        lastNonZeroxIndex = float('inf')
        indexdiff = float('inf')
    else:
        lastNonZeroyIndex = np.max(np.nonzero(ygazes))
        lastNonZeroxIndex = np.max(np.nonzero(xgazes))
        indexdiff = lastNonZeroyIndex - lastNonZeroxIndex
        
    # When the difference is less than 20, it is safe to cut
    if(indexdiff < 20):
        ygazes = ygazes[:lastNonZeroyIndex+1]
        xgazes = xgazes[:lastNonZeroyIndex+1]


    #finds y axis line limits for a page

    linegazesno = floor(len(ygazes)/pagelines)
    gazesteps = floor(linegazesno/15)
    gazejump = 2*gazesteps
    startwindow = floor(linegazesno/2)
    endwindow = floor(linegazesno/4)
    lastlinewindow = floor(linegazesno/4)
    linechangelimit = floor(linegazesno/4)
    bottomywindow = floor(linegazesno)
    fisrtlinechangelimit = linechangelimit*2
    trapmaxylinemeddiff = 250
    trapminylinemeddiff = 50
    windowxdropbefore = 4*gazesteps
    windwosxdropafter = 2*gazesteps
    pagejumpthreshold = 20
    longerspikes = False

    # if ( text=='armyjet' or text=='midfred' or text=='midfredloud' or text=='sunny' ):
    #     trapminylinemeddiff = 50
    #     trapmaxylinemeddiff = 250
    #     fisrtlinechangelimit = linechangelimit*2
    
    #Second run update values for variables
    if (secondRun == True):
        #startwindow = floor(linegazesno/2)
        #endwindow = floor(linegazesno/2)
        #lastlinewindow = floor(linegazesno/2)
        linechangelimit = floor(linegazesno/3)
        firtlineminimumheight = 10
        
        if( firstruncuts > pagelines+1 ):
            longerspikes = True
            
        gazesteps = floor(linegazesno/20)
        # gazejump = 2*gazesteps

        windowxdropbefore = 3*gazesteps
        windwosxdropafter = 4*gazesteps

        fisrtlinechangelimit = linechangelimit
        trapminylinemeddiff = 50
        trapmaxylinemeddiff = 250
        
        #first line starts too far ahead
        xfilterwindow = 20
        
        # winfirstgaze = 2*linegazesno
        if( linegazesno < 200 ):
            winfirstgaze = linegazesno
    
   
    # # # #  filter X, Y gazes # # # #
    # filter gazes with a median filter for Y
    ygazes = [0 if i < 0 else i for i in ygazes]
    ygazesfil = copy.deepcopy(ygazes)

    for i in range (filterwindow, len(ygazes)-filterwindow):
        start = int(i-filterwindow)
        end = int(i+filterwindow)+1
        ygazesfil[i] = Median( ygazes, start, end )


    # filter gazes with a median filter for X
    xgazes = [0 if i < 0 else i for i in xgazes]
    xgazesfil = copy.deepcopy(xgazes)

    for i in range (xfilterwindow, len(xgazes)-xfilterwindow):
        start = int(i-xfilterwindow)
        end = int(i+xfilterwindow)+1
        xgazesfil[i] = Median( xgazes, start, end )    

    xgazes = copy.deepcopy(xgazesfil)


    #set(gcf,'Visible','off')
    """
    indexes = [i for i in range(1,len(x)+1)]
    plt.plot(indexes,ygazesfil,'r')
    plt.title(['Line steps in page ', str(pageno), ', ', str(secondRun)])
    """


    #take a moving window bigger that ygazesfil and take the minimum median of it as bottomy
    #bottomy = min(median(ygazesfil(1:bottomywindow)));    
    bottomy = Median( ygazesfil, 9, bottomywindow ) 

    #find first gaze
    if(bottomy < epsilon):
        bottomy = epsilon
    

    for i in range(len(ygazesfil)):
        if(ygazesfil[i]-bottomy<epsilon):
            pagestart = i
            break
    
    
    # find the y median from startwindow gazes for determination of first line
    if(pagestart < startwindow):
        diff = np.diff( xgazes[pagestart : startwindow] )
        diff = diff.tolist()
        min_diff = min(diff)
    else:
        min_diff = math.inf
    
    
    if ( min_diff < xlinestep ):
        y1med = Median( ygazes, pagestart, startwindow )
    else:
        y1med = Median( ygazes, pagestart, floor(startwindow/2) )


    #find the first line start
    for i in range(0, len(ygazes)-winfirstgaze):
        ywindow = ygazes[i+1 : i+winfirstgaze+1]
        ywindow = [int(x) for x in ywindow]
        meanywindow = mean(ywindow)
        if ( abs(meanywindow-y1med) < meanmeddiff ):
            pagestart = i
            break

    #find the line jumps
    pagelinelimits = []
    #flag = zeros(1,10)
    myflag = 0
    count = 0

    if(pagestart==NULL):
        pagestart = 1

    pagelinelimits.append( pagestart )
    
    #ylinemedian(1) = y1med
    i = pagestart + 4*gazesteps
    A = []
    ylinemedianaux = y1med
    errorlinechangelimit = -1
    errorepsilon = -1
    errorgazejump = -1
    newpagestart = 0 

    while( i < len(ygazesfil)-max(2*gazesteps,gazejump) ):
        xendArray = i+windwosxdropafter
        if(xendArray>=len(xgazes)):
            xendArray = len(xgazes)-1

        startindex = min(i-min(windowxdropbefore,i-pagelinelimits[count]) , xendArray)
        endindex = max(i-min(windowxdropbefore,i-pagelinelimits[count]) , xendArray)
        listxg = xgazes[startindex : endindex+1]
        
        maxx = max(listxg)
        indexmax = listxg.index(max(listxg))
        minx = min(listxg)
        indexmin = listxg.index(min(listxg))
        
        
        newindexmax = 0
        newindexmin = 0
        endwindowignore = linegazesno

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  Specific Cases  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        if( text=="testapartav2part1" or text=="testapartav2part2" or text=="decodepseudowords2v" or text=="decoderealwords2v" or (text=="armyjet" and pageno==1 and count==3) or (text=="jockey" and pageno==1 and (count==2 or count==4)) or (text=="enemypie" and pageno==3 and count==3) ):
            xlinestep = 250
        
        if( secondRun==True and newfilterwindow==0 ):
            if( (text=='zebra' and pageno==2 and count>=3) or (text=='midfred' and pageno==2 and count>=3) or (text=='sunny' and pageno==3 and count>=4) ):
                newfilterwindow = int(filterwindow/2)
                for k in range (newfilterwindow, len(ygazes)-newfilterwindow):
                    start = int(k-newfilterwindow)
                    end = int(k+newfilterwindow)
                    ygazesfil[k] = Median( ygazes, start, end )
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        if ( ( ((ygazesfil[i+2*gazesteps]-ygazesfil[i]>ylinestep) and (minx-maxx<xlinestep)) and (indexmin<=indexmax) )    and  ( i+endwindowignore<len(xgazes) )  ):
            localxfilterwindow = xfilterwindow + 10
            # increase xfilterwindow and get xgazes filtered
            for f in range(localxfilterwindow, len(xgazes)-localxfilterwindow):
                xgazesfil[f] = Median(xgazes, f-localxfilterwindow, f+localxfilterwindow+1)
            #xgazesfil = median_filter(xgazes,size=2*xfilterwindow+1)
             
            startindex = min(i-min(windowxdropbefore,i-pagelinelimits[count]) , xendArray)
            endindex = max(i-min(windowxdropbefore,i-pagelinelimits[count]) , xendArray)
            subset = xgazesfil[startindex : endindex+1]
            # newmaxx = max(subset)
            newindexmax = subset.index(max(subset))     # other way to calculate the index of max or min element in a list
            # newminx = min(subset)
            newindexmin = subset.index(min(subset))     # other way to calculate the index of max or min element in a list

        if (  ((ygazesfil[i+2*gazesteps]-ygazesfil[i]>ylinestep) and (minx-maxx<xlinestep))  and  ((indexmin>indexmax) or (newindexmin>newindexmax))  ):    #||((myflag==1)&&(minx-maxx<xlinestep/2)))%(xgazes(i+2*gazesteps)-xgazes(i)<xlinestep)
            #if 2nd point is too close to y first point maybe this is the
            #correct start so move 2nd point to first?
            if ( (count == 0) and ((i+2*gazesteps) - pagelinelimits[0] < fisrtlinechangelimit) ):   #(((count == 1) &&((i+2*gazesteps) - pagelinelimits[1] < fisrtlinechangelimit)) && (newpagestart==0))
                #set new page start
                newpagestart = i + 2*gazesteps     #+floor(gazesteps/2);
                pagelinelimits[0] = newpagestart
            else:
                # allagh dhmhtrhs 27.10.2022 (gia arxh)
                if( ygazesfil[i] > firtlineminimumheight ):
                    count = count+1
                    add(pagelinelimits, count, i + 2*gazesteps)    #+floor(gazesteps/2);
                    ylinemedianaux = Median( ygazesfil, pagelinelimits[count-1],  pagelinelimits[count]+1 )

            i = i+gazejump
            currline = ylinemedianaux
            if(count>1):
                prevline = Median(ygazesfil, pagelinelimits[count-2], pagelinelimits[count-1]+1)
            
            if ( (count > 0) and (pagelinelimits[count]-pagelinelimits[count-1]<gazejump+5) ):
                i = i-gazejump+gazesteps
                pagelinelimits[count] = 0
                errorgazejump = count
                count = count-1
            elif( ( (count>0) and (count<=pagelines-1) and (pagelinelimits[count]-pagelinelimits[count-1]<linechangelimit) ) or ( (count>1) and (count<=pagelines) and (currline-prevline<epsilon) ) ): 
                if( (count>0) and (pagelinelimits[count]-pagelinelimits[count-1] < linechangelimit) ):
                    errorlinechangelimit = count

                if ( (count>1) and ((ylinemedianaux-Median(ygazesfil, pagelinelimits[count-2], pagelinelimits[count-1]+1))<epsilon) ):
                    errorepsilon = count

                pagelinelimits[count-1] = pagelinelimits[count]
                pagelinelimits[count] = 0            
                count = count-1
                
                # now we have new lines, recalculate against previous
                currline = Median( ygazesfil, pagelinelimits[count-1], pagelinelimits[count]+1 )
                if( count > 1 ):
                    prevline = Median(ygazesfil, pagelinelimits[count-2], pagelinelimits[count-1]+1)
                    
                if( count>1  and count<=pagelines  and currline-prevline < epsilon):
                    pagelinelimits[count-1] = pagelinelimits[count]
                    pagelinelimits[count] = 0            
                    count = count-1
                      
    
        else:
            i = i+1   
            
    numberofcuts = len(pagelinelimits)

    #pagelinelimitscut=pagelinelimits(~flag);
    pagelinelimitscut = pagelinelimits[0:pagelines]
    while(len(pagelinelimitscut)<pagelines):
        pagelinelimitscut.append(0)
        


    #  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ # # # # # # # # # # # # # #  ALLAGH 29-11-2022  # # # # # # # # # # # # # # #  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  #

    # # IRO ALLAGH # # 
    # # fill rest empty indexes in pagelinelimits with zeros (as I want len(pagelinelimits) = 10 ) # # #
    while( len(pagelinelimits) < 10 ):
        pagelinelimits.append(0)
    # # # end of fill # # #
    

    # # DIMITRIS ALLAGH # # 
    ylinemedian = []
    if( pagelines+1 < len(pagelinelimits) ):
        for count in range(pagelines+1):
            endpoint= pagelinelimits[count+1]
            if(endpoint!=0):
                ylinemedian.append( Median( ygazesfil, pagelinelimits[count] ,endpoint+1 ) )
            else:
                break


    for count in range(1, len(ylinemedian)):
        if(  len(pagelinelimitscut)>pagelines and ylinemedian[count]+pagejumpthreshold<ygazesfil[pagelinelimits[count]] ):
            pagelinelimitscut[count] = pagelinelimits[count+1]

            if( pagelinelimits[count+2] != 0 ):
                pagelinelimitscut[count+1] = pagelinelimits[count+2]
            count += 1


    # # IRO ALLAGH # #
    # # # # check if I add zeros in pagelinelimits, in order to delete them # # # #
    pagelinelimits = [ pagelinelimits[0] ] + [ pagelinelimits[i] for i in range(1,len(pagelinelimits)) if pagelinelimits[i]!=0 ]
    # # # # except from first cut, that might be in index x=0, all the other zeros I want to be deleted # # # 

    # # # # # Remove dublicates from pagelinelimitscut and pagelinelimits # # # # # # 
    pagelinelimitscut = list(dict.fromkeys(pagelinelimitscut))
    pagelinelimits = list(dict.fromkeys(pagelinelimits))
    # # # # # # End of remove doubles # # # # # # # # # #

    # # # # # Remove zeros from pagelinelimitscut
    pagelinelimitscut = [pagelinelimitscut[k] for k in range(len(pagelinelimitscut)-1) if pagelinelimitscut[k]!=0] + [pagelinelimitscut[-1]]
    # # # end of remove zeros 

    #  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  # # # # # # # # # # # # # #  TELOS ALLAGHS 29-11-2022  # # # # # # # # # # # # # # # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  #


    #for count=1:length(pagelinelimitscut)-1:
    #  ylinemedian(count)=median(ygazesfil(pagelinelimitscut(count):pagelinelimitscut(count+1)));
    #set y coord of last line
    
    pagelinelimitscut, flag, crashlist, ylastline = pagelinelimts_handleErrors(pagelinelimitscut, ygazesfil, lastlinegazejump, subject_no, text, pageno, secondRun, errorepsilon, errorlinechangelimit, errorgazejump, lastlinewindow, errorcrashtxt, crashlist, runcrashestxt, cutsUItxt)
    if(flag==0):
        return pagelinelimitscut, flag, crashlist, numberofcuts
    
    #******** Try to filter noise at the end using standard deviation ********%
    # Initialize stdindex 
    stdindex = None
    # Define the window size
    window_size = 50
    # Initialize an array to store standard deviations
    std_deviation_results = np.zeros(len(ygazes))
    # Calculate standard deviation for each window
    for stdindex in range(pagelinelimitscut[-1], len(ygazes) - window_size + 1):
        window_data = ygazes[stdindex:stdindex+window_size]
        std_deviation_results[stdindex] = statistics.stdev(window_data)
    # Plot the standard deviation results
    #plt.plot(range(1, len(ygazes)+1), std_deviation_results, 'g')
    #plt.title(plotTitle)
    # Find the index after the last cut where std goes up, cut and
    for stdindex in range(pagelinelimitscut[-1], len(ygazes) - window_size + 1):
        window_data = ygazes[stdindex:stdindex+window_size]
        std_deviation_results[stdindex] = statistics.stdev(window_data)
        if (std_deviation_results[stdindex] > 50):
            break

    # Find last line end
    pagelinelimitscut, ylinemedian, lastlineend = pagelinelimits_lastline(ygazesfil,pagelinelimits,pagelinelimitscut,lastlinegazejump, ylastline, ylinestep, epsilon, linechangelimit, pagelines, linegazesno, i, count)


    #********* Traps ********#
    # Check last line trap
    # get the mean of the standard deviation till the end.
    if( stdindex==None ):
        mean_std = 0
    else:
        mean_std = statistics.mean(std_deviation_results[stdindex:])
    # If the mean is above a threshold, then we have a cut
    if mean_std < 100:
        pagelinelimitscut, flag, crashlist = pagelinelimits_lastlinetrap(ylastline, lastlineendtrap, ygazesfil, lastlineend, pagelinelimitscut, secondRun, subject_no, text, exam, pageno, errorcrashtxt, endwindow, crashlist, runcrashestxt, cutsUItxt)
        if(flag==0):
            return pagelinelimitscut, flag, crashlist, numberofcuts
    
    
    # Check if we have lost a line
    pagelinelimitscut, avggazesperstep, flag, crashlist = pagelinelimits_linecheck(ylastline, linethreshold, subject_no, text, exam, pageno, secondRun, pagelinelimitscut, ygazesfil, crashlist, errorcrashtxt, runcrashestxt, cutsUItxt)
    if(flag==0):
        return pagelinelimitscut, flag, crashlist, numberofcuts
    
    # check if the number of gazes of last line is below the threshold of double the average of other lines
    pagelinelimitscut, flag, crashlist = pagelinelimits_lastlinecheck(pagelinelimitscut, avggazesperstep, subject_no, text,exam, pageno, secondRun, ygazesfil, crashlist, errorcrashtxt, runcrashestxt, cutsUItxt)
    if(flag==0):
        return pagelinelimitscut, flag, crashlist, numberofcuts
    
    # check if the difference of successive y medians of lines are within bounds
    pagelinelimitscut, flag, crashlist = pagelinelimits_checkyjumps(ylinemedian, trapmaxylinemeddiff, trapminylinemeddiff, subject_no, text,exam, pageno, secondRun, pagelinelimitscut, ygazesfil, crashlist, errorcrashtxt, runcrashestxt, cutsUItxt) 
    if(flag==0):
        return pagelinelimitscut, flag, crashlist, numberofcuts
    
    #  if found_error %(pagelinelimitscut(end)==0) || (pagelinelimitscut(end)+lastlinegazejump>length(ygazesfil)) || (ybackread-ylastline>epsilon) || ((length(ygazesfil)-lastlineend)>mean(diff(pagelinelimitscut))/1) || (ylinemeddiffmax>trapmaxylinemeddiff)||(ylinemeddiffmin<trapminylinemeddiff)
    #   fprintf(fid,'\n::::. end of run .::::')  
    #   fprintf(fid,'\n')
    #  end 

    print("pagelinelimitscut = ",pagelinelimitscut)
    saveCuts(pagelinelimitscut, ygazesfil, subject_no, exam, text, pageno, cutsUItxt)
    return pagelinelimitscut, flag, crashlist, numberofcuts




def pagelinelimits_linecheck(ylastline, linethreshold, subject_no, text, exam, pageno, secondRun, pagelinelimitscut, ygazesfil, crashlist, errorcrashtxt, runcrashestxt, cutsUItxt):
    #check if the average number of gazes for each step is within limits
    # # calculate the gazes for each step without the last one
    gazesperstep = []
    for count in range(len(pagelinelimitscut)-2):
        gazesperstep.append( pagelinelimitscut[count+1] - pagelinelimitscut[count] )
    
    # get the average gazes for step
    if(gazesperstep==[]):
        avggazesperstep = 0
    else:
        avggazesperstep = np.mean(gazesperstep)

    #add new trap get the median from the last cut + average y gazes line. Check if this median is within the threshold of being a new line
    tilend = math.ceil(pagelinelimitscut[-1] + avggazesperstep)
    if( tilend > len(ygazesfil) ):
        tilend = len(ygazesfil)

    flag = 1
    endmedian = Median(ygazesfil, pagelinelimitscut[-1], tilend)
    
    linelengththreshold = avggazesperstep/6
    
    if( tilend-pagelinelimitscut[-1]>linelengththreshold and endmedian>ylastline+linethreshold and endmedian<ylastline+2*linethreshold ):
        flag = 0
        
        # clear pagelinelimitscut from remaining zeros
        pagelinelimitscut = [pagelinelimitscut[0]] + [pagelinelimitscut[j] for j in range(1,len(pagelinelimitscut)) if pagelinelimitscut[j]!=0]
        
        fid = open(errorcrashtxt, 'a+')
        fid.write('Subject %d Exam %d Text %s Page %d is lost - May have lost last line (ERROR.03, %d)\n' %(subject_no,exam,text,pageno,secondRun))

        if(secondRun==False):
            crashlist.append(pageno)

        if(secondRun==True):
            saveCrashCuts(pagelinelimitscut, ygazesfil, subject_no, exam, text, pageno, runcrashestxt)

        saveCuts(pagelinelimitscut, ygazesfil, subject_no, exam, text, pageno, cutsUItxt)

        fid.write('\n')
        fid.close()

    return pagelinelimitscut, avggazesperstep, flag, crashlist


def pagelinelimits_lastlinecheck(pagelinelimitscut, avggazesperstep, subject_no, text, exam, pageno, secondRun, ygazesfil, crashlist, errorcrashtxt, runcrashestxt, cutsUItxt):
    flag = 1
    
    #get the gazes of last line
    lastLineGazes = pagelinelimitscut[-1] - pagelinelimitscut[-2]

    # check if number of gazes of last line is below the threshold of double the average of other lines
    if( lastLineGazes > 2*avggazesperstep ):
        flag = 0
        
        # clear pagelinelimitscut from remaining zeros
        pagelinelimitscut = [pagelinelimitscut[0]] + [pagelinelimitscut[j] for j in range(1,len(pagelinelimitscut)) if pagelinelimitscut[j]!=0]

        fid = open(errorcrashtxt, 'a+')
        fid.write('Subject %d Exam %d Text %s Page %d is lost - Last line too long trap (ERROR.04, %d)\n' %(subject_no,exam,text,pageno,secondRun))
        fid.write('last line gazes: %d, above twice the average: %d (ERR108)\n' %(lastLineGazes, avggazesperstep))
    
        if(secondRun==False):
            crashlist.append(pageno)

        if(secondRun==True):
            saveCrashCuts(pagelinelimitscut, ygazesfil, subject_no, exam, text, pageno, runcrashestxt)

        saveCuts(pagelinelimitscut, ygazesfil, subject_no, exam, text, pageno, cutsUItxt)

        fid.write('\n')
        fid.close()

    return pagelinelimitscut, flag, crashlist



def pagelinelimits_checkyjumps(ylinemedian, trapmaxylinemeddiff, trapminylinemeddiff, subject_no, text,exam, pageno, secondRun, pagelinelimitscut, ygazesfil, crashlist, errorcrashtxt, runcrashestxt, cutsUItxt):
    flag = 1
    
    #check if the difference of successive y medians of lines are within bounds
    ylinemediandiff = np.diff(ylinemedian)
    ylinemeddiffmax=max(ylinemediandiff)
    ylinemeddiffmin=min(ylinemediandiff)

    if( (ylinemeddiffmax > trapmaxylinemeddiff) or (ylinemeddiffmin < trapminylinemeddiff) ):
        
        flag = 0
        
        # clear pagelinelimitscut from remaining zeros
        pagelinelimitscut = [pagelinelimitscut[0]] + [pagelinelimitscut[j] for j in range(1,len(pagelinelimitscut)) if pagelinelimitscut[j]!=0]

        fid = open(errorcrashtxt, 'a+')
        fid.write('Subject %d Exam %d Text %s Page %d is lost - wrong y jump (ERROR.03, %d)\n' %(subject_no,exam,text,pageno,secondRun))
            
        if (ylinemeddiffmax > trapmaxylinemeddiff):
            ylinemeddiffmax = floor(ylinemeddiffmax)
            fid.write('+ Ylinemeddiffmax: %d > trapmaxylinemeddiff: %d (ERR106)\n' %(ylinemeddiffmax, trapmaxylinemeddiff))

        if(ylinemeddiffmin < trapminylinemeddiff):
            ylinemeddiffmin = floor(ylinemeddiffmin)
            fid.write('+ Ylinemeddiffmin: %d < trapminylinemeddiff: %d (ERR107)\n' %(ylinemeddiffmin, trapminylinemeddiff))

        fid.write('\n')
        fid.close()

        
        if(secondRun==False):
            crashlist.append(pageno)

        if(secondRun==True):
            saveCrashCuts(pagelinelimitscut, ygazesfil, subject_no, exam, text, pageno, runcrashestxt)

        saveCuts(pagelinelimitscut, ygazesfil, subject_no, exam, text, pageno, cutsUItxt)
       
        print("pagelinelimitscut = ",pagelinelimitscut)
        
    return pagelinelimitscut, flag, crashlist


def pagelinelimts_handleErrors(pagelinelimitscut, ygazesfil, lastlinegazejump, subject_no, text, pageno, secondRun, errorepsilon, errorlinechangelimit, errorgazejump, lastlinewindow, crashfilename, crashlist, runcrashestxt, cutsUItxt):
    exam = 1
    # if( (pagelinelimitscut[-1]==0) or (len(pagelinelimitscut) < pagelines) or (pagelinelimitscut[-1]+lastlinegazejump > len(ygazesfil)) ):
    if( (pagelinelimitscut[-1]==0) or (pagelinelimitscut[-1]+lastlinegazejump > len(ygazesfil)) ):
        ylastline = 0
        
        flag = 0
        
        # clear pagelinelimitscut from remaining zeros
        pagelinelimitscut = [pagelinelimitscut[0]] + [pagelinelimitscut[j] for j in range(1,len(pagelinelimitscut)) if pagelinelimitscut[j]!=0]

        fid = open(crashfilename, 'a')
        fid.write('Subject %d Exam %d Text %s Page %d is lost - missing line in general (ERROR.01, %d)\n' %(subject_no, exam, text, pageno, secondRun))
        
        if(errorepsilon > -1):
            fid.write('+ Line jump is too short in step: %d (ERR101)\n' %(errorepsilon-1))
            
        if(errorlinechangelimit > -1):
            fid.write('+ Line is too short in step: %d (ERR102)\n' %(errorlinechangelimit-1))
            
        if(errorgazejump > -1):
            fid.write('+ Error gazejump in step: %d (ERR103)\n' %(errorgazejump-1))


        fid.write('\n')
        fid.close()

        
        if(secondRun==False):
            crashlist.append(pageno)

        if(secondRun==True):
            saveCrashCuts(pagelinelimitscut, ygazesfil, subject_no, exam, text, pageno, runcrashestxt)

        saveCuts(pagelinelimitscut, ygazesfil, subject_no, exam, text, pageno, cutsUItxt)
        
        
        #set(gcf,'Visible','off') 
        """
        nozerospagelinelimitscut = [i for i in pagelinelimitscut if i != 0]
        ygazesfilpoints = findPlotpoints(pagelinelimitscut,ygazesfil)
        plt.plot(nozerospagelinelimitscut, ygazesfilpoints,'o')
        plt.title(['Line steps in page ', str(pageno), ', ', str(secondRun)])
        """
        
        print("pagelinelimitscut = ",pagelinelimitscut)
        
    else:
        flag=1
        ylastline = Median( ygazesfil, pagelinelimitscut[-1], min(pagelinelimitscut[-1]+lastlinewindow+1, len(ygazesfil)) )
    
    return pagelinelimitscut, flag, crashlist, ylastline


def pagelinelimits_lastline(ygazesfil, pagelinelimits, pagelinelimitscut, lastlinegazejump, ylastline, ylinestep, epsilon, linechangelimit, pagelines, linegazesno, yindex, count):
    #find last line end
    startsearch = pagelinelimitscut[-1]+lastlinegazejump
    if startsearch >= len(ygazesfil):
        startsearch = pagelinelimitscut[-1] - 1
    lastlineend = findlastline(ygazesfil, startsearch, ylastline, ylinestep)

    i = yindex
    while( i+1 < len(ygazesfil)-1 ):
        if( lastlineend+1 >= len(ygazesfil) ):
            break
        for i in range(lastlineend+1, len(ygazesfil)):
            if(  (abs(ygazesfil[i]-ylastline) < epsilon) and (i-lastlineend<linechangelimit) and (i+50 < len(ygazesfil)) or 
            ( (count>0) and (Median(ygazesfil, lastlineend, pagelinelimits[count])-Median(ygazesfil, pagelinelimits[count-1], pagelinelimits[count]) < epsilon) )  ): # and (Median(ygazesfil, lastlineend, pagelinelimits[count])-Median(ygazesfil, pagelinelimits[count-1], pagelinelimits[count]) >= 0) # To trito meros ths 2hs sxeshs tou OR (i.e (Median(ygazesfil, lastlineend, pagelinelimits[count])-Median(ygazesfil, pagelinelimits[count-1], pagelinelimits[count]) >= 0) ) mpike giati iparxei diaforetikh diaxeirish tou NULL/NaN se matlab & python

                startsearch = i+1
                lastlineend = findlastline(ygazesfil,startsearch,ylastline,ylinestep)
                
                break
        

    #find last sudden drop (*****)
    lastlineydrop = Median(ygazesfil, -1-linegazesno, len(ygazesfil))   
    # print("lastlineydrop = ",lastlineydrop) 
    for i in range(len(ygazesfil)):
        if(lastlineydrop-ygazesfil[i] < 2*epsilon):
            pageend = i
    
    
    ##################
    if( len(pagelinelimitscut) > pagelines+1 ):
        pagelinelimitscut = pagelinelimitscut[:pagelines+1]
    
    if( len(pagelinelimitscut) == pagelines+1 ):
        if( pageend < lastlineend ):
            pagelinelimitscut[-1] = pageend
        else:
            pagelinelimitscut[-1] = lastlineend
    else:
        if( pageend < lastlineend ):
            pagelinelimitscut.append( pageend )
        else:
            pagelinelimitscut.append( lastlineend )
            
    ####################      
            
            
    # if (pageend < lastlineend):
    #     pagelinelimitscut.append(pageend)
    # else:
    #     pagelinelimitscut.append(lastlineend)


    ylinemedian = []
    for count in range(0, len(pagelinelimitscut)-1):
        add( ylinemedian, count, Median(ygazesfil, pagelinelimitscut[count], pagelinelimitscut[count+1]+1) )
    
    return pagelinelimitscut, ylinemedian, lastlineend


def pagelinelimits_lastlinetrap(ylastline, lastlineendtrap, ygazesfil, lastlineend, pagelinelimitscut, secondRun, subject_no, text, exam, pageno, errorcrashtxt, endwindow, crashlist, runcrashestxt, cutsUItxt):
    # check if y of last line is the same as the back-read y median
    #  endwindow = mean(diff(pagelinelimitscut))/4
    #  do net allow endwindow to be too small
    if(endwindow < 150):
        endwindow = 150

    if(secondRun == True):
        endwindow = 300

    flag = 1

    if( endwindow*2 > len(ygazesfil) ):
        ybackread=Median(ygazesfil,0, len(ygazesfil))
    else:
        ybackread=Median(ygazesfil,-1-endwindow*2, len(ygazesfil))
        
    diffpagelinelimitscut = np.diff(pagelinelimitscut)
    diffpagelinelimitscut = diffpagelinelimitscut.tolist()    

    if( (ybackread-ylastline>lastlineendtrap) or ((len(ygazesfil)-lastlineend)>mean(diffpagelinelimitscut)/1) ): #or ((abs(ybackread-ylastline)>epsilon)&&(abs(ybackread-ylastline)<140))
    #    if ~(max(ygazesfil(lastlineend+1:end))<ylastline)||~((length(ygazesfil)-lastlineend)>2*mean(diff(pagelinelimitscut)))
        
        flag = 0
        
        # clear pagelinelimitscut from remaining zeros
        pagelinelimitscut = [pagelinelimitscut[0]] + [pagelinelimitscut[j] for j in range(1,len(pagelinelimitscut)) if pagelinelimitscut[j]!=0]
        
        fid = open(errorcrashtxt, 'a+')
        fid.write('Subject %d Exam %d Text %s Page %d is lost - lost line (ERROR.02, %d)\n' %(subject_no,exam,text,pageno,secondRun))
            
        if(ybackread-ylastline>lastlineendtrap):
            fid.write('+ Ybackread:%d - ylastline:%d > lastlineendtrap:%d (ERR104)\n' %(ybackread,ylastline,lastlineendtrap))
            
        if((len(ygazesfil)-lastlineend)>mean(diffpagelinelimitscut)/1):
            #fprintf('length(ygazesfil) - lastlineend:%f > mean(diff(pagelinelimitscut))/1:%f',(length(ygazesfil)-lastlineend),mean(diff(pagelinelimitscut))/1)
            fid.write('+ Second reading or last step away from last gaze (ERR105)\n')

        fid.write('\n')
        fid.close()

        
        if(secondRun==False):
            crashlist.append(pageno)

        if(secondRun==True):
            saveCrashCuts(pagelinelimitscut, ygazesfil, subject_no, exam, text, pageno, runcrashestxt)
        
        saveCuts(pagelinelimitscut, ygazesfil, subject_no, exam, text, pageno, cutsUItxt)
        
        print("pagelinelimitscut = ",pagelinelimitscut)
    
    return pagelinelimitscut, flag, crashlist



def saveCuts(coords, ygazes, subject_no, exam, text, pageno, cutsUItxt):
    fid = open(cutsUItxt, 'a')
    fid.write('Subject %d Exam %d Text %s Page %d\n' %(subject_no, exam, text, pageno))
    fid.write('Line limit cuts\n')
    for index in range(0, len(coords)):
        fid.write('(%d, %d)\n' %(coords[index],ygazes[coords[index]]))

    fid.write('Filtered y gazes\n')
    for i in range(len(ygazes)):
        fid.write('%d,'%(ygazes[i]))
    fid.write('\n')


def saveCrashCuts(coords, ygazes, subject_no, exam, text, pageno, runcrashestxt):
    fid = open(runcrashestxt, 'a')
    fid.write('Subject %d Exam %d Text %s Page %d\n' %(subject_no,exam,text,pageno))
    fid.write('Line limit cuts\n')
    for index in range(0, len(coords)):
        fid.write('(%d, %d)\n' %(coords[index],ygazes[coords[index]]))

    fid.write('Filtered y gazes\n')
    for i in range(len(ygazes)):
        fid.write('%d,'%(ygazes[i]))
    fid.write('\n')


def add(l,count,point):
    if(len(l)-1 >= count):
        l[count] = point
    else:
        l.append(point)


def Median(x, a, b):
    if( a < 0 or a==1 ):
        a=0
    
    if(a==b):
        med = x[a]
    else:
        try:
            med = statistics.median(x[a : b])
        except statistics.StatisticsError as e:
            med = math.nan  # edw eixame problima metaxi matlab:nan kai python, giafto balame math.nan opoy einai san float(nan) kai den tha exw problima kai stis praxeis
    

    
    return med


"""
def findPlotpoints(pagelinelimitscut,ygazesfil):
    ygazesfilpoints = []
    for i in pagelinelimitscut:
        ygazesfilpoints.append(ygazesfil[i])
    
    return ygazesfilpoints
"""