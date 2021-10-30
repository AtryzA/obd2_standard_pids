import sys
import tkinter as tk
import config

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt

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
        self.plot = []
        self.canvas = []
        self.x, self.y = [], [[] for _ in range(config.VALID_LEN)]
        self.xlim = [0, 60]

        for index in range(config.VALID_LEN):
            self.text.append(tk.StringVar())
            self.text[index].set("Not Working")
            self.plot.append(plt.figure(figsize=(5,2)))
            self.canvas.append(FigureCanvasTkAgg(self.plot[index], self.root))
            self.canvas[index].get_tk_widget().grid(column=0, row=index)
            self.label.append(tk.Label(self.root, textvariable=self.text[index]).grid(column=1, row=index))

    def update(self, values):
        for index, (pname, unit) in enumerate(config.UNITs.items()):
            self.text[index].set(f'{pname} : {values[index]} {unit}')
        self.root.after(1000, self.update, values)

    def pltupdate(self, values):
        plt.cla()
        self.x.append(values[-1])
        if len(self.x) > 60 or self.x[-1] > self.xlim[1]:
            self.xlim[0] += 1
            self.xlim[1] += 1
        for index, (_, limit) in enumerate(config.UNITs_LIMIT.items()):
            self.y[index].append(values[index])
            plot = self.plot[index].add_subplot(111)
            plot.set_ylim(0, limit)
            plot.set_xlim(self.xlim[0], self.xlim[1])
            plot.plot(self.x, self.y[index])
            self.canvas[index].draw()
        self.root.after(1000, self.pltupdate, values)

    def start(self, values):
        self.pltupdate(values)
        self.update(values)
        self.root.mainloop()