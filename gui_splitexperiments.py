

from asyncio.windows_events import NULL
from tkinter import *
from PIL import Image,  ImageTk
import time


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import eyeradarlogo_path


def gui_splitexperiments():
    global tests, checkbuttonsstate
    tests = ['raven', 'decodesentences', 'decodewordsv2', 'decodepseudov2', 'visualorthov2', 'visualrecognv2', 'phonolrhymes', 'rantwo']
    checkbuttonsstate = []
    
    global root
    root = Tk(className=' eyeRadar  DYSLEXIA')

    w = 1300 # width for the Tk root
    h = 700 # height for the Tk root

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
    number_entry.grid(row=0, column=3, padx=(50,30), pady=(30,15), ipady=20, sticky=W)
    number_entry.focus_force()
    number_label = Label(frame1, text="Enter subject's number ", font=('Arial', 15), background='#FDBD67')
    number_label.grid(row=0, column=0, padx=(0,50), pady=(30,15))
    
    # range id space
    global range_entry
    range_entry = Entry(frame1, width=30, justify='center', font=('Arial', 15))
    range_entry.config(state='disabled')
    range_entry.grid(row=1, column=3, padx=(50,30), pady=(5,10), ipady=20)
    range_button = Button(frame1, text="Use Range", width=20, height=3, justify='left', bg='#ffebcc', font=('Arial', 15), command=useRange)
    range_button.grid(row=1, column=0, padx=(0,50), pady=(5,10))

    # label text space
    text_label = Label(frame1, text=" ....::: Texts :::.... ", font=('Arial', 19), background='#FDBD67')
    text_label.grid(row=2, column=1, pady=(25,25))  #padx=(430,5)


    # # FRAME 2 # #

    frame2 = Frame(root, background='#FDBD67')
    
    fixed_texts_per_row = 3

    for i in range(len(tests)):
        if(i%fixed_texts_per_row==0):
            padding_left=0
        elif(i%fixed_texts_per_row==1):
            padding_left=90
        else:
            padding_left=40

        checkvar = IntVar()
        textcheckbox = Checkbutton(frame2, text=tests[i], font=('Arial', 14), variable=checkvar, onvalue=1, offvalue=0, background='#FDBD67')
        textcheckbox.grid(row=int(i/fixed_texts_per_row) + 1, column=i%fixed_texts_per_row, padx=padding_left, pady=5, sticky=W)
        checkbuttonsstate.append(checkvar)
    

    # #  FRAME 3  # #
    
    frame3 = Frame(root, pady=30, background='#FDBD67')
    
    checkall_button = Button(frame3, text="Check all", width=15, height=3, bg='#ffebcc', font=('Arial', 15), command=checkall)
    checkall_button.grid(row=0, column=0, padx=(25,50), pady=(0,10))

    uncheckall_button = Button(frame3, text="Uncheck all", width=15, height=3, bg='#ffebcc', font=('Arial', 15), command=uncheckall)
    uncheckall_button.grid(row=0, column=1, padx=(15,50), pady=(0,10))

    ok_button = Button(frame3, text="OK", width=25, height=3, bg='#ffebcc', font=('Arial', 15), command=ok)
    ok_button.grid(row=1, column=0, padx=(15,30), pady=(10,10))   

    cancel_button = Button(frame3, text="Cancel", width=25, height=3, bg='#ffebcc', font=('Arial', 15), command=cancel)
    cancel_button.grid(row=1, column=1, padx=(15,30), pady=(10,10))   

    image1 = Image.open(eyeradarlogo_path)  
    image2 =  ImageTk. PhotoImage(image1)
    image_label = Label(frame3 , image=image2, background='#FDBD67')
    image_label.grid(row=0, column=2, padx=(5,25), pady=(10,10), rowspan=2)  

        
    frame1.pack()
    frame2.pack()
    frame3.pack()
    
    # root.protocol("WM_DELETE_WINDOW", close)
    # root.state('zoomed')
    
    root.mainloop()

    # # return number_entry, range_entry, checkbuttonsstate, ukcheckbuttonsstate, uscheckbuttonsstate, checkbuttonsstate
    # print("subs = ", subs)
    # print("texts = ", texts)

    return subs, texts


def useRange():
    range_entry['state'] = 'normal'
    range_entry.focus()


def uncheckall():
    for i in range(len(checkbuttonsstate)):
        checkbuttonsstate[i].set(0)
        

def checkall():
    for i in range(len(checkbuttonsstate)):
        checkbuttonsstate[i].set(1)


        

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

    for i in range(len(checkbuttonsstate)):
        if( checkbuttonsstate[i].get() ):
            texts.append(tests[i]) 

    return texts


def ok():
    global subs, texts
    subs = getSubs()
    texts = getTexts()
    try:
        root.destroy()
    except:
        return


def cancel():
    exit()


def close():
    return



# gui_splitexperiments(0)