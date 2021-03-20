# CIS 41B Final Project: GUI.py
import matplotlib
matplotlib.use('TkAgg')
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
# import tkinter.messagebox as tkmb
import sqlite3


class MainWindow(tk.Tk):
    def __init__(self):
        """ Constructor: Set up a main window """
        super().__init__()
        self.choice = 0  # Initialize choice here to use in other methods.
        self.conn = sqlite3.connect("rollingstones.db")
        self.cur = self.conn.cursor()
        self.title("Rolling Stone Charts")
        self.cur.execute("PRAGMA TABLE_INFO(Names)")
        self.name_cols = [elem[1] for elem in self.cur.fetchall()]
        self.cur.execute("PRAGMA TABLE_INFO(AlbumsDB)")
        self.album_cols = [elem[1] for elem in self.cur.fetchall()]
        self.cur.execute("PRAGMA TABLE_INFO(SongsDB)")
        self.song_cols = [elem[1] for elem in self.cur.fetchall()]
        self.cur.execute("PRAGMA TABLE_INFO(ArtistsDB)")
        self.artist_cols = [elem[1] for elem in self.cur.fetchall()]
        rank100_tpl = ("Top 100 Songs", ("Default", "Weeks On Chart", "Sale Units"))
        rank200_tpl = ("Top 200 Albums", ("Default", "Weeks On Chart", "Sale Units",
                                          "Song Sales", "Song Streams"))
        rank500_tpl = ("Top 500 Artists", ("Default", "Weeks on Chart", "Album Sales"))
        tk.Label(self, text="\nSelect a chart to begin:\n",
                 font=(None, 18), width=19).grid(row=0, column=0)
        b1 = tk.Button(self, text=rank100_tpl[0], width=15,
                       command=lambda: self.show_results(rank100_tpl))
        b2 = tk.Button(self, text=rank200_tpl[0], width=15,
                       command=lambda: self.show_results(rank200_tpl))
        b3 = tk.Button(self, text=rank500_tpl[0], width=15,
                       command=lambda: self.show_results(rank500_tpl))
        b1.grid(row=1, column=0)
        b2.grid(row=2, column=0)
        b3.grid(row=3, column=0)
        tk.Label(self).grid(row=4, column=0)
        self.protocol("WM_DELETE_WINDOW", self.end_program)

    def end_program(self):
        """ End the program after closing the connection to a database """
        self.conn.close()
        self.quit()

    def open_filter_window(self, rank_tpl):
        """ Open a filter window and get the user input """
        fw = FilterWindow(self, rank_tpl)
        self.wait_window(fw)
        return fw.get_choice()

    def show_results(self, rank_tpl):
        """ Open a list box or bar chart window
            by an appropriate SQL command for the user input """
        self.choice = self.open_filter_window(rank_tpl)
        if rank_tpl[0] == "Top 200 Albums":
            '''
            if self.choice == 0:
            elif self.choice == 1:
            elif self.choice == 2:
            elif self.choice == 3:
            else:
            '''
        else:
            if rank_tpl[0] == "Top 100 Songs":
                '''
                if self.choice == 0:
                elif self.choice == 1:
                else:
                '''
            else:
                field1 = self.artist_cols[0]
                if self.choice == 0:
                    field2 = self.artist_cols[1]
                    self.cur.execute('''SELECT ArtistsDB.%s, ArtistsDB.%s 
                                        FROM ArtistsDB ORDER BY %s DESC'''
                                     % (field1, field2, field2))
                elif self.choice == 1:
                    '''
                    '''
                else:
                    '''
                    '''
            if self.choice == 0:
                ListBoxWindow(self, rank_tpl[0], self.cur.fetchall())
            else:
                '''
                '''


class FilterWindow(tk.Toplevel):
    def __init__(self, master, rank_tpl):
        """ Constructor: Set up a filter window """
        super().__init__(master)
        self.title(rank_tpl[0])
        self.choice_num = 0  # Initialize choice_num here to use in other methods.
        tk.Label(self, text="\nSort By:",
                 font=(None, 18), width=19).grid(row=0, column=0, columnspan=3)
        self.control_var = tk.IntVar()
        for i in range(len(rank_tpl[1])):
            tk.Radiobutton(self, text=rank_tpl[1][i], variable=self.control_var,
                           value=i).grid(row=i+1, column=1, sticky='w')
        self.control_var.set(0)
        b = tk.Button(self, text="OK", command=self.set_choice)
        b.grid(row=6, column=0, columnspan=3)
        tk.Label(self).grid(row=7, column=0)
        self.grab_set()
        self.focus_set()
        self.transient(master)

    def set_choice(self):
        """ Store the user input and destroy the filter window """
        self.choice_num = self.control_var.get()
        self.destroy()

    def get_choice(self):
        """ Return the user input """
        return self.choice_num


class ListBoxWindow(tk.Toplevel):
    def __init__(self, master, title, data):
        """ Constructor: Set up a list box window """
        super().__init__(master)
        self.data = data
        self.title(title)
        tk.Label(self).grid(row=0, column=0)
        s = tk.Scrollbar(self)
        self.lb = tk.Listbox(self, height=10, width=45, yscrollcommand=s.set)
        for rank, one_data in enumerate(data, 1):
            self.lb.insert(tk.END, "%3d. %s: %d" % (rank, one_data[0], one_data[1]))
        s.config(command=self.lb.yview)
        self.lb.grid(row=1, column=0)
        s.grid(row=1, column=1, sticky='ns')
        tk.Label(self).grid(row=2, column=0)


class BarChartWindow(tk.Toplevel):
    def __init__(self, master):
        """ Constructor: Set up a bar chart window """
        super().__init__(master)
        fig = plt.figure()
        # plotting
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()


app = MainWindow()
app.mainloop()
