import Tkinter


class ip_port:
    def __init__(self,tt):
        self.window =Tkinter.Tk()
        self.window.title("Minecraft-CS")
        self.window.geometry("400x400")      

        self.labelIp = Tkinter.Label(self.window, text = "IP_ADDR")
        self.inputIp = Tkinter.Entry(self.window)
        self.labelPort = Tkinter.Label(self.window, text = "PORT")
        self.inputPort = Tkinter.Entry(self.window)
        self.labelName = Tkinter.Label(self.window, text = "YOUR NAME")
        self.inputName = Tkinter.Entry(self.window)
        self.button = Tkinter.Button(self.window, text = "GO" ,command = self.exit_)      
        self.tt = tt
        self.labelIp.pack()
        self.inputIp.pack()
        self.labelPort.pack()
        self.inputPort.pack()
        self.labelName.pack()
        self.inputName.pack()
        self.button.pack()
        self.window.mainloop()

    def exit_(self):
        self.tt.value =self.inputIp.get(), int(self.inputPort.get()), self.inputName.get()
        self.window.destroy()
