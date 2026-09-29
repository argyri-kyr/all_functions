

from asyncio.windows_events import NULL
from tkinter import *
from PIL import Image,  ImageTk
import time


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import eyeradarlogo_path


def basic_plot_gui():
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

    # root.geometry("1050x950")

    # # FRAME 1 # #

    frame1 = Frame(root, background='#FDBD67')

    # subject's id space
    global number_entry
    number_entry = Entry(frame1, width=30, justify='center', font=('Arial', 15))
    number_entry.grid(row=0, column=2, padx=(70,30), pady=(40,20), ipady=20, sticky=W)
    number_entry.focus_force()
    number_label = Label(frame1, text="Enter subject's number ", font=('Arial', 15), background='#FDBD67')
    number_label.grid(row=0, column=0, padx=(0,200), pady=(20,20))

    
    # range id space
    global range_entry
    range_entry = Entry(frame1, width=30, justify='center', font=('Arial', 15))
    range_entry.config(state='disabled')
    range_entry.grid(row=1, column=2, padx=(70,30), pady=(5,10), ipady=20)
    range_button = Button(frame1, text="Use Range", width=20, height=3, justify='left', bg='#ffebcc', font=('Arial', 15), command=useRange)
    range_button.grid(row=1, column=0, padx=(0,200), pady=(5,20))

    # # Frame 2
    frame2 = Frame(root, background='#FDBD67')
    
    # pages space
    page_label = Label(frame2, text="Select  Pages", font=('Arial', 17), background='#FDBD67')
    page_label.grid(row=1, column=0,  padx=(30,130), pady = (10,10))
    
    global pagescheckbuttonsstate
    pagescheckbuttonsstate = []
    for i in range(1,6):
        checkvar = IntVar()
        textcheckbox = Checkbutton(frame2, text=i, font=3, variable=checkvar, onvalue=1, offvalue=0, background='#FDBD67')
        textcheckbox.grid(row=1, column=i+1, padx =20, pady=(10,10))
        pagescheckbuttonsstate.append(checkvar)

    pagescheckbuttonsstate[0].set(1)

    # label text space
    text_label = Label(frame2, text=" ....::: Texts :::.... ", font=('Arial', 17), background='#FDBD67')
    text_label.grid(row=2, column=1, pady=(30,30))  #padx=(430,5)



    # # FRAME 3 # #

    frame3 = Frame(root, background='#FDBD67')
    
    # Fix appear number of texts per row
    fixed_texts_per_row_greek = 5
    
    # greek texts space
    greekrows = 0
    global greekcheckbuttonsstate
    greekcheckbuttonsstate = []
    for i in range(len(greektexts)):
        if(i%fixed_texts_per_row_greek==0):
            padding_left=20
        elif(i%fixed_texts_per_row_greek==1):
            padding_left=90
        else:
            padding_left=40

        checkvar = IntVar()
        textcheckbox = Checkbutton(frame3, text=greektexts[i], font=('Arial', 14), variable=checkvar, onvalue=1, offvalue=0, background='#FDBD67')
        textcheckbox.grid(row=int(i/fixed_texts_per_row_greek), column=i%fixed_texts_per_row_greek, padx=padding_left, pady=5, sticky=W)
        greekcheckbuttonsstate.append(checkvar)
        
        # greekcheckbuttonsstate[-1].set(1)  # set default button's state as  -- Checked --
        greekrows = int(i/fixed_texts_per_row_greek)
        
    # uk texts space
    ukrows = 0
    global ukcheckbuttonsstate
    ukcheckbuttonsstate = []
    for i in range(len(uktexts)):
        if(i%5==0):
            padding_left=20
        elif(i%5==1):
            padding_left=90
        else:
            padding_left=40

        checkvar = IntVar()
        textcheckbox = Checkbutton(frame3, text=uktexts[i], font=('Arial', 14), variable=checkvar, onvalue=1, offvalue=0, background='#FDBD67')
        textcheckbox.grid(row=greekrows+1+int(i/5), column=i%5, padx=padding_left, pady=5, sticky=W)
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
            padding_left=90
        else:
            padding_left=40

        checkvar = IntVar()
        textcheckbox = Checkbutton(frame3, text=ustexts[i], font=('Arial', 14), variable=checkvar, onvalue=1, offvalue=0, background='#FDBD67')
        textcheckbox.grid(row=ukrows+1+int(i/5), column=i%5, padx=padding_left, pady=5, sticky=W)
        uscheckbuttonsstate.append(checkvar)
        
        # uscheckbuttonsstate[-1].set(1)  # set default button's state as  -- Checked --                                                                                
        usrows = ukrows+1+int(i/5)


    # #  FRAME 3  # #

    frame4 = Frame(root, pady=30, background='#FDBD67')
    uncheckall_button = Button(frame4, text="Uncheck all", width=15, height=3, bg='#ffebcc', font=('Arial', 15), command=uncheckall)
    uncheckall_button.grid(row=0, column=0, padx=(25,40), pady=(10,10))

    checkgr_button = Button(frame4, text="Check GR", width=15, height=3, bg='#ffebcc', font=('Arial', 15), command=checkgr)
    checkgr_button.grid(row=0, column=1, padx=(15,40), pady=(10,10))

    checkuk_button = Button(frame4, text="Check UK", width=15, height=3, bg='#ffebcc', font=('Arial', 15), command=checkuk)
    checkuk_button.grid(row=0, column=2, padx=(15,40), pady=(10,10))

    checkus_button = Button(frame4, text="Check US", width=15, height=3, bg='#ffebcc', font=('Arial', 15), command=checkus)
    checkus_button.grid(row=0, column=3, padx=(15,40), pady=(10,10))    

    ok_button = Button(frame4, text="OK", width=25, height=3, bg='#ffebcc', font=('Arial', 15), command=ok)
    ok_button.grid(row=1, column=0, padx=(15,30), pady=(10,10), columnspan=2)   

    cancel_button = Button(frame4, text="Cancel", width=25, height=3, bg='#ffebcc', font=('Arial', 15), command=cancel)
    cancel_button.grid(row=1, column=2, padx=(15,30), pady=(10,10), columnspan=2)   

    image1 = Image.open(eyeradarlogo_path)  
    image2 =  ImageTk. PhotoImage(image1)
    image_label = Label(frame4 , image=image2, background='#FDBD67')
    image_label.grid(row=0, column=4, padx=(5,25), pady=(10,10), rowspan=2)  

        
    frame1.pack()
    frame2.pack()
    frame3.pack()
    frame4.pack()
    
    # root.protocol("WM_DELETE_WINDOW", close)
    # root.state('zoomed')
    
    root.mainloop()

    # # return number_entry, range_entry, greekcheckbuttonsstate, ukcheckbuttonsstate, uscheckbuttonsstate
    # print("subs = ", subs)
    # print("texts = ", texts)
    # print("pages = ",pages)

    return subs, texts, pages


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


def ok():
    global subs, texts, pages
    subs = getSubs()
    texts = getTexts()
    pages = getPages()
    try:
        root.destroy()
    except:
        return


def cancel():
    exit()


def close():
    return



# fixation_gui()