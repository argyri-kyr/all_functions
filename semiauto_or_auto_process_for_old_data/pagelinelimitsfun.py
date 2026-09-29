from asyncio.windows_events import NULL
from math import floor
import math
from statistics import mean
import numpy as np
from findlastline import findlastline


def pagelinelimitsfun(x, y, pagelines, subject_no, exam, text, pageno, cutsUItxt, errorcrashtxt, runcrashestxt, crashlist, secondRun):
    global pagestart, startwindow
    pagestart = NULL

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


    #finds y axis line limits for a page
    xgazes = x
    ygazes = y
    linegazesno = floor(len(ygazes)/pagelines)
    gazesteps = floor(linegazesno/15)
    gazejump = 2*gazesteps
    startwindow = floor(linegazesno/2)
    endwindow = floor(linegazesno/4)
    lastlinewindow = floor(linegazesno/4)
    linechangelimit = floor(linegazesno/6)
    bottomywindow = floor(linegazesno)
    fisrtlinechangelimit = linechangelimit*2
    trapmaxylinemeddiff = 250
    trapminylinemeddiff = 50
    windowxdropbefore = 4*gazesteps
    windwosxdropafter = 2*gazesteps

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
        gazesteps = floor(linegazesno/20)
        gazejump = 2*gazesteps
        windowxdropbefore = 3*gazesteps
        windwosxdropafter = 4*gazesteps

        fisrtlinechangelimit = linechangelimit
        trapminylinemeddiff = 50
        trapmaxylinemeddiff = 250
        
        #first line starts too far ahead
        winfirstgaze = 2*linegazesno

        xfilterwindow = 20
    
   
    # # # #  filter X, Y gazes # # # #
    # filter gazes with a median filter for Y
    ygazes = [0 if i < 0 else i for i in ygazes]
    ygazesfil = ygazes.copy()

    for i in range (filterwindow, len(ygazes)-filterwindow):
        start = int(i-filterwindow)
        end = int(i+filterwindow)+1

        ygazesfil[i] = Median( ygazes, start, end )

    # filter gazes with a median filter for X
    xgazes = [0 if i < 0 else i for i in xgazes]
    xgazesfil = xgazes.copy()

    for i in range (xfilterwindow, len(xgazes)-xfilterwindow):
        start = int(i-xfilterwindow)
        end = int(i+xfilterwindow)+1

        xgazesfil[i] = Median( xgazes, start, end )    

    xgazes = xgazesfil


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
    
    
    #find the y median from startwindow gazes for determination of first line
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

        if ( i-min(windowxdropbefore,i-pagelinelimits[count]) < xendArray ):
            listxg = xgazes[ i-min(windowxdropbefore,i-pagelinelimits[count]) : xendArray+1]

        elif ( i-min(windowxdropbefore,i-pagelinelimits[count]) > xendArray ):
            listxg = xgazes[ xendArray-1 : i-min(windowxdropbefore,i-pagelinelimits[count])+1]

        elif ( i-min(windowxdropbefore,i-pagelinelimits[count]) == xendArray ):
            listxg = [ xgazes[ xendArray ] ]
        



        maxx = max(listxg)
        indexmax = listxg.index(max(listxg))
        minx = min(listxg)
        indexmin = listxg.index(min(listxg))
        
        if (  ((ygazesfil[i+2*gazesteps]-ygazesfil[i]>ylinestep) and (minx-maxx<xlinestep))  and  (indexmin>indexmax)  ):    #||((myflag==1)&&(minx-maxx<xlinestep/2)))%(xgazes(i+2*gazesteps)-xgazes(i)<xlinestep)
            #if 2nd point is too close to y first point maybe this is the
            #correct start so move 2nd point to first?
            if ( (count == 0) and ((i+2*gazesteps) - pagelinelimits[0] < fisrtlinechangelimit) ):   #(((count == 1) &&((i+2*gazesteps) - pagelinelimits[1] < fisrtlinechangelimit)) && (newpagestart==0))
                #set new page start
                newpagestart = i + 2*gazesteps     #+floor(gazesteps/2);
                pagelinelimits[0] = newpagestart
            else:
                # allagh dhmhtrhs 27.10.2022 (gia arxh)
                if( ygazesfil[i] > 20 ):
                    count = count+1
                    add(pagelinelimits, count, i + 2*gazesteps)    #+floor(gazesteps/2);
                    ylinemedianaux = Median( ygazesfil, pagelinelimits[count-1],  pagelinelimits[count] )

            i = i+gazejump
            
            if ( (count > 0) and (pagelinelimits[count]-pagelinelimits[count-1]<gazejump+5) ):
                i = i-gazejump+gazesteps
                pagelinelimits[count] = 0
                errorgazejump = count
                count = count-1
            elif( ( (count>0) and (pagelinelimits[count]-pagelinelimits[count-1] < linechangelimit) ) or ( (count>1) and (count<pagelines-1) and (ylinemedianaux-Median(ygazesfil, pagelinelimits[count-2], pagelinelimits[count-1]) < epsilon) ) ): 
                if( (count>0) and (pagelinelimits[count]-pagelinelimits[count-1] < linechangelimit) ):
                    errorlinechangelimit = count

                if ( (count>1) and ((ylinemedianaux-Median(ygazesfil, pagelinelimits[count-2], pagelinelimits[count-1]))<epsilon) ):
                    errorepsilon = count

                pagelinelimits[count-1] = pagelinelimits[count]
                pagelinelimits[count] = 0            
                count = count-1
    
        else:
            i = i+1   

    #pagelinelimitscut=pagelinelimits(~flag);
    pagelinelimitscut = pagelinelimits[0:pagelines]


    #  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ # # # # # # # # # # # # # #  ALLAGH 29-11-2022  # # # # # # # # # # # # # # #  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  #

    # # IRO ALLAGH # # 
    # # fill rest empty indexes in pagelinelimits with zeros (as I want len(pagelinelimits) = 10 ) # # #
    while( len(pagelinelimits) < 10 ):
        pagelinelimits.append(0)
    # # # end of fill # # #
    

    # # DIMITRIS ALLAGH # # 
    ylinemedian = []
    if( pagelines+1 < len(pagelinelimits) ):
        for count in range(pagelines):
            endpoint= pagelinelimits[count+1]
            if(endpoint!=0):
                ylinemedian.append( np.median( ygazesfil[pagelinelimits[count] : endpoint] ) )
            else:
                break

    threshold = 20
    for count in range(1, len(ylinemedian)-1):
        if( ylinemedian[count] + threshold < ygazesfil[pagelinelimits[count]] ):
            pagelinelimitscut[count] = pagelinelimits[count+1]

            if( pagelinelimits[count+2] != 0 ):
                pagelinelimitscut[count+1] = pagelinelimits[count+2]
            count += 1


    # # IRO ALLAGH # #
    # # # # check if I add zeros in pagelinelimits, in order to delete them # # # #
    pagelinelimits = [ pagelinelimits[0] ]+ [ pagelinelimits[i] for i in range(1,len(pagelinelimits)) if pagelinelimits[i]!=0 ]
    # # # # except from first cut, that might be in index x=0, all the other zeros I want to be deleted # # # 

    # # # # # Remove dublicates from pagelinelimitscut and pagelinelimits # # # # # # 
    pagelinelimitscut = list(dict.fromkeys(pagelinelimitscut))
    pagelinelimits = list(dict.fromkeys(pagelinelimits))
    # # # # # # End of remove doubles # # # # # # # # # #

    # # # # # Remove zeros from pagelinelimitscut
    pagelinelimitscut = [x for x in pagelinelimitscut if x!=0]
    # # # end of remove zeros 

    #  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  # # # # # # # # # # # # # #  TELOS ALLAGHS 29-11-2022  # # # # # # # # # # # # # # # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  #


    #for count=1:length(pagelinelimitscut)-1:
    #  ylinemedian(count)=median(ygazesfil(pagelinelimitscut(count):pagelinelimitscut(count+1)));
    #set y coord of last line
    if( (pagelinelimitscut[-1]==0) or (len(pagelinelimitscut) < pagelines) or (pagelinelimitscut[-1]+lastlinegazejump > len(ygazesfil)) ):

        flag = 0

        fid = open(errorcrashtxt, 'a')
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
        return pagelinelimitscut, flag, crashlist
    else:
        ylastline = Median(ygazesfil, pagelinelimitscut[-1], min(pagelinelimitscut[-1]+lastlinewindow, len(ygazesfil)) )

    #find last line end
    lastlineend = findlastline(ygazesfil, pagelinelimitscut[-1]+lastlinegazejump, ylastline, ylinestep)

    #  for i in range (pagelinelimitscut[-1]+50, len(ygazesfil)):
    #      if( abs( ygazesfil(i)-ylastline)>ylinestep ):
    #          lastlineend = i-1
    #          break
    #      else:
    #          lastlineend = length(ygazesfil);
    #
    # loop to avoid short line jumps
    #  while( i<len(ygazesfil) :
    #      lastlineend = findlastline(ygazesfil, lastlineend+1, ylastline)
    # for i in range(len(ygazesfil)):
    #     if(ygazesfil[i] == 666):
    #         print(" i1 = ", i)
    #     if(ygazesfil[i]== 993):
    #         print(" i2 = ", i)
    # print("(ygazesfil[-2] = ",ygazesfil[-2])
    
    while( i+1 < len(ygazesfil) ):
        j = lastlineend+1
        for j in range(lastlineend+1, len(ygazesfil)):
            if(  (abs(ygazesfil[j]-ylastline) < epsilon) and (j-lastlineend<linechangelimit) and (j+50 < len(ygazesfil)) or 
            ( ( len(ygazesfil[lastlineend:pagelinelimits[count]])>0) and (count>0) and (Median(ygazesfil, lastlineend, pagelinelimits[count])-Median(ygazesfil, pagelinelimits[count-1], pagelinelimits[count]) < epsilon) )  ):

                startsearch = j+1
                lastlineend = findlastline(ygazesfil,startsearch,ylastline,ylinestep)
                
                break
        
        i=j
        

    #find last sudden drop (*****)
    lastlineydrop = Median(ygazesfil, -1-linegazesno, -1)   
    # print("lastlineydrop = ",lastlineydrop) 
    for i in range(len(ygazesfil)):
        if(lastlineydrop-ygazesfil[i] < 2*epsilon):
            pageend = i
   
    if (pageend < lastlineend):
        pagelinelimitscut.append(pageend)
    else:
        pagelinelimitscut.append(lastlineend)

    ylinemedian = []
    for count in range(0, len(pagelinelimitscut)-1):
        add( ylinemedian, count, Median(ygazesfil, pagelinelimitscut[count], pagelinelimitscut[count+1]) )
   
    # ylinemedian=[ylinemedian,median(ygazesfil(pagelinelimitscut(end-1):pagelinelimitscut(end)))];
    
    #plot pagelinelimits
    # set(gcf,'Visible','off')
    
    """
    ygazesfilpoints = findPlotpoints(pagelinelimitscut,ygazesfil)
    plt.plot(pagelinelimitscut,ygazesfilpoints,'o')
    plt.title(['Line steps in page ', str(pageno), ', ', str(secondRun)])
    """

    # check if y of last line is the same as the back-read y median
    #  endwindow = mean(diff(pagelinelimitscut))/4
    #  do net allow endwindow to be too small
    if(endwindow < 150):
        endwindow = 150

    if(secondRun == True):
        endwindow = 300

    flag = 1

    ybackread=Median(ygazesfil,-1-endwindow*2, -1)
    diffpagelinelimitscut = np.diff(pagelinelimitscut)
    diffpagelinelimitscut = diffpagelinelimitscut.tolist()    

    if( (ybackread-ylastline>lastlineendtrap) or ((len(ygazesfil)-lastlineend)>mean(diffpagelinelimitscut)/1) ): #or ((abs(ybackread-ylastline)>epsilon)&&(abs(ybackread-ylastline)<140))
    #    if ~(max(ygazesfil(lastlineend+1:end))<ylastline)||~((length(ygazesfil)-lastlineend)>2*mean(diff(pagelinelimitscut)))
        
        flag = 0
        
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
   



    #check if the average number of gazes for each step is within limits
    # # calculate the gazes for each step without the last one
    gazesperstep = []
    for count in range(len(pagelinelimitscut)-1):
        gazesperstep.append( pagelinelimitscut[count+1] - pagelinelimitscut[count] )
    
    # get the average gazes for step
    avggazesperstep = mean(gazesperstep)

    #add new trap get the median from the last cut + average y gazes line. Check if this median is within the threshold of being a new line
    tilend = pagelinelimitscut[-1] + avggazesperstep 
    if( tilend >= len(ygazesfil) ):
        tilend = len(ygazesfil)

    endmedian = np.median(ygazesfil[pagelinelimitscut[-1]: tilend])
    if( endmedian>ylastline+linethreshold and endmedian<ylastline+2*linethreshold ):
        flag = 0

        fid = open(errorcrashtxt, 'a+')
        fid.write('Subject %d Exam %d Text %s Page %d is lost - May have lost last line (ERROR.03, %d)\n' %(subject_no,exam,text,pageno,secondRun))

        if(secondRun==False):
            crashlist.append(pageno)

        if(secondRun==True):
            saveCrashCuts(pagelinelimitscut, ygazesfil, subject_no, exam, text, pageno, runcrashestxt)

        saveCuts(pagelinelimitscut, ygazesfil, subject_no, exam, text, pageno, cutsUItxt)

        fid.write('\n')
        fid.close()
        return pagelinelimitscut, flag, crashlist
    

    #get the gazes of last line
    lastLineGazes = pagelinelimitscut[-1] - pagelinelimitscut[-2]

    # check if number of gazes of last line is below the threshold of double the average of other lines
    if( lastLineGazes > 2*avggazesperstep ):
        flag = 0

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
    
    #check if the difference of successive y medians of lines are within bounds
    ylinemediandiff = np.diff(ylinemedian)
    ylinemeddiffmax=max(ylinemediandiff)
    ylinemeddiffmin=min(ylinemediandiff)

    if( (ylinemeddiffmax > trapmaxylinemeddiff) or (ylinemeddiffmin < trapminylinemeddiff) ):
        
        flag = 0
        
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
    
    #  if found_error %(pagelinelimitscut(end)==0) || (pagelinelimitscut(end)+lastlinegazejump>length(ygazesfil)) || (ybackread-ylastline>epsilon) || ((length(ygazesfil)-lastlineend)>mean(diff(pagelinelimitscut))/1) || (ylinemeddiffmax>trapmaxylinemeddiff)||(ylinemeddiffmin<trapminylinemeddiff)
    #   fprintf(fid,'\n::::. end of run .::::')  
    #   fprintf(fid,'\n')
    #  end 

    print("pagelinelimitscut = ",pagelinelimitscut)
    saveCuts(pagelinelimitscut, ygazesfil, subject_no, exam, text, pageno, cutsUItxt)
    return pagelinelimitscut, flag



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
    if( a < 0 ):
        a=0
    
    med = np.median( x[a : b] )
    
    if(a==b):
        med = x[a]
    
    return med


"""
def findPlotpoints(pagelinelimitscut,ygazesfil):
    ygazesfilpoints = []
    for i in pagelinelimitscut:
        ygazesfilpoints.append(ygazesfil[i])
    
    return ygazesfilpoints
"""