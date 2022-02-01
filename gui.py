# below to test_module #######

# import multiprocessing
# import random
##############################
import sys
import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config

class gui:
    def __init__(self) -> None:
        self.root = None
        try:
            self.setup()
        except Exception as e:
            self.cleanup()

    def setup(self):
        self.call_root_window()
        self.call_tabpage_widget()
        self.call_onepage_widget()
        self.call_specpage_widget()
        self.x, self.y = [], [[] for _ in range(config.GRAPH_VISIBLE_LEN)]
        self.y_max = {}
        self.xlim = [0, 60]

    def cleanup(self):
        try:
            del self
        except Exception as e:
            print(e)

    def call_root_window(self):
        self.root = tk.Tk()
        self.root.title(u'OBD2')
        self.root.attributes('-fullscreen', False)

    def call_tabpage_widget(self):
        nb = ttk.Notebook(self.root)
        self.tabs = []
        for pname in config.GRAPH_VISIBLE.keys():
            tab = tk.Frame(nb)
            self.tabs.append(tab)
            nb.add(tab, text=f"{pname}", padding=3)
        spec_tab = tk.Frame(nb)
        self.tabs.append(spec_tab)
        nb.add(spec_tab, text="ALL_Params", padding=3)
        nb.bind("<<NotebookTabChanged>>", self.pltupdate)
        nb.pack(expand=1, fill="both", pady=10)

    def call_onepage_widget(self):
        fig = Figure()
        self.ax = fig.add_subplot(1, 1, 1)
        self.canvas = []
        self.text = []
        for index in range(config.GRAPH_VISIBLE_LEN):
            fig_canvas = FigureCanvasTkAgg(fig, self.tabs[index])
            param_text = tk.StringVar()
            param_text.set("Not Working!!!")
            self.text.append(param_text)
            tk.Label(self.tabs[index], textvariable=self.text[index]).pack()
            fig_canvas.get_tk_widget().pack()
            self.canvas.append(fig_canvas)

    def call_specpage_widget(self):
        self.spectext = []
        for index in range(config.VALID_PIDs_LEN):
            param_text = tk.StringVar()
            param_text.set("Not Working!!!")
            self.spectext.append(param_text)
            tk.Label(self.tabs[-1], textvariable=self.spectext[index]).pack()

    def dataupdate(self, values):
        for index, (_, data_index) in enumerate(config.GRAPH_VISIBLE.items()):
            self.y[index].append(values[data_index])
        self.x.append(len(self.y[0]))
        if len(self.x) > 60:
            self.xlim[0] += 1
            self.xlim[1] += 1
        self.root.after(1000, self.dataupdate, values)

    def textupdate(self, values):
        for index, (pname, _) in enumerate(config.GRAPH_VISIBLE.items()):
            offset = len(self.y[index])
            self.y_max[pname] = max(self.y[index][-(60 if offset > 60 else offset):])
            self.text[index].set(f'Maximum Per Minute : {self.y_max[pname]:.2f} {config.UNITs[pname]}')
        for index, (pname, unit) in enumerate(config.UNITs.items()):
            self.spectext[index].set(f'{pname} : {values[index]:.2f} {unit}')
        self.root.after(1000, self.textupdate, values)

    def pltupdate(self, event=None):
        self.ax.clear()
        if event != None:
            nb = event.widget
            index = nb.index("current")
            text = nb.tab(nb.select(), "text")
            if text == "ALL_Params":
                pass
            else:
                self.ax.set_xlim(self.xlim[0], self.xlim[1])
                self.ax.set_xlabel("Time [s]")
                self.ax.set_ylabel(f"{text} [{config.UNITs[text]}]")
                self.ax.plot(self.x, self.y[index])
                self.canvas[index].draw()
        self.root.after(1000, self.pltupdate, event)

    def start(self, values):
        self.dataupdate(values)
        self.pltupdate()
        self.textupdate(values)
        self.root.mainloop()

# below to test_code ########

#     def test_process1(self, values):
#         while True:
#             for index in range(7):
#                 values[index] = random.random() / (index + 1)

# values = multiprocessing.Array('d', range(7))
# ui = gui()
# p1 = multiprocessing.Process(target=ui.start, args=[values])
# p2 = multiprocessing.Process(target=ui.test_process1, args=[values])
# p2.start()
# p1.start()
##############################