# CIS 41B Final Project: GUI.py - Kaede Hamada
import matplotlib
matplotlib.use('TkAgg')
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter.messagebox as tkmb
from backendQuery import Album, Song, Artist


class MainWindow(tk.Tk):
    def __init__(self):
        """ Constructor: Set up a main window """
        super().__init__()
        self.choice_num = None  # Initialize choice_num here to use in other methods.
        self.choice_index = None  # Initialize choice_index here to use in other methods.
        self.title("Rolling Stone Charts")
        self.albums = Album()
        self.songs = Song()
        self.artists = Artist()
        rank100_tpl = ("Top 100 Songs", ("Default", "Weeks On Chart", "Song Units"))
        rank200_tpl = ("Top 200 Albums", ("Default", "Weeks On Chart", "Album Sales",
                                          "Song Sales", "Song Streams"))
        rank500_tpl = ("Top 500 Artists", ("Default", "Weeks on Chart", "Song Streams"))
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
        self.albums.close_conn()
        self.songs.close_conn()
        self.artists.close_conn()
        self.quit()

    def open_filter_window(self, rank_tpl):
        """ Open a filter window and get the user input """
        fw = FilterWindow(self, rank_tpl)
        self.wait_window(fw)
        return fw.get_choice()

    def open_choice_lb_window(self, chart, field, data):
        """ Open a choice list box window and get the user input """
        clbw = ChoiceLBWindow(self, chart, field, data)
        self.wait_window(clbw)
        return clbw.get_choice()

    def show_results(self, rank_tpl):
        """ Open a list box or bar chart window
            by an appropriate SQL command for the user input """
        self.choice_num = self.open_filter_window(rank_tpl)
        if self.choice_num:
            # For the choices whose results will be displayed as list boxes
            if (rank_tpl[0] == "Top 200 Albums") \
                    or (rank_tpl[0] != "Top 200 Albums" and self.choice_num == 1):
                data_list = list()
                if rank_tpl[0] == "Top 200 Albums":
                    if self.choice_num == 1:
                        title = "The Top 200 Albums Ranked by Album Units"
                        data_list = self.albums.albumsDefault()
                    elif self.choice_num == 2:
                        labels = self.albums.labelsInAlbums()
                        self.choice_index \
                            = self.open_choice_lb_window(rank_tpl[0], "Record Labels", labels)
                        if self.choice_index and len(self.choice_index) > 0:
                            title = "The Top Album from Selected Record Labels by Weeks on Chart"
                            for index in self.choice_index:
                                data_list.append(self.albums.topAlbumOfLabel(labels[index]))
                        else:  # NO task if the user doesn't choose anything
                            return
                    elif self.choice_num == 3:
                        title = "The Top 200 Albums Ranked by Album Sales"
                        data_list = self.albums.albumsSales()
                    elif self.choice_num == 4:
                        title = "The Top 200 Albums Ranked by Song Sales"
                        data_list = self.albums.albumSongSales()
                    else:  # self.choice_num == 5
                        title = "The Top 200 Albums Ranked by Song Streams"
                        data_list = self.albums.albumsSongStreams()
                else:  # rank_tpl[0] != "Top 200 Albums" and self.choice_num > 1
                    if rank_tpl[0] == "Top 100 Songs":
                        title = "Top 100 Songs Ranked by Song Units"
                        data_list = self.songs.songsDefault()
                    else:  # rank_tpl[0] == "Top 500 Artists"
                        title = "Top 500 Artists Ranked by Song Streams"
                        data_list = self.artists.artistsDefault()
                ResultLBWindow(self, rank_tpl[0], title, data_list)
            else:  # For the choices whose results will be displayed as bar charts
                if rank_tpl[0] == "Top 100 Songs":
                    field = "Songs"
                    data_list = self.songs.allSongs()
                else:  # rank_tpl[0] == "Top 500 Artists"
                    field = "Artists"
                    data_list = self.artists.allArtists()
                self.choice_index = self.open_choice_lb_window(rank_tpl[0], field, data_list)
                if self.choice_index and len(self.choice_index) > 0:
                    x_list = list()
                    y_list = list()
                    error_list = list()
                    if rank_tpl[0] == "Top 100 Songs":
                        x_axes = "Songs"
                        if self.choice_num == 2:
                            y_axes = "Weeks on Chart"
                            data_function = self.songs.weeksOfSong
                        else:  # self.choice_num == 3
                            y_axes = "Song Units"
                            data_function = self.songs.unitsOfSong
                    else:  # rank_tpl[0] == "Top 500 Artists"
                        x_axes = "Artists"
                        if self.choice_num == 2:
                            y_axes = "Weeks on Chart"
                            data_function = self.artists.weeksOfArtist
                        else:  # self.choice_num == 3
                            y_axes = "Song Streams"
                            data_function = self.artists.songStreamsOfArtist
                    for index in self.choice_index:
                        data = data_function(data_list[index])
                        if data:
                            y_list.append(data)
                            x_list.append(data_list[index])
                        else:
                            error_list.append(data_list[index])
                    if len(error_list) > 0:
                        tkmb.showinfo("No Data", "No data: " + ','.join(error_list), parent=self)
                    if len(y_list) > 0:
                        ResultBCWindow(self, rank_tpl[0], x_list, y_list, x_axes, y_axes)


class FilterWindow(tk.Toplevel):
    def __init__(self, master, rank_tpl):
        """ Constructor: Set up a filter window """
        super().__init__(master)
        self.title(rank_tpl[0])
        self.choice = None  # Initialize choice_num here to use in other methods.
        tk.Label(self, text="\nSort By:",
                 font=(None, 18), width=19).grid(row=0, column=0, columnspan=3)
        self.control_var = tk.IntVar()
        for i in range(len(rank_tpl[1])):
            tk.Radiobutton(self, text=rank_tpl[1][i], variable=self.control_var,
                           value=i+1).grid(row=i+1, column=1, sticky='w')
        self.control_var.set(1)
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


class ChoiceLBWindow(tk.Toplevel):
    def __init__(self, master, chart, field, data):
        """ Constructor: Set up a list box window """
        super().__init__(master)
        self.master = master
        self.choice = None
        self.title(chart)
        tk.Label(self, text="\nChoose " + field,
                 font=(None, 18), width=19).grid(row=0, column=0, columnspan=2)
        s = tk.Scrollbar(self)
        self.lb = tk.Listbox(self, height=10,  width=35,
                             selectmode="multiple", yscrollcommand=s.set)
        self.lb.insert(tk.END, *data)
        s.config(command=self.lb.yview)
        self.lb.grid(row=1, column=0)
        s.grid(row=1, column=1, sticky="ns")
        tk.Button(self, text="OK", command=self.set_choice).grid(row=2, column=0)
        self.grab_set()
        self.focus_set()
        self.transient(master)

    def set_choice(self):
        self.choice = self.lb.curselection()
        self.destroy()

    def get_choice(self):
        return self.choice


class ResultLBWindow(tk.Toplevel):
    def __init__(self, master, chart, title, data):
        """ Constructor: Set up a list box result window """
        super().__init__(master)
        self.data = data
        self.title(chart)
        tk.Label(self, text='\n'+title, font=(None, 18)).grid(row=0, column=0)
        s = tk.Scrollbar(self)
        self.lb = tk.Listbox(self, height=10, width=86, yscrollcommand=s.set)
        if len(data[0]) == 4:
            for one_data in data:
                self.lb.insert(tk.END, "%s: %s - %s (%d)"
                               % (one_data[0], one_data[1], one_data[2], one_data[3]))
        elif len(data[0]) == 3:
            for rank, one_data in enumerate(data, 1):
                self.lb.insert(tk.END, "%3d. %s - %s: %d"
                               % (rank, one_data[0], one_data[1], one_data[2]))
        else:
            for rank, one_data in enumerate(data, 1):
                self.lb.insert(tk.END, "%3d. %s: %d" % (rank, one_data[0], one_data[1]))
        s.config(command=self.lb.yview)
        self.lb.grid(row=1, column=0)
        s.grid(row=1, column=1, sticky='ns')
        tk.Label(self).grid(row=2, column=0)


class ResultBCWindow(tk.Toplevel):
    def __init__(self, master, chart, x_data, y_data, x_label, y_label):
        """ Constructor: Set up a bar chart result window """
        super().__init__(master)
        self.title(chart)
        fig = plt.figure()
        plt.title(x_label + " and Their " + y_label)
        plt.bar(range(len(x_data)), y_data, align="center")
        plt.xticks(range(len(x_data)), x_data, rotation=90)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()


class RecordInfoWindow(tk.Toplevel):
    def __init__(self, master, data):
        """ Constructor: Set up a bar chart result window """
        super().__init__(master)
        self.title("Info")


app = MainWindow()
app.mainloop()
