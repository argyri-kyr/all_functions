

from asyncio.windows_events import NULL
import tkinter as tk

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


import tkinter as tk
from tkinter import messagebox as mb
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import *
import matplotlib.pyplot as plt
import wave


from storeAudioROIS import storeAudioROIS_v2
from saveAudioNotes import saveAudioNotes
from checkValidNotesAudio import checkValidNotes
from decodingErrors import decodingErrors



def audio_window(root, audiowav):
    global total_length, play_btn, pause_btn, previous_btn, next_btn, back_btn, forw_btn, back10_btn, forw10_btn, slider_label, my_slider, nextsub_btn, close_btn, text_box    
    # audiomp3 = audiowav[:-3] + 'mp3'
    # sound = pydub.AudioSegment.from_wav(audiowav)
    # sound.export(audiomp3, format="mp3")
    # pygame.mixer.init()
    # pygame.mixer.music.load(audiomp3)
    # audio = MP3(audiomp3)
    # total_length = audio.info.length

    pygame.mixer.init()
    pygame.mixer.music.load(audiowav)
    pygame.mixer.music.rewind()
    
    with wave.open(audiowav) as mywav:
        total_length = mywav.getnframes() / mywav.getframerate()
    total_mins, total_secs = divmod(total_length, 60)
    # print("total_length = ", total_length)

    # # # # FIRST row buttons # # # #
    play_btn = tk.Button(root, text="Play", width=10, background='#D7F0F9', command=play)
    play_btn.grid(row=1, column=0, padx=(60,15))

    pause_btn = tk.Button(root, text="Pause", width=10, background='#D7F0F9', command=pause)
    pause_btn.grid(row=1, column=1, padx=15)

    previous_btn = tk.Button(root, text="Previous_Page", width=15, background='#D7F0F9', command=previous_page)
    previous_btn.grid(row=1, column=2, padx=15)

    next_btn = tk.Button(root, text="Next_Page", width=15, background='#D7F0F9', command=next_page)
    next_btn.grid(row=1, column=3, padx=(15,50))
    
    
    # # # # SECOND row buttons # # # #
    back_btn = tk.Button(root, text="Back 1s", width=10, background='#D7F0F9', command=backwards)
    back_btn.grid(row=2, column=0, padx=(60,15))
    root.bind("<KeyPress-Left>", lambda event: backwards())

    forw_btn = tk.Button(root, text="Forw 1s", width=10, background='#D7F0F9', command=forwards)
    forw_btn.grid(row=2, column=1, padx=15)
    root.bind("<KeyPress-Right>", lambda event: forwards())

    back10_btn = tk.Button(root, text="Back 10s", width=10, background='#D7F0F9', command=backwards10)
    back10_btn.grid(row=2, column=2, padx=1)

    forw10_btn = tk.Button(root, text="Forw 10s", width=10, background='#D7F0F9', command=forwards10)
    forw10_btn.grid(row=2, column=3, padx=(15,50))


    # # # # THIRD row buttons # # # #
    # create temporary slider label
    slider_label = Label(root, text="1", background='#D7F0F9')
    slider_label.grid(row=3, column=1, columnspan=2)
    
    
    # # # # FORTH row buttons # # # #
    # Create style for Scale object
    style = ttk.Style()
    style.configure("TScale", background='#D7F0F9')

    # create music position slide
    my_slider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, value=1, command=slide, length=360, style="TScale")
    my_slider.grid( row=4, column=0, columnspan=4)


    # # # # FIFTH row buttons # # # #
    nextsub_btn = tk.Button(root, text="Next Sub", width=15, background='#D7F0F9', command=nextsub)
    nextsub_btn.grid(row=5, column=0 ,padx=(50,10))

    close_btn = tk.Button(root, text="Close All", width=15, background='#D7F0F9', command=terminate)
    close_btn.grid(row=5, column=3, padx=(10,40))
    
    
    # # # # # #  Text Box  # # # # # # #  
    text_box = tk.Text(root, width=65, height=22, font=("Arial", 10))
    text_box.grid(row=0, column=4, rowspan = 7, pady=10)
    filtextbox()
    

def tick():
    global current_time

    if not is_paused:
            
        # mins, secs = divmod(current_time, 60)
        # label.config(text=f"{mins:02.0f}:{secs:06.3f}")


        # current_time = int(pygame.mixer.music.get_pos()/1000)
        
        # print("int(my_slider.get()) = ", int(my_slider.get()))
        # print("int(current_time) = ", int(current_time))
        ########################    Update slider position value to current song position...  ##########################
        if( int(my_slider.get()) == int(total_length) ):
            pass
        
        # # # slider hasn't been moved
        elif( int(my_slider.get()) == int(current_time) ):
            # Update slider and set total_length and current_time
            slider_position = int(total_length)
            my_slider.config(to=slider_position, value=int(current_time))
            current_time = int(pygame.mixer.music.get_pos()/1000)+1
            # print("current_time mpika2 = ", current_time)
        
        # # # slider HAS been moved
        else:
            # Update slider and set total_length and current_time
            slider_position = int(total_length)
            my_slider.config(to=slider_position, value=int(my_slider.get()))
            current_time = int(my_slider.get())
            
            # Move this thing along by one second
            next_time = int(my_slider.get()) + 1
            my_slider.config(value=next_time)
                    
        # update slider_label
        slider_label.config(text=f' {int(my_slider.get())}  of  {int(total_length)}')
    
    back_btn.config(state="disabled" if is_paused else "normal")
    forw_btn.config(state='disabled' if is_paused else "normal")
    back10_btn.config(state='disabled' if is_paused else "normal")
    forw10_btn.config(state='disabled' if is_paused else "normal")
        
    my_slider.after(1000, tick)



