import os
import csv
import numpy as np
import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import filedialog
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import config

class Application:
    def __init__(self):
        self.root = None
        self.header = None
        self.data = None
        self.fig_canvas = None

    def start(self):
        self.call_root_window()
        self.call_csv_reader_widget()
        self.call_graphview_widget()
        self.root.mainloop()

    def call_root_window(self):
        self.root = tk.Tk()
        self.root.geometry('600x500')
        self.root.title('OBD Log Graph')

    def call_csv_reader_widget(self):
        frame = tk.Frame(self.root, relief="ridge", bd=1)
        frame.pack(fill=tk.BOTH, padx=5, pady=5)
        tk.Label(frame, text='Reference file >>').pack(side=tk.LEFT)
        entry_field = tk.Entry(frame)
        entry_field.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        tk.Button(frame, text='Select', command=lambda: self.set_path(entry_field)).pack(side=tk.LEFT)
        tk.Button(frame, text='Read',
                  command=lambda: self.read_csv(entry_field.get(),
                                                )).pack(side=tk.LEFT)

    def call_graphview_widget(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        fig = Figure()
        self.ax = fig.add_subplot(1, 1, 1)
        self.fig_canvas = FigureCanvasTkAgg(fig, frame)
        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, frame)
        self.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def call_pulldown_widget(self):
        self.selectData = StringVar()
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        cb = ttk.Combobox(frame, values=self.header, textvariable=self.selectData, state="readonly")
        cb.set(self.header[0])
        cb.bind('<<ComboboxSelected>>', self.show_graph)
        cb.pack()
        self.root.geometry('650x600')

    def set_path(self, entry_field):
        entry_field.delete(0, tk.END)
        abs_path = os.path.abspath(os.path.dirname(__file__))
        file_path = filedialog.askopenfilename(initialdir=abs_path)
        entry_field.insert(tk.END, str(file_path))

    def read_csv(self, path):
        extension = os.path.splitext(path)[1]
        if extension == '.csv':
            with open(path) as f:
                reader = csv.reader(f)
                self.header = [row for row in reader][0]
            self.data = np.genfromtxt(path, delimiter=',', skip_header=2, skip_footer=1)
            self.call_pulldown_widget()
            self.show_graph()
        else:
            messagebox.showwarning('warning', 'Please select a csv file.')

    def show_graph(self, event=None):
        self.ax.clear()
        x = np.linspace(0, len(self.data), len(self.data))
        y = self.data[:,self.header.index(self.selectData.get())]
        self.ax.plot(x, y)
        self.ax.set_xlim(0, len(self.data))
        self.ax.set_xlabel("Time [s]")
        self.ax.set_ylabel(f"{self.selectData.get()} [{config.UNITs[self.selectData.get()]}]")
        self.fig_canvas.draw()

if __name__ == '__main__':
    viewer = Application()
    viewer.start()