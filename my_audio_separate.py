import time
import tkinter as tk
from mutagen.mp3 import MP3
import pydub

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

def play():
    global stime, is_paused
    pygame.mixer.music.play()
    stime = time.time()
    is_paused = False
    pause_btn.config(text="Pause")


def backwards():
    global stime, is_paused, elapsed
    if stime and not is_paused:
        elapsed = time.time() - stime
        delta = min(elapsed, 5)
        '''
        pygame.mixer.music.rewind()
        pygame.mixer.music.set_pos(elapsed-delta)
        '''
        pygame.mixer.music.play(start=elapsed-delta)
        stime += delta


def forwards():
    global stime, is_paused, elapsed
    if stime and not is_paused:
        elapsed = time.time() - stime
        delta = min(total_length-elapsed, 5)
        '''
        pygame.mixer.music.rewind()
        pygame.mixer.music.set_pos(elapsed+delta)
        '''
        pygame.mixer.music.play(start=elapsed+delta)
        stime -= delta
        print("stime = ", stime)
        

def pause():
    global is_paused, stime, elapsed
    is_paused = not is_paused
    now = time.time()
    if is_paused:
        elapsed = now - stime  # save the elapsed time
        pygame.mixer.music.pause()
        pause_btn.config(text="Resume")
    else:
        pygame.mixer.music.unpause()
        pause_btn.config(text="Pause")
        stime = now - elapsed # adjust the start time


def previous_page():
    global pageno
    pageno+=1
    print("pageno = ", pageno)
    return

def next_page():
    return


def eco_window(root, audiowav):
    global total_length, play_btn, back_btn, forw_btn, pause_btn, label, previous_btn, next_btn
    
    audiomp3 = "C:/Users/Admin/Music/AudioRecording.mp3"
    sound = pydub.AudioSegment.from_wav(audiowav)
    sound.export(audiomp3, format="mp3")

    audiomp3 = "C:/Users/Admin/Music/AudioRecording.mp3"

    pygame.mixer.init()
    pygame.mixer.music.load(audiomp3)

    audio = MP3(audiomp3)
    total_length = audio.info.length
    # print("total_length = ", total_length)

    play_btn = tk.Button(root, text="Play", width=10, background='orange', command=play)
    play_btn.grid(row=1, column=0, padx=(30,10), pady=20)

    back_btn = tk.Button(root, text="Back 5s", width=10, background='orange', command=backwards)
    back_btn.grid(row=1, column=1, padx=10, pady=2)

    forw_btn = tk.Button(root, text="Forw 5s", width=10, background='orange', command=forwards)
    forw_btn.grid(row=1, column=2, padx=10, pady=2)

    pause_btn = tk.Button(root, text="Pause", width=10, background='orange', command=pause)
    pause_btn.grid(row=1, column=3, padx=(10,30))

    label = tk.Label(root, font="Consolas 12", background='orange')
    label.grid(row=2, column=1, columnspan=2, pady = 5)

    previous_btn = tk.Button(root, text="Previous_Page", width=15, background='orange', command=previous_page)
    previous_btn.grid(row=2, column=0, padx=(30, 10))

    next_btn = tk.Button(root, text="Next_Page", width=15, background='orange', command=next_page)
    next_btn.grid(row=2, column=3, padx=(10,30))



def tick():
    global stime, elapsed
    if not is_paused:
        if not pygame.mixer.music.get_busy():
            stime = None
        elapsed = time.time()-stime if stime else 0
        mins, secs = divmod(elapsed, 60)
        label.config(text=f" {mins:02.0f}:{secs:06.3f}" + "  /  " + str(round(total_length, 4)) + " ")
    back_btn.config(state="disabled" if is_paused else "normal")
    forw_btn.config(state="disabled" if is_paused else "normal")
    label.after(100, tick)

pageno=0
def main():
    global stime, is_paused, elapsed, pageno
    stime = None
    is_paused = False
    elapsed = 0
    pageno=1
    
    audiowav = "C:/Users/Admin/Music/AudioRecording.wav"
    
    root = tk.Tk()
    w = 620 # width for the Tk root
    h = 150 # height for the Tk root

    # # get screen width and height
    ws = 1920    # ws = root.winfo_screenwidth() # width of the screen
    hs = 1080    # hs = root.winfo_screenheight() # height of the screen


    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2) - 50

    # set the dimensions of the screen 
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.configure(bg='darkblue')

    eco_window(root, audiowav)
    
    tick()
    root.mainloop()

main()