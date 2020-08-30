import sys
# if int(sys.version[0]) == 2:
#     import tkinter as Tkinter
# elif int(sys.version[0]) == 3:
#     import Tkinter
import tkinter as tk

class result:

    def __init__(self,mes):
        self.window =tk.Tk()
        self.window.title("Result")
        self.window.geometry("200x50")
        self.label = tk.Label(self.window, text = mes)
        self.label.pack()
        self.window.mainloop()
