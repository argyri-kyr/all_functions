


import time
from asyncio.windows_events import NULL
from tkinter import *
import tkinter
from PIL import Image,  ImageTk

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import eyeradarlogo_path


def vergence_gui():
    global greektexts, uktexts, ustexts
    greektexts = ['visit', 'zoo', 'island', 'olympia', 'efeyreseis', 'psaras', 'zebra', 'morning', 'visitloud', 'eilikrinia', 'doro', 'treno', 'RAN', 'decodesentences3v', 'decoderealwords2v', 'decodepseudowords2v', 'visualrecogn3v', 'visualortho3v', 'rantwopart1', 'rantwopart2']
    uktexts = ['sunny', 'midfred','armyjet', 'midfredloud', 'enemypie', 'horse', 'jockey', 'gasmask']
    ustexts = ['sunnyus', 'midfredus','armyjetus', 'midfredloudus', 'enemypieus', 'horseus', 'jockeyus', 'gasmaskus']

    global root
    root = Tk(className=' eyeRadar  DYSLEXIA')

    w = 1400 # width for the Tk root
    h = 980 # height for the Tk root

    # # get screen width and height
    ws = 1920    # ws = root.winfo_screenwidth() # width of the screen
    hs = 1080    # hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2) - 40

    # set the dimensions of the screen 
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.configure(bg='#FDBD67')

    # root.geometry("1000x900")

    # #  FRAME 1  # #
    
    frame1 = Frame(root, bg='#FDBD67')

    # subject's id space
    global number_entry
    number_entry = Entry(frame1, width=25, justify='center', font=('Arial', 15))
    number_entry.grid(row=0, column=1, pady = (40,10), ipady=10, sticky=W)
    number_entry.focus_force()
    number_label = Label(frame1, text="Enter subject's number ", font=('Arial', 15), bg='#FDBD67')
    number_label.grid(row=0, column=0, padx=(0,40), pady = (40,10), sticky=W)


    # range id space
    global range_entry
    range_entry = Entry(frame1, width=25, justify='center', font=('Arial', 15))
    range_entry.config(state='disabled')
    range_entry.grid(row=1, column=1, pady=(40,10), ipady=10, sticky=W)
    range_button = Button(frame1, text="Use Range", width=20, height=2, justify='left', bg='#ffebcc', font=('Arial', 15), command=useRange)
    range_button.grid(row=1, column=0, padx=(0,40), pady=(40,10), sticky=W)

    
    # start gaze space
    global start_entry
    start_entry = Entry(frame1, width=25, justify='center', font=('Arial', 15))
    start_entry.grid(row=0, column=3, pady = (40,10), ipady=10, sticky=W)
    start_label = Label(frame1, text="Gaze Start", font=('Arial', 15), bg='#FDBD67')
    start_label.grid(row=0, column=2, padx=(100,40), pady = (40,10), sticky=W)
    

    # end gaze space
    global end_entry
    end_entry = Entry(frame1, width=25, justify='center', font=('Arial', 15))
    end_entry.grid(row=1, column=3, pady = (15,10), ipady=10, sticky=W)
    end_label = Label(frame1, text="Gaze End", font=('Arial', 15), bg='#FDBD67')
    end_label.grid(row=1, column=2, padx=(100,40), pady = (15,10), sticky=W)
    

    

    # #  FRAME 2  # #
    frame2 = Frame(root, bg='#FDBD67')

    # pages space
    page_label = Label(frame2, text="Pages", font=('Arial', 15), background='#FDBD67')
    page_label.grid(row=1, column=0,  padx=(60,80), pady = (50,20))

    # pages space
    global pagescheckbuttonsstate
    pagescheckbuttonsstate = []
    total_pages = 5

    for i in range(total_pages + 1):
        if  ( i < total_pages ):
            checkvar = IntVar()
            textcheckbox = Checkbutton(frame2, text=i+1, font=('Arial', 14), variable=checkvar, onvalue=1, offvalue=0, bg='#FDBD67')
            textcheckbox.grid(row=1, column=i+1, padx=40, pady=(50,20), sticky=W)
            pagescheckbuttonsstate.append(checkvar)

        else:
            checkall_button = Button(frame2, text="Check all", width=10, height=1, bg='#ffebcc', font=('Arial', 14), command=checkallpages)
            checkall_button.grid(row=1, column=i+1, padx = (20,50), pady = (50,20))

            uncheckall_button = Button(frame2, text="Uncheck all", width=10, height=1, bg='#ffebcc', font=('Arial', 14), command=uncheckallpages)
            uncheckall_button.grid(row=1, column=i+2, padx = (5,50), pady = (50,20))


    pagescheckbuttonsstate[0].set(1)  # set default page=1 button's state as  -- Checked --


    # #  FRAME 3  # #

    # label text space
    frame3 = Frame(root, bg='#FDBD67')
    text_label = Label(frame3, text=" ....::: Texts :::.... ", font=('Arial', 17), bg='#FDBD67')
    text_label.grid(row=0, column=2,  pady = (20,20))  #padx=(430,5)

    # greek texts space
    greekrows = 0
    global greekcheckbuttonsstate
    greekcheckbuttonsstate = []
    for i in range(len(greektexts)):
        if(i%5==0):
            padding_left=20
        elif(i%5==1):
            padding_left=100
        else:
            padding_left=40

        checkvar = IntVar()
        textcheckbox = Checkbutton(frame3, text=greektexts[i], font=('Arial', 14), variable=checkvar, onvalue=1, offvalue=0, bg='#FDBD67')
        textcheckbox.grid(row=1+int(i/5), column=i%5, padx=padding_left, pady=5, sticky=W)
        greekcheckbuttonsstate.append(checkvar)
        
        # greekcheckbuttonsstate[-1].set(1)  # set default button's state as  -- Checked --
       
        greekrows = int(i/5)
    
    greekcheckbuttonsstate[-1].set(0)   # Uncheck RAN text

    # uk texts space
    ukrows = 0
    global ukcheckbuttonsstate
    ukcheckbuttonsstate = []
    for i in range(len(uktexts)):
        if(i%5==0):
            padding_left=20
        elif(i%5==1):
            padding_left=100
        else:
            padding_left=40

        checkvar = IntVar()
        textcheckbox = Checkbutton(frame3, text=uktexts[i], font=('Arial', 14), variable=checkvar, onvalue=1, offvalue=0, bg='#FDBD67')
        textcheckbox.grid(row=1+greekrows+1+int(i/5), column=i%5, padx=padding_left, pady=5, sticky=W)
        ukcheckbuttonsstate.append(checkvar)
        
        # ukcheckbuttonsstate[-1].set(1)  # set default button's state as  -- Checked --   
                                                                                
        ukrows = greekrows+1+int(i/5)

    # us texts space
    usrows = 0
    global uscheckbuttonsstate
    uscheckbuttonsstate = []
    for i in range(len(ustexts)):
        if(i%5==0):
            padding_left=20
        elif(i%5==1):
            padding_left=100
        else:
            padding_left=40

        checkvar = IntVar()
        textcheckbox = Checkbutton(frame3, text=ustexts[i], font=('Arial', 14), variable=checkvar, onvalue=1, offvalue=0, bg='#FDBD67')
        textcheckbox.grid(row=1+ukrows+1+int(i/5), column=i%5, padx=padding_left, pady=5, sticky=W)
        uscheckbuttonsstate.append(checkvar)

        # uscheckbuttonsstate[-1].set(1)  # set default button's state as  -- Checked --                                                                                

        usrows = ukrows+1+int(i/5)


    # #  FRAME 4  # #   
       
    frame4 = Frame(root, pady=30, bg='#FDBD67')
    uncheckall_button = Button(frame4, text="Uncheck all", width=15, height=2, bg='#ffebcc', font=('Arial', 15), command=uncheckall)
    uncheckall_button.grid(row=0, column=0, padx = (15,40), pady = (20,10))

    checkgr_button = Button(frame4, text="Check GR", width=15, height=2, bg='#ffebcc', font=('Arial', 15), command=checkgr)
    checkgr_button.grid(row=0, column=1, padx = (15,40), pady = (20,10))

    checkuk_button = Button(frame4, text="Check UK", width=15, height=2, bg='#ffebcc', font=('Arial', 15), command=checkuk)
    checkuk_button.grid(row=0, column=2, padx = (15,40), pady = (20,10))

    checkus_button = Button(frame4, text="Check US", width=15, height=2, bg='#ffebcc', font=('Arial', 15), command=checkus)
    checkus_button.grid(row=0, column=3, padx = (15,40), pady = (20,10))    

    ok_button = Button(frame4, text="OK", width=30, height=2, bg='#ffebcc', font=('Arial', 15), command=ok)
    ok_button.grid(row=1, column=0, padx = (15,40), pady = (10,10), columnspan=2)   

    cancel_button = Button(frame4, text="Cancel", width=30, height=2, bg='#ffebcc', font=('Arial', 15), command=cancel)
    cancel_button.grid(row=1, column=2, padx = (15,40), pady = (15,10), columnspan=2) 
    
    image1 = Image.open(eyeradarlogo_path)   # Dimensions of logo: 240x67
    image2 =  ImageTk. PhotoImage(image1)
    image_label = tkinter.Label(frame4, image=image2, bg='#FDBD67')
    image_label.grid(row=0, column=4, padx=(5,15), pady=(10,10), rowspan=2)  


        
    frame1.pack()
    frame2.pack()
    frame3.pack()
    frame4.pack()
    
    # root.protocol("WM_DELETE_WINDOW", close)
    
    root.mainloop()

    # print("sub = ", sub)
    # print("texts = ", texts)
    # print("pages = ", pages)

    return subs, texts, pages, start, end



def useRange():
    range_entry['state'] = 'normal'
    range_entry.focus()


def uncheckall():
    for i in range(len(greekcheckbuttonsstate)):
        greekcheckbuttonsstate[i].set(0)
    
    for i in range(len(ukcheckbuttonsstate)):
        ukcheckbuttonsstate[i].set(0)

    for i in range(len(uscheckbuttonsstate)):
        uscheckbuttonsstate[i].set(0)


def checkgr():
    for i in range(len(greekcheckbuttonsstate)):
        greekcheckbuttonsstate[i].set(1)


def checkuk():
    for i in range(len(ukcheckbuttonsstate)):
        ukcheckbuttonsstate[i].set(1)


def checkus():
    for i in range(len(uscheckbuttonsstate)):
        uscheckbuttonsstate[i].set(1)


def checkallpages():
    for i in range(len(pagescheckbuttonsstate)):
        pagescheckbuttonsstate[i].set(1)


def uncheckallpages():
    for i in range(len(pagescheckbuttonsstate)):
        pagescheckbuttonsstate[i].set(0)


def getSubs():
    subs = NULL
    if( range_entry['state'] == 'disabled' ):
        # subs = [ int(number_entry.get()) ]
        if( number_entry.get().isdigit() ):
            subs = [ int(number_entry.get()) ]
        
        else:
            print("\n Invalid entry in: 'Enter subject's number' box. Try again with one single subject's id ( id must be integer ) .")
            root.destroy()
            time.sleep(3)


    
    elif( range_entry['state'] != 'disabled' ):
        start = int(number_entry.get())
        if(range_entry.get()==""):
            end=start
        else:
            end = int(range_entry.get()) + 1
        subs = [i for i in range(int(start), int(end))]
    
    return subs



def getTexts():
    texts = []

    for i in range(len(greekcheckbuttonsstate)):
        if( greekcheckbuttonsstate[i].get() ):
            texts.append(greektexts[i])
        
    for i in range(len(ukcheckbuttonsstate)):
        if( ukcheckbuttonsstate[i].get() ):
            texts.append(uktexts[i])
    
    for i in range(len(uscheckbuttonsstate)):
        if( uscheckbuttonsstate[i].get() ):
            texts.append(ustexts[i])

    return texts


def getPages():
    pages = []
    for i in range(len(pagescheckbuttonsstate)):
        if( pagescheckbuttonsstate[i].get() ):
            pages.append(i+1)
    
    return pages


def getStart():
    if(start_entry.get()!=''):
        start = int(start_entry.get())
    else:
        start = ''
    return start


def getEnd():
    if(end_entry.get()!=''):
        end = int(end_entry.get())
    else:
        end = ''
    return end


def ok():
    global subs, texts, pages, start, end
    subs = getSubs()
    texts = getTexts()
    pages= getPages()
    start = getStart()
    end = getEnd()

    root.destroy()


def cancel():
    exit()


def close():
    return


# vergence_gui()