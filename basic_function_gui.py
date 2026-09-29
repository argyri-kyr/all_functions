

from asyncio.windows_events import NULL
from tkinter import *
from PIL import Image,  ImageTk
import time


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from globalVars import eyeradarlogo_path


def basic_function_gui(checkedflag):
    global greektexts, uktexts, ustexts, extratexts
    greektexts = ['visit', 'zoo', 'island', 'olympia', 'efeyreseis', 'psaras', 'zebra', 'morning', 'visitloud', 'eilikrinia', 'doro', 'treno', 'RAN', 'grkisla', 'grkislaloud', 'grkislaext', 'grkislaextloud', 'decoderealwords2v', 'decodepseudowords2v', 'decodesentences3v', 'phonolrhymes2v', 'rantwopart1', 'rantwopart2', 'raven2v', 'visualortho3v', 'visualrecogn3v']
    uktexts = ['sunny', 'midfred','armyjet', 'midfredloud', 'enemypie', 'horse', 'jockey', 'gasmask']
    ustexts = ['sunnyus', 'midfredus','armyjetus', 'midfredloudus', 'enemypieus', 'horseus', 'jockeyus', 'gasmaskus']
    extratexts = ['raven', "testattention", "testlekseona", "testlekseonb"]

    global root
    root = Tk(className=' eyeRadar  DYSLEXIA')

    w = 1530 # width for the Tk root
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
    number_entry.grid(row=0, column=3, padx=(35,30), pady=(30,15), ipady=20, sticky=W)
    number_entry.focus_force()
    number_label = Label(frame1, text="Enter subject's number ", font=('Arial', 15), background='#FDBD67')
    number_label.grid(row=0, column=0, padx=(0,30), pady=(30,15))

    
    # range id space
    global range_entry
    range_entry = Entry(frame1, width=30, justify='center', font=('Arial', 15))
    range_entry.config(state='disabled')
    range_entry.grid(row=1, column=3, padx=(35,30), pady=(5,10), ipady=20)
    range_button = Button(frame1, text="Use Range", width=20, height=3, justify='left', bg='#ffebcc', font=('Arial', 15), command=useRange)
    range_button.grid(row=1, column=0, padx=(0,30), pady=(5,10))

    # label text space
    text_label = Label(frame1, text=" ....::: Texts :::.... ", font=('Arial', 19), background='#FDBD67')
    text_label.grid(row=2, column=1, pady=(25,25))  #padx=(430,5)

    # # FRAME 2 # #

    frame2 = Frame(root, background='#FDBD67')

    # by_pass fix & hard_cases Choices & left_eye & right_eye Choices
    global firstchoicesstate
    firstchoicesstate = []
    checkvar = IntVar()
    bypasscheckbox = Checkbutton(frame2, text="bypass fix", font=('Arial', 14), variable=checkvar, onvalue=1, offvalue=0, background='#FDBD67')
    bypasscheckbox.grid(row=0, column=0, padx = 0, pady=(0,25), sticky=W)
    firstchoicesstate.append(checkvar)

    checkvar = IntVar()
    hardcasescheckbox = Checkbutton(frame2, text="hard cases", font=('Arial', 14), variable=checkvar, onvalue=1, offvalue=0, background='#FDBD67')
    hardcasescheckbox.grid(row=0, column=1, padx=90, pady=(0,25), sticky=W)
    firstchoicesstate.append(checkvar)

    checkvar = IntVar()
    lefteyecheckbox = Checkbutton(frame2, text="only left eye", font=('Arial', 14), variable=checkvar, onvalue=1, offvalue=0, background='#FDBD67')
    lefteyecheckbox.grid(row=0, column=2, padx=40, pady=(0,25), sticky=W)
    firstchoicesstate.append(checkvar)

    checkvar = IntVar()
    righteyecheckbox = Checkbutton(frame2, text="only right eye", font=('Arial', 14), variable=checkvar, onvalue=1, offvalue=0, background='#FDBD67')
    righteyecheckbox.grid(row=0, column=3, padx=40, pady=(0,25), sticky=W)
    firstchoicesstate.append(checkvar)
    # print(firstchoicesstate[0].get(),firstchoicesstate[1].get() )
    
    # Fix appear number of texts per row
    fixed_texts_per_row = 7

    # greek texts space
    greekrows = 0
    global greekcheckbuttonsstate
    greekcheckbuttonsstate = []
    for i in range(len(greektexts)):
        if(i%fixed_texts_per_row==0):
            padding_left=0
        elif(i%fixed_texts_per_row==1):
            padding_left=40
        else:
            padding_left=10

        checkvar = IntVar()
        textcheckbox = Checkbutton(frame2, text=greektexts[i], font=('Arial', 14), variable=checkvar, onvalue=1, offvalue=0, background='#FDBD67')
        textcheckbox.grid(row=int(i/fixed_texts_per_row) + 1, column=i%fixed_texts_per_row, padx=padding_left, pady=5, sticky=W)
        greekcheckbuttonsstate.append(checkvar)
        
        # if( checkedflag==1 ):
        #     greekcheckbuttonsstate[-1].set(1)  # set default button's state as  -- Checked --
        
        # if( checkedflag==2 and greektexts[i]=="visitloud" ):
        #     greekcheckbuttonsstate[-1].set(1)
        
        # elif( checkedflag==2 and greektexts[i]=="grkislaloud" ):
        #     greekcheckbuttonsstate[-1].set(1)
        
        # elif( checkedflag==2 and greektexts[i]=="grkislaextloud" ):
        #     greekcheckbuttonsstate[-1].set(1)
        
        
        if( checkedflag==2 and greektexts[i].endswith('loud') ):
            greekcheckbuttonsstate[-1].set(1)
            
        greekrows = int(i/5) + 1
   
    # greekcheckbuttonsstate[-1].set(0)   # Uncheck RAN text



    # uk texts space
    ukrows = 0
    global ukcheckbuttonsstate
    ukcheckbuttonsstate = []
    for i in range(len(uktexts)):
        if(i%5==0):
            padding_left=0
        elif(i%5==1):
            padding_left=40
        else:
            padding_left=10

        checkvar = IntVar()
        textcheckbox = Checkbutton(frame2, text=uktexts[i], font=('Arial', 14), variable=checkvar, onvalue=1, offvalue=0, background='#FDBD67')
        textcheckbox.grid(row=greekrows+1+int(i/5), column=i%5, padx=padding_left, pady=5, sticky=W)
        ukcheckbuttonsstate.append(checkvar)
        
        # if( checkedflag==1 ):
        #     ukcheckbuttonsstate[-1].set(1)  # set default button's state as  -- Checked --    
        
        # if( checkedflag==2 and uktexts[i]=="midfredloud" ):
        #     ukcheckbuttonsstate[3].set(1)
                                                                               
        if( checkedflag==2 and uktexts[i].endswith('loud') ):
            ukcheckbuttonsstate[-1].set(1)
        
        ukrows = greekrows+1+int(i/5)



    # us texts space
    usrows = 0
    global uscheckbuttonsstate
    uscheckbuttonsstate = []
    for i in range(len(ustexts)):
        if(i%5==0):
            padding_left=0
        elif(i%5==1):
            padding_left=40
        else:
            padding_left=10

        checkvar = IntVar()
        textcheckbox = Checkbutton(frame2, text=ustexts[i], font=('Arial', 14), variable=checkvar, onvalue=1, offvalue=0, background='#FDBD67')
        textcheckbox.grid(row=ukrows+1+int(i/5), column=i%5, padx=padding_left, pady=5, sticky=W)
        uscheckbuttonsstate.append(checkvar)
        
        # uscheckbuttonsstate[-1].set(1)  # set default button's state as  -- Checked -- 
                                                                                       
        if( checkedflag==2 and ustexts[i].endswith('loudus') ):
            uscheckbuttonsstate[-1].set(1)
            
        usrows = ukrows+1+int(i/5)
        
    # extra texts
    extrarows = 0
    global extracheckbuttonsstate
    extracheckbuttonsstate = []
    for i in range(len(extratexts)):
        if(i%5==0):
            padding_left=0
        elif(i%5==1):
            padding_left=40
        else:
            padding_left=10

        checkvar = IntVar()
        textcheckbox = Checkbutton(frame2, text=extratexts[i], font=('Arial', 14), variable=checkvar, onvalue=1, offvalue=0, background='#FDBD67')
        textcheckbox.grid(row=usrows+1+int(i/5), column=i%5, padx=padding_left, pady=5, sticky=W)
        extracheckbuttonsstate.append(checkvar)
        
        # extracheckbuttonsstate[-1].set(1)  # set default button's state as  -- Checked --                                                                                

        extrarows = usrows+1+int(i/5)


    # #  FRAME 3  # #

    frame3 = Frame(root, pady=30, background='#FDBD67')
    uncheckall_button = Button(frame3, text="Uncheck all", width=15, height=3, bg='#ffebcc', font=('Arial', 15), command=uncheckall)
    uncheckall_button.grid(row=0, column=0, padx=(25,40), pady=(0,10))

    checkgr_button = Button(frame3, text="Check GR", width=15, height=3, bg='#ffebcc', font=('Arial', 15), command=checkgr)
    checkgr_button.grid(row=0, column=1, padx=(15,40), pady=(0,10))

    checkuk_button = Button(frame3, text="Check UK", width=15, height=3, bg='#ffebcc', font=('Arial', 15), command=checkuk)
    checkuk_button.grid(row=0, column=2, padx=(15,40), pady=(0,10))

    checkus_button = Button(frame3, text="Check US", width=15, height=3, bg='#ffebcc', font=('Arial', 15), command=checkus)
    checkus_button.grid(row=0, column=3, padx=(15,40), pady=(0,10))    

    ok_button = Button(frame3, text="OK", width=25, height=3, bg='#ffebcc', font=('Arial', 15), command=ok)
    ok_button.grid(row=1, column=0, padx=(15,30), pady=(10,10), columnspan=2)   

    cancel_button = Button(frame3, text="Cancel", width=25, height=3, bg='#ffebcc', font=('Arial', 15), command=cancel)
    cancel_button.grid(row=1, column=2, padx=(15,30), pady=(10,10), columnspan=2)   

    image1 = Image.open(eyeradarlogo_path)  
    image2 =  ImageTk. PhotoImage(image1)
    image_label = Label(frame3 , image=image2, background='#FDBD67')
    image_label.grid(row=0, column=4, padx=(5,25), pady=(10,10), rowspan=2)  

        
    frame1.pack()
    frame2.pack()
    frame3.pack()
    
    # root.protocol("WM_DELETE_WINDOW", close)
    # root.state('zoomed')
    
    root.mainloop()

    # # return number_entry, range_entry, greekcheckbuttonsstate, ukcheckbuttonsstate, uscheckbuttonsstate, extracheckbuttonsstate
    # print("subs = ", subs)
    # print("texts = ", texts)

    return subs, texts, finalfirstchoices


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
    
    for i in range(len(extracheckbuttonsstate)):
        extracheckbuttonsstate[i].set(0)


def checkgr():
    for i in range(len(greekcheckbuttonsstate)):
        greekcheckbuttonsstate[i].set(1)


def checkuk():
    for i in range(len(ukcheckbuttonsstate)):
        ukcheckbuttonsstate[i].set(1)


def checkus():
    for i in range(len(uscheckbuttonsstate)):
        uscheckbuttonsstate[i].set(1)

def checkextra():
    for i in range(len(extracheckbuttonsstate)):
        extracheckbuttonsstate[i].set(1)
        

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

    for i in range(len(extracheckbuttonsstate)):
        if( extracheckbuttonsstate[i].get() ):
            texts.append(extratexts[i])
            

    return texts



def getFirstStates():
    firstchoices = []
    for i in range(len(firstchoicesstate)):
        firstchoices.append(firstchoicesstate[i].get())

    return firstchoices



def ok():
    global subs, texts, finalfirstchoices
    subs = getSubs()
    texts = getTexts()
    finalfirstchoices = getFirstStates()
    try:
        root.destroy()
    except:
        return


def cancel():
    exit()


def close():
    return



# gui(0)