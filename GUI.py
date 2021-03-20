# CIS 41B Final Project: GUI.py
import matplotlib
matplotlib.use('TkAgg')
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
# import tkinter.messagebox as tkmb


class MainWindow(tk.Tk):
    def __init__(self):
        """ Constructor: Set up a main window """
        super().__init__()
        self.title("Rolling Stone Charts")
        rank100_tpl = ("Top 100 Songs", ("Default", "Weeks On Chart", "Sale Units"))
        rank200_tpl = ("Top 200 Albums", ("Default", "Weeks On Chart", "Sale Units",
                                          "Song Sales", "Song Streams"))
        rank500_tpl = ("Top 500 Artists", ("Default", "Weeks on Chart",
                                           "Album Sales", "Song Streams"))
        tk.Label(self, text="\nSelect a chart to begin:\n",
                 font=(None, 18), width=19).grid(row=0, column=0)
        b1 = tk.Button(self, text=rank100_tpl[0], width=15,
                       command=lambda: FilterWindow(self, rank100_tpl))
        b2 = tk.Button(self, text=rank200_tpl[0], width=15,
                       command=lambda: FilterWindow(self, rank200_tpl))
        b3 = tk.Button(self, text=rank500_tpl[0], width=15,
                       command=lambda: FilterWindow(self, rank500_tpl))
        b1.grid(row=1, column=0)
        b2.grid(row=2, column=0)
        b3.grid(row=3, column=0)
        tk.Label(self).grid(row=4, column=0)
        self.protocol("WM_DELETE_WINDOW", self.end_program)

    def end_program(self):
        """ End the program after closing the connection to a database """
        # self.conn.close()
        self.quit()


class FilterWindow(tk.Toplevel):
    def __init__(self, master, rank_tpl):
        """ Constructor: Set up a filter window """
        super().__init__(master)
        self.choice = ""
        self.title(rank_tpl[0])
        l = tk.Label(self, text="\nSort By:", font=(None, 18), width=19)
        l.grid(row=0, column=0, columnspan=3)
        self.control_var = tk.StringVar()
        for i in range(5):
            try:
                tk.Radiobutton(self, text=rank_tpl[1][i], variable=self.control_var,
                               value=rank_tpl[1][i]).grid(row=i+1, column=1, sticky='w')
            except IndexError:
                tk.Label(self).grid(row=i+1, column=0)
        self.control_var.set(rank_tpl[1][0])
        b = tk.Button(self, text="OK", command=self.set_choice)
        b.grid(row=6, column=0, columnspan=3)
        tk.Label(self).grid(row=7, column=0)
        self.grab_set()
        self.focus_set()
        self.transient(master)

    def set_choice(self):
        """ Store the user input and destroy the filter window """
        self.choice = self.control_var.get()
        self.destroy()

    def get_choice(self):
        """ Return the user input """
        return self.choice


app = MainWindow()
app.mainloop()
