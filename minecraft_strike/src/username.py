import sys
if int(sys.version[0]) == 2:
    import tkinter as Tkinter
elif int(sys.version[0]) == 3:
    import Tkinter

class ip_port:
    def __init__(self,tt):
        self.window =Tkinter.Tk()
        self.window.title("Minecraft-CS")
        self.window.geometry("400x400")
        self.name=0
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
        if int(self.inputPort.get()) == 0:
            self.tt.value = ("127.0.0.1",31425,self.name)
        self.window.destroy()
