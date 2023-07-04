import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *



class SeatingPlan:
    
    def __init__(self):
        pass 

    
    def main(self):

        root = Tk()
        self.windows = root
        # get the dimensions of the screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # set the relative width and height of the window
        width = int(0.9 * screen_width)
        height = int(0.9 * screen_height)
        x = int(0.05* screen_width)
        y = int(0* screen_height)
        root.geometry(f"{width}x{height}+{x}+{y}")

        
        root.config(bg = 'linen')
      
        root.title("Seating Plan")

        tk.Label(root, bg='linen',text="Seating Plan", fg="red", font=(None, 30)).place(x=int(screen_width)/2.5, y=70)
         

        
        scrollbar= ttk.Scrollbar(root, orient= 'vertical')
        scrollbar.pack(side= RIGHT, fill= BOTH)
   
                
        cols = ('Day', 'Date','Time','Student Name','Course ID','Room')
        self.listBox = ttk.Treeview(root,height=25, columns=cols, show='headings' )
              
            

        i = 0
        for col in cols:
            self.listBox.column("#{}".format(i),anchor=CENTER, stretch=NO, width=232)
            self.listBox.heading(col, text=col)
            self.listBox.place(x= 5, y=240)
            i = i + 1


        Button(root,highlightbackground = 'linen', text="Clear Data",command = self.clear ,height=2, width= 13).place(x=10, y=145)
        
        self.show_datesheet()
        root.mainloop()  

    def show_datesheet(self):
        # Open the text file and read its contents
        file = open("Code\schedule\SeatingPlan.txt", "r")
        lines = file.read()               
        words = lines.split('\n')
        new_lst = []
        for word in words:
            new = word.split(' ')    
            i = 0
            while i < len(new) - 1:
                if new[i] != "" and i < len(new) - 2 and new[i+1] != "" :
                    new[i] = new[i] + " " + new[i+1]
                    new.pop(i+1)
                    
                else:
                    i += 1
            final = [x for x in new if x != ""]
            new_lst.append(final)

        
        for i,lines in enumerate(new_lst):
            self.listBox.insert("", 'end', values= lines)
            
    def clear(self):
        self.listBox.delete(*self.listBox.get_children())
        

