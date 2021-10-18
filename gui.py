import sys
import tkinter as tk

class gui:
    def __init__(self) -> None:
        self.root = None
        try:
            self.setup()
        except:
            sys.exit()
        self.label_parts('ENGINE')
        self.label_parts('RPM')
        self.label_parts('SPEED')
        self.label_parts('km/h')
        self.label_parts('SPEED')
        self.label_parts('RPM')

    def setup(self):
        self.root = tk.Tk()
        self.root.title(u'OBD2')
        self.root.geometry('400x300')


    def label_parts(self, text):
        tk.Label(text=text).pack()

    def start(self):
        self.root.mainloop()