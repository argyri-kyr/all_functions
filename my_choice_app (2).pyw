
from ttkthemes import ThemedTk
import tkinter as tk
import matplotlib.pyplot as plt
 
 

from loaduncutgazeszoom_2023 import main3
from loaduncutgazeszoom_hardcases_2023 import main1
from semiauto_or_auto_process.autoloaduncutgazeszoom import main2

  

def choice1():
    window.destroy()
    main1()    

def choice2():
    window.destroy()
    main2()    
    
def choice3():
    window.destroy()
    main3()    
    
#radiobutton

def app_main():
    global window, rbtn1, rbtn2, rbtn3, radiobuttonsstate, selected_radiobutton_value1

    # Create window Tkinter
    window = ThemedTk(theme='clam')
    window.configure(bg='darkslategrey')
    
    # Name our Tkinter application title
    window.title(" Choice App ")
    
    # Define window size in Tkinter python
    w = 720 # width for the Tk root
    h = 500 # height for the Tk root

    # # get screen width and height
    ws = 1920    # ws = root.winfo_screenwidth() # width of the screen
    hs = 1080    # hs = root.winfo_screenheight() # height of the screen


    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2) - 40

    # set the dimensions of the screen 
    # and where it is placed
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    window.iconbitmap(r'C:\VScode\launch.json\all_functions\my_icon.ico')  
    
    img= tk.PhotoImage(file='./icon4.png', master= window)
    # Show image using label 
    label1 = tk.Label( window, image = img) 
    label1.place(x = 0, y = 0) 

    
    # Create a label widget in Tkinter
    label = tk.Label(window, foreground='white', bg='#111111', text="Click the function you want to run", font=('Garamond 17'), pady = 20)
    label.pack(pady=20)
    
    radiobuttonsstate = []
    # Create 1st button to update the label widget
    selected_radiobutton_value1 = tk.IntVar()
    rbtn1 = tk.Radiobutton(window, foreground='white', bg='#111111', activebackground='powderblue', text="loaduncutgazeszoom_hardcases_2023", variable=selected_radiobutton_value1, font=('Garamond 15'), pady = 2, command=choice1)
    rbtn1.pack(pady=20)
    radiobuttonsstate.append(selected_radiobutton_value1)

    # Create 2nd button to update the label widget
    selected_radiobutton_value = tk.IntVar()
    rbtn2 = tk.Radiobutton(window, foreground='white', bg='#111111', activebackground='powderblue', text="autoloaduncutgazeszoom", variable=selected_radiobutton_value, font=('Garamond 15'), pady = 2, command=choice2)
    rbtn2.pack(pady=20)
    radiobuttonsstate.append(selected_radiobutton_value)

    # Create 3d button to update the label widget
    selected_radiobutton_value = tk.IntVar()
    rbtn3 = tk.Radiobutton(window, foreground='white', bg='#111111', activebackground='powderblue', text="loaduncutgazeszoom_2023", variable=selected_radiobutton_value, font=('Garamond 15'), pady = 2, command=choice3)
    rbtn3.pack(pady=20)
    radiobuttonsstate.append(selected_radiobutton_value)
    
    
    # selected_radiobutton_value = selected_radiobutton_value.get()
    # print(selected_radiobutton_value)
    
    window.mainloop()


app_main()