def audio_main(audiopath, previous_page_ref, next_page_ref, getParam_ref):
    global root, is_paused, current_time, previous_page, next_page, getParamAudiomain
    
    is_paused = False
    current_time = 1
    previous_page = previous_page_ref
    next_page = next_page_ref
    
    getParamAudiomain = getParam_ref
    
    root = ThemedTk(theme='adapta')
    root.configure(bg='#FCDBD9')
    w = 1200 # width for the Tk root
    h = 380 # height for the Tk root
    
    # # get screen width and height
    ws = 1920    # ws = root.winfo_screenwidth() # width of the screen
    hs = 1080    # hs = root.winfo_screenheight() # height of the screen


    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2) + 260
    

    # set the dimensions of the screen 
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.configure()

    audio_window(root, audiopath)
    
    tick()
    
    return


def play():
    global is_paused
    pygame.mixer.music.play()
    is_paused = False
    pause_btn.config(text="Pause")
    my_slider.config(value=1)
    slider_label.config(text=f' {int(1)}  of  {int(total_length)}')
     

def pause():
    global is_paused, current_time
    is_paused = not is_paused
    if is_paused:
        pygame.mixer.music.pause()
        pause_btn.config(text="Resume")
    else:
        pygame.mixer.music.unpause()
        pause_btn.config(text="Pause")


def backwards():
    global is_paused, current_time
    if not is_paused:
        current_time = int(my_slider.get())
        delta = min(current_time, 2)
        '''
        pygame.mixer.music.rewind()
        pygame.mixer.music.set_pos(current_time-delta)
        '''
        pygame.mixer.music.play(start=current_time-delta)

        my_slider.config(value=current_time-delta)
        slider_label.config(text=f' {int(current_time-delta)}  of  {int(total_length)}')


def forwards():
    global is_paused, current_time
    if not is_paused:
        current_time = int(my_slider.get())
        delta = min(total_length-current_time, 1)
        '''
        pygame.mixer.music.rewind()
        pygame.mixer.music.set_pos(current_time+delta)
        '''
        pygame.mixer.music.play(start=current_time+delta)
    
        my_slider.config(value=current_time+delta)
        slider_label.config(text=f' {int(current_time+delta)}  of  {int(total_length)}')
        


def backwards10():
    global is_paused, current_time
    if not is_paused:
        current_time = int(my_slider.get())
        delta = min(current_time, 10)
        '''
        pygame.mixer.music.rewind()
        pygame.mixer.music.set_pos(current_time-delta)
        '''
        pygame.mixer.music.play(start=current_time-delta)
     
        my_slider.config(value=current_time-delta)
        slider_label.config(text=f' {int(current_time-delta)}  of  {int(total_length)}')


def forwards10():
    global is_paused, current_time
    if not is_paused:
        current_time = int(my_slider.get())
        delta = min(total_length-current_time, 10)
        '''
        pygame.mixer.music.rewind()
        pygame.mixer.music.set_pos(current_time+delta)
        '''
        pygame.mixer.music.play(start=current_time+delta)
                
        my_slider.config(value=current_time+delta)
        slider_label.config(text=f' {int(current_time+delta)}  of  {int(total_length)}')


def nextsub():
    # at first check for wrong notes
    wrongNotes, data1, data2, data3 = checkValidNotes(getParamAudiomain("text"), getParamAudioUI)
    if(wrongNotes):
        return

    # check for doubles or new checked entry
    # getParamAudiomain("eventdataTofinaldata")(getParamAudiomain("pageno"))
    
    # save finalROISselected.txt
        # # this saving was in version1, clicked ROIS
        # for pno in range(getParamAudiomain("totalpages")):
        #     storeAudioROIS_v1(getParamAudiomain("text"), pno+1, getParamAudiomain("groiselectedpath"),  getParamAudiomain("finalselectedrois")[pno][0],  getParamAudiomain("finalselectedrois")[pno][1])
    storeAudioROIS_v2(getParamAudiomain("groiselectedpath"), data1, data2)
    
    # save My_Audio_Notes.txt
    end_index = text_box.index("end linestart")
    mynotes = text_box.get("1.0", end_index)
    saveAudioNotes(mynotes, getParamAudiomain("gnotespath"))
    emptynotes = ['\n' , '', NULL]
    checknewlineonly = list(set(mynotes))

    # connect selected ROIS with their words and save the file
    decodingErrors(getParamAudiomain("text"), getParamAudiomain("gwordsselectedpath"), data1, data2, data3)

    if(mynotes in emptynotes or checknewlineonly==['\n']): 
        checkisloud = checkisLoud()
        if( checkisloud=="no" ):
            if os.path.exists(getParamAudiomain("gnotespath")): 
                os.remove(getParamAudiomain("gnotespath"))
            if os.path.exists(getParamAudiomain("gwordsselectedpath")): 
                os.remove(getParamAudiomain("gwordsselectedpath"))
            if os.path.exists(getParamAudiomain("groiselectedpath")): 
                os.remove(getParamAudiomain("groiselectedpath"))
    
    plt.close('all')
    pygame.mixer.music.stop()
    root.destroy()

    return 


def terminate():
    # at first check for wrong notes
    wrongNotes, data1, data2, data3 = checkValidNotes(getParamAudiomain("text"), getParamAudioUI)
    if(wrongNotes):
        return
    
    # check for doubles or new checked entry
    # getParamAudiomain("eventdataTofinaldata")(getParamAudiomain("pageno"))   
        
    # save finalROISselected.txt
        # # this saving was in version1, clicked ROIS
        # for pno in range(getParamAudiomain("totalpages")):
        #     storeAudioROIS_v1(getParamAudiomain("text"), pno+1, getParamAudiomain("groiselectedpath"),  getParamAudiomain("finalselectedrois")[pno][0],  getParamAudiomain("finalselectedrois")[pno][1])
    storeAudioROIS_v2(getParamAudiomain("groiselectedpath"), data1, data2)
    
    # save My_Audio_Notes.txt
    end_index = text_box.index("end linestart")
    mynotes = text_box.get("1.0", end_index)
    saveAudioNotes(mynotes, getParamAudiomain("gnotespath"))
    emptynotes = ['\n' , '', NULL]
    checknewlineonly = list(set(mynotes))
    
    # connect selected ROIS with their words and save the file
    decodingErrors(getParamAudiomain("text"), getParamAudiomain("gwordsselectedpath"), data1, data2, data3)

    if(mynotes in emptynotes or checknewlineonly==['\n']):
        checkisloud = checkisLoud()
        if( checkisloud=="no" ):
            if os.path.exists(getParamAudiomain("gnotespath")): 
                os.remove(getParamAudiomain("gnotespath"))
            if os.path.exists(getParamAudiomain("gwordsselectedpath")): 
                os.remove(getParamAudiomain("gwordsselectedpath"))
            if os.path.exists(getParamAudiomain("groiselectedpath")): 
                os.remove(getParamAudiomain("groiselectedpath"))


    plt.close()
    root.destroy()
    exit()



def slide(x):
    global is_paused
    
    # start fix: this fix is because slider start from 0 and i was 1 second off because my audio start from 1, so this fix is about the cases that i want to start over, then slider dont start from 0 instead start from 1
    myfixedstart = int(my_slider.get())
    if( myfixedstart == 0):
        myfixedstart = 1
    pygame.mixer.music.play(loops=0, start=myfixedstart)
    # end fix
    
    is_paused = False
    pause_btn.config(text="Pause")


def getParamAudioUI(param):
    d = {"root":root, "pause_btn":pause_btn, "my_slider":my_slider, "slider_label":slider_label, "total_length":total_length, "text_box":text_box}
    return d[param]


def filtextbox():
    path_to_file = getParamAudiomain("gnotespath")
    if  os.path.exists(path_to_file):
        try:
            with open(path_to_file, encoding="utf8") as f:
                contents = f.read()
        except:
            try:
                with open(path_to_file) as f:
                    contents = f.read()  
            except:
                pass
        
        text_box.insert(tk.END, contents)





# def checkisLoud():
#     res=mb.askquestion('Confirm Next', 'Is this a loud text?')
    
#     # root.destroy()
#     return res

def checkisLoud():
    def on_response(answer):
        response.set(answer)
        dialog.destroy()  # Close the dialog when a response is given
        check_frame.destroy() # Close the check_frame when a response is given
    
    check_frame = tk.Tk()
    check_frame.withdraw()
    dialog = tk.Toplevel()
    dialog.title("Confirm Loud")
    
    # Center the dialog on the screen
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    window_width = 350  # Dialog width
    window_height = 150  # Dialog height
    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)
    
    # Set the position of the dialog/frame in the screen
    dialog.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

    # Confirmation question
    tk.Label(dialog, text="Is this a loud text?", font=("Arial", 15)).pack(pady=10)

    # Set focus and bring to front
    dialog.lift()  # Bring to front
    dialog.focus_force()  # Force focus
    
    # Add Yes and No buttons with customized size
    yes_button = tk.Button(dialog, text="Yes", command=lambda: on_response("yes"), width=10, height=2)
    no_button = tk.Button(dialog, text="No", command=lambda: on_response("no"), width=10, height=2)
    
    yes_button.pack(side="left", padx=(60,0), pady=20)
    no_button.pack(side="right", padx=(0,60), pady=20)

    # Response Handler
    response = tk.StringVar()
    response.set(None)  # Default value (not selected)
    dialog.wait_window()  # Wait until a response is given
    
    return  response.get()

