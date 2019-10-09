import tkinter as tk
from tkinter import *


class Gui:

    def start_gui(self, result_string):

        root = tk.Tk()
        T = tk.Text(root, height=45, width=80)
        T.pack()
        T.insert(tk.END, result_string)
        tk.mainloop()


def start_gui(result_string):
    root = tk.Tk()
    T = tk.Text(root, height=45, width=80)
    T.pack()
    T.insert(tk.END, result_string)
    tk.mainloop()
