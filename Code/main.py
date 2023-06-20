import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import model_week1 as w1
import model_week2 as w2
import subprocess
import show_datesheet as d
date = d.DateSheet()

class Examination:
        
    def main(self):

        root = Tk()
        self.windows = root
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # set the relative width and height of the window
        width = int(600)
        height = int(200)
        x = int(screen_width/3)
        y = int(screen_height/3.5)
        root.geometry(f"{width}x{height}+{x}+{y}")
        
    
        root.config(bg = 'linen')
      
        root.title("Examination Scheduler")

        tk.Label(root, bg='linen',text="Examination Scheduling", fg="red", font=(None, 20)).place(x=150, y=40)
    

        
        def week_1():
            w1.main()
            date.main()

        def week_2():
            w2.main()
            date.main()

        
        
        Button(root,highlightbackground = 'linen', text="Week 1",command = week_1,height=2, width= 17).place(x=125, y=110)
        Button(root,highlightbackground = 'linen', text="Week 2",command = week_2,height=2, width= 17).place(x=360, y=110)
        

        
        
        root.mainloop()  


a = Examination()
a.main()