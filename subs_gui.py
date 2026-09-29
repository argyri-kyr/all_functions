

from asyncio.windows_events import NULL
from tkinter import *
from PIL import Image,  ImageTk
import time


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import eyeradarlogo_path


def subs_gui():

    global root
    root = Tk(className=' eyeRadar  DYSLEXIA')

    w = 1000 # width for the Tk root
    h = 400 # height for the Tk root

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
    number_entry = Entry(frame1, width=20, justify='center', font=('Arial', 15))
    number_entry.grid(row=0, column=3, padx=(80,20), pady=(40,30), ipady=20, sticky=W)
    number_entry.focus_force()
    number_label = Label(frame1, text="Enter subject's number ", font=('Arial', 15), background='#FDBD67')
    number_label.grid(row=0, column=0, padx=(30,70), pady=(30,30))

    
    # range id space
    global range_entry
    range_entry = Entry(frame1, width=20, justify='center', font=('Arial', 15))
    range_entry.config(state='disabled')
    range_entry.grid(row=1, column=3, padx=(80,20), pady=(5,10), ipady=20)
    range_button = Button(frame1, text="Use Range", width=18, height=2, justify='left', bg='#ffebcc', font=('Arial', 15), command=useRange)
    range_button.grid(row=1, column=0, padx=(30,70), pady=(5,20))



    ok_button = Button(frame1, text="OK", width=20, height=3, bg='#ffebcc', font=('Arial', 15), command=ok)
    ok_button.grid(row=2, column=0, padx=(30,70), pady=(50,10), columnspan=2)   

    cancel_button = Button(frame1, text="Cancel", width=20, height=3, bg='#ffebcc', font=('Arial', 15), command=cancel)
    cancel_button.grid(row=2, column=2, padx=(80,20), pady=(50,10), columnspan=2)   

    image1 = Image.open(eyeradarlogo_path)  
    image2 =  ImageTk. PhotoImage(image1)
    image_label = Label(frame1 , image=image2, background='#FDBD67')
    image_label.grid(row=2, column=4, padx=(50,25), pady=(50,10), rowspan=2)  

        
    frame1.pack()
    
    # root.protocol("WM_DELETE_WINDOW", close)
    # root.state('zoomed')
    
    root.mainloop()

    # # return number_entry, range_entry, greekcheckbuttonsstate, ukcheckbuttonsstate, uscheckbuttonsstate
    # print("subs = ", subs)
    # print("texts = ", texts)

    return subs


def useRange():
    range_entry['state'] = 'normal'
    range_entry.focus()



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




def ok():
    global subs
    subs = getSubs()
    try:
        root.destroy()
    except:
        return


def cancel():
    exit()


def close():
    return



# gui(0)