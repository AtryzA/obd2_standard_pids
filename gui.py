import sys
import tkinter as tk
import config

class gui:
    def __init__(self) -> None:
        self.root = None
        try:
            self.setup()
        except:
            sys.exit()

    def setup(self):
        self.root = tk.Tk()
        self.root.title(u'OBD2')
        self.root.attributes('-fullscreen', True)
        self.text = []
        self.label = []
        for index in range(config.VALID_LEN):
            self.text.append(tk.StringVar())
            self.text[index].set("Not Working")
            self.label.append(tk.Label(self.root, textvariable=self.text[index]).pack())

    def update(self, values):
        for index, (pname, unit) in enumerate(config.UNITs.items()):
            self.text[index].set(f'{pname} : {values[index]} {unit}')
        self.root.after(1000, self.update, values)

    def start(self, values):
        self.update(values)
        self.root.mainloop()