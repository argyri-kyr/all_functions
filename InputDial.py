import tkinter as tk
from tkinter import ttk
from tkinter import *

class Dialogue(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Input  Dialogue")
        self.geometry('800x800')
        self.Sub_Info()
        self.Txt_Info()
        self.Options_Info()
        self.inputDialog=[]        
        

    def Close(self):
            self.destroy()  


    def Sub_Info(self):
        label1 =tk.Label(self)
        label1.pack(fill=X, padx=10, pady=10)

        lname = tk.Label(label1,
                    font=("Times New Roman", 15),
                    text="Name:")  #name 'label'

        self.name_var = tk.StringVar()
        
        tname = tk.Entry(label1,  
                    textvariable = self.name_var, 
                    bg = "white")   #name 'text'

        


        lid = tk.Label(label1,
                    font=("Times New Roman", 15),
                    text=" Id:")  #id 'label'

        self.id_var = tk.StringVar()

        tid = tk.Entry(label1, 
                    textvariable = self.id_var)   #id 'text'

        lname.grid(row = 0, column = 0, sticky = NW, padx = 50, pady = 10)
        tname.grid(row = 0, column = 1, pady = 10, sticky= N)
        lid.grid(row = 1, column = 0, sticky = NW, padx = 50)
        tid.grid(row = 1, column = 1, sticky= N, pady = 10)
    

    def Take_input(self):
        name = self.name_var.get()
        self.inputDialog.append(name) 
        id = self.id_var.get()
        self.inputDialog.append(id) 

        self.name_var.set("")
        self.id_var.set("")
        #print(*self.inputDialog)

    
    def getState(self,buttons):
        for b in buttons:
            return b.get()
    


    def Txt_Info(self):
        label2 = tk.Label(self)
        label2.pack(fill=X, padx=10, pady=10)

        label2_1 = tk.Label(label2, font=("Times New Roman", 15), text = "Texts:")
        label2_1.grid(row = 3, column = 0, sticky = NW, padx = 50, pady = 10)

        
        label2_2 = tk.Label(label2)
        label2_2.grid(row = 4, column = 0, padx = 50, pady = 10)

        self.txts = ['zoo',  'island',  'Η πεταλούδα', 'Τα παιχνίδια', 'Μια φορά και έναν καιρό', 'Olympia' , 'Ζουγκλα' , 'Time for Limits' , 'visit' , 'Jungle' , 'School' , 'Animals']
        self.GrNum = 7  #Number of Greek Texts

        self.checkedtext=[]
        for i in range( len(self.txts) ):
            self.checkedtext.append(tk.IntVar(self))

        self.Checkbuttons=[]
        for i in range( len(self.txts)//2 +1 ):
            self.Checkbuttons.append( ttk.Checkbutton(label2_2, 
                                     text = self.txts[i], 
                                     variable = self.checkedtext[i],
                                     onvalue = 1,
                                     offvalue = 0).grid(row = 5+ i , column = 0, sticky = W )
                                    )    
        for i in range( len(self.txts)//2 +1 , len(self.txts)  ):
            self.Checkbuttons.append( ttk.Checkbutton(label2_2, 
                                     text = self.txts[i], 
                                     variable = self.checkedtext[i],
                                     onvalue = 1,
                                     offvalue = 0).grid(row = 5+ i-len(self.txts)//2 , column = 0, padx =300, sticky = W)
                                    )    


    def Check(self,states,position,button,checkbuttons):
        if states[position].get() == 1:
            for i in range( len(self.txts) ):
                if( i!=position and i<len(states) ):
                    states[i].set(0)
                if(position == 0): # if pressed button is: Check_All
                    self.checkedtext[i].set(1)
                elif(position == 1): # if pressed button is: UnCheck_All
                    self.checkedtext[i].set(0)

    def CheckGr(self,states,position,button,checkbuttons) :
        if states[position].get() == 1:
            for i in range( len(self.txts) ):
                if( i!=position and i<len(states) ):
                    states[i].set(0)

                if(i<self.GrNum):
                    self.checkedtext[i].set(1)
                else:
                    self.checkedtext[i].set(0)
        


    def Options_Info(self):
        srow= 5 + len(self.txts)//2  #start row

        label3 = tk.Label(self)
        label3.pack(fill=X, padx=10, pady=10)

        labelinfo = tk.Label(label3, text = "Options:", font=("Times New Roman", 15),padx = 50,pady = 10)
        labelinfo.grid(row = srow, column = 0, sticky = NW)

        textContainer= tk.Label(label3)
        textContainer.grid(row = srow+1 ,sticky = NW)

        var =[]

        var1 = tk.IntVar(self)
        var.append(var1)
        button_All = ttk.Checkbutton(textContainer,
                                text="Check All",
                                variable=var1,
                                onvalue = 1,
                                offvalue = 0,
                                command= lambda :self.Check(var, 0, button_All, self.checkedtext) ).pack(side=LEFT, padx = 50)
        
        
        var2 = tk.IntVar(self)
        var.append(var2)
        button_None = ttk.Checkbutton(textContainer,
                                text="UnCheck All",
                                variable=var2,
                                onvalue = 1,
                                offvalue = 0,
                                command= lambda :self.Check(var, 1, button_None, self.checkedtext) ).pack(side=LEFT, padx = 10)
        
        var3 = tk.IntVar(self)
        var.append(var3)        
        button_Gr = ttk.Checkbutton(textContainer,
                                text="Check Greek",
                                variable=var3,
                                onvalue = 1,
                                offvalue = 0,
                                command= lambda :self.CheckGr(var, 2, button_Gr, self.checkedtext) ).pack(side=LEFT, padx = 10)

        OK2 = Button(label3,
                    text ="OK",
                    command = lambda:[self.Take_input(), self.getState(self.checkedtext), self.Close()])   #OK button    
        
        OK2.grid(row = srow+2, column=0, padx=50 , pady=20, sticky = NW)


    def get_text(self):
        l=[]
        for i in range(len(self.txts)):
            if(self.checkedtext[i].get() == 1):
                l.append(self.txts[i])
        return l

    
