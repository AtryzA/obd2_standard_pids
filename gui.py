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
        self.root.attributes('-fullscreen', False)
        self.text = []
        self.label = []
        self.label_pos = config.VALID_PIDs_LEN
        self.plot = []
        self.canvas = []
        self.canvas_pos = 0
        self.x, self.y = [], [[] for _ in range(config.GRAPH_VISIBLE_LEN)]
        self.y_max = {}
        self.xlim = [0, 60]

        for index in range(config.GRAPH_VISIBLE_LEN):
            self.plot.append(plt.figure(figsize=(5,2)))
            self.canvas.append(FigureCanvasTkAgg(self.plot[index], self.root))
            self.canvas[index].get_tk_widget().grid(column=0, row=index)

        for index in range(config.VALID_PIDs_LEN):
            self.text.append(tk.StringVar())
            self.text[index].set("Not Working")
            if index in config.GRAPH_VISIBLE.values():
                self.label.append(tk.Label(self.root, textvariable=self.text[index]).grid(column=1, row=self.canvas_pos))
                self.canvas_pos += 1
            else:
                self.label.append(tk.Label(self.root, textvariable=self.text[index]).grid(sticky = tk.N+tk.S, row=self.label_pos))
                self.label_pos -= 1

    def update(self, values):
        for index, (pname, _) in enumerate(config.GRAPH_VISIBLE.items()):
            offset = len(self.y[index])
            self.y_max[pname] = max(self.y[index][-(60 if offset > 60 else offset):])
        for index, (pname, unit) in enumerate(config.UNITs.items()):
            self.text[index].set(f'{pname} : {values[index]} {unit}')
        print(self.y_max)
        self.root.after(1000, self.update, values)

    def pltupdate(self, values):
        plt.cla()
        self.x.append(len(self.y[0]))
        if len(self.x) > 60:
            self.xlim[0] += 1
            self.xlim[1] += 1
        for index, (_, data_index) in enumerate(config.GRAPH_VISIBLE.items()):
            self.y[index].append(values[data_index])
            plot = self.plot[index].add_subplot(111)
            plot.set_xlim(self.xlim[0], self.xlim[1])
            plot.plot(self.x, self.y[index])
            self.canvas[index].draw()
        self.root.after(1000, self.pltupdate, values)

    def start(self, values):
        self.pltupdate(values)
        self.update(values)
        self.root.mainloop()