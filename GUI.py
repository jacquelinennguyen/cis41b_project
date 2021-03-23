# CIS 41B Final Project: GUI.py - Kaede Hamada
import matplotlib

matplotlib.use('TkAgg')
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter.messagebox as tkmb
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta, FR
from PIL import ImageTk, Image
import urllib
import requests
import threading
import importlib
from backendWebScraper import scrape
from backendQuery import Song, Album, Artist
from backendDB import updateDB
from datetime import datetime
from weeks import getweeks
from tkinter import ttk

dayToday = date.today().strftime("%d")
lastFriday = datetime.now() + relativedelta(days=-1, weekday=FR(-2) if dayToday == "Fri" else FR(-1))
monthLetter = lastFriday.strftime("%b")
monthNumber = lastFriday.strftime("%m")
day = lastFriday.strftime("%d")
year = lastFriday.strftime("%Y")

# thread = threading.Thread(target=backendWebScraper.scrape, args=(year, monthLetter, monthNumber, day,))
# thread.start()
# thread.join()


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
        tk.Label(self, text="Select a chart to begin:",
                 font=(None, 18), width=19).grid(row=0, column=0, pady=5)
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
        self.focus_set()

        week_select_win = WeekSelectWindow(self)
        week_select_win.wait_window()
        self.week_chosen = tk.StringVar()
        self.week_chosen.set(week_select_win.get_week())
        self.focus_set()
        self.make_update_thread()

        self.protocol("WM_DELETE_WINDOW", self.end_program)

    def make_update_thread(self):
        chosen_week = self.week_chosen.get()
        elements = chosen_week.split(' ')
        _monthLetter = elements[0]
        _monthNumber = datetime.strptime(monthLetter, '%b').strftime("%m")
        _day = elements[1][:-1]
        _year = elements[2]
        update_thread = threading.Thread(target=scrape, args=(_year, _monthLetter, _monthNumber, _day,))
        update_thread.start()
        update_thread.join()

    def update(self, chosen_week):
        elements = chosen_week.split(' ')
        _monthLetter = elements[0]
        _monthNumber = datetime.strptime(monthLetter, '%b').strftime("%m")
        _day = elements[1][:-1]
        _year = elements[2]

        scrape(_year, _monthLetter, _monthNumber, _day)

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
                ResultLBWindow(self, rank_tpl[0], title, data_list, self.week_chosen)
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


class WeekSelectWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.wait_visibility()
        self.focus_set()
        self.grab_set()
        self.title("Select Week")
        n = tk.StringVar()
        self.d_weeks = getweeks()
        d_keys = list(self.d_weeks.keys())
        d_keys.reverse()
        # print(d_keys)
        self.week_chosen = tk.StringVar()
        self.weeks = ttk.Combobox(self, width=27, textvariable=n)
        self.weeks['values'] = tuple(d_keys)
        self.weeks.bind("<<ComboboxSelected>>")
        tk.Label(self, text="Choose a week to see charts for").grid(row=0, column=0)
        self.weeks.grid(column=0, row=5, pady=10)

        update_button = tk.Button(self, text="Ok", command=self.save_choice)
        update_button.grid(row=6, column=0)

    def save_choice(self):
        self.week_chosen.set(self.weeks.get())
        self.destroy()

    def get_week(self):
        return self.week_chosen.get()


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
                           value=i + 1).grid(row=i + 1, column=1, sticky='w')
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
        self.lb = tk.Listbox(self, height=10, width=35,
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
    def __init__(self, master, chart, title, data, week_chosen):
        """ Constructor: Set up a list box result window """
        super().__init__(master)
        self.focus_set()
        self.data = data
        self.title(chart)
        tk.Label(self, text='\n' + title, font=(None, 18)).grid(row=0, column=0)
        tk.Label(self, textvariable=week_chosen, font=(None, 14)).grid(row=1, column=0)
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

        # START OF TEST:
        elif len(data[0]) == 13:
            self.song_frame = tk.Frame(self)
            for rank, one_data in enumerate(data, 1):
                self.lb.insert(tk.END, "%3d. %s" % (rank, one_data[0]))
            self.song_name = tk.StringVar()
            self.artist_name = tk.StringVar()
            self.units_trend = list()
            self.label = tk.StringVar()
            self.peak_position = tk.IntVar()
            self.weeks_on_chart = tk.IntVar()
            self.top_cities = tk.StringVar()
            self.song_streams = tk.IntVar()

            song_name_lbl = tk.Label(self.song_frame, textvariable=self.song_name, font=('Helvetica', 24, 'bold'),
                                     relief="ridge")
            artist_name_lbl = tk.Label(self.song_frame, textvariable=self.artist_name, font=('Helvetica', 18, 'bold'),
                                       relief="ridge")
            label_lbl = tk.Label(self.song_frame, textvariable=self.label, font=('Helvetica', 14))
            peak_position_lbl = tk.Label(self.song_frame, textvariable=self.peak_position, font=('Helvetica', 14))
            weeks_on_chart_lbl = tk.Label(self.song_frame, textvariable=self.weeks_on_chart, font=('Helvetica', 14))
            top_cities_lbl = tk.Label(self.song_frame, textvariable=self.top_cities, font=('Helvetica', 14), anchor="w")
            song_streams_lbl = tk.Label(self.song_frame, textvariable=self.song_streams, font=('Helvetica', 14))

            song_name_lbl.grid(row=0, column=1, sticky="n")
            artist_name_lbl.grid(row=1, column=1)
            label_lbl.grid(row=2, column=0, sticky="w", columnspan=2)
            peak_position_lbl.grid(row=5, column=0, sticky="w", columnspan=2)
            weeks_on_chart_lbl.grid(row=6, column=0, sticky="w", columnspan=2)
            top_cities_lbl.grid(row=7, column=0, sticky="w", columnspan=2)
            song_streams_lbl.grid(row=8, column=0, sticky="w", columnspan=2)

            self.lb.bind("<<ListboxSelect>>", self.show_song_record)

        elif len(data[0]) == 15:  # grabbing all columns for showing the record.
            self.album_frame = tk.Frame(self)
            for rank, one_data in enumerate(data, 1):
                self.lb.insert(tk.END, "%3d. %s" % (rank, one_data[0]))
            self.album_name = tk.StringVar()
            self.artist_name = tk.StringVar()
            self.album_units = tk.IntVar()
            self.album_sales = tk.IntVar()
            self.song_sales = tk.IntVar()
            self.peak_position = tk.IntVar()
            self.weeks_on_chart = tk.IntVar()
            self.top_songs = tk.StringVar()
            self.song_streams = tk.IntVar()
            album_name_lbl = tk.Label(self.album_frame, textvariable=self.album_name, font=('Helvetica', 24, 'bold'),
                                      relief="ridge")
            artist_name_lbl = tk.Label(self.album_frame, textvariable=self.artist_name, font=('Helvetica', 18, 'bold'),
                                       relief="ridge")
            album_units_lbl = tk.Label(self.album_frame, textvariable=self.album_units, font=('Helvetica', 14))
            album_sales_lbl = tk.Label(self.album_frame, textvariable=self.album_sales, font=('Helvetica', 14))
            song_sales_lbl = tk.Label(self.album_frame, textvariable=self.song_sales, font=('Helvetica', 14))
            peak_position_lbl = tk.Label(self.album_frame, textvariable=self.peak_position, font=('Helvetica', 14))
            weeks_on_chart_lbl = tk.Label(self.album_frame, textvariable=self.weeks_on_chart, font=('Helvetica', 14))
            top_songs_lbl = tk.Label(self.album_frame, textvariable=self.top_songs, font=('Helvetica', 14), anchor="w")
            song_streams_lbl = tk.Label(self.album_frame, textvariable=self.song_streams, font=('Helvetica', 14))

            album_name_lbl.grid(row=0, column=1, sticky="n")
            artist_name_lbl.grid(row=1, column=1)
            album_units_lbl.grid(row=2, column=0, sticky="w", columnspan=2)
            album_sales_lbl.grid(row=3, column=0, sticky="w", columnspan=2)
            song_sales_lbl.grid(row=4, column=0, sticky="w", columnspan=2)
            peak_position_lbl.grid(row=5, column=0, sticky="w", columnspan=2)
            weeks_on_chart_lbl.grid(row=6, column=0, sticky="w", columnspan=2)
            top_songs_lbl.grid(row=7, column=0, sticky="w", columnspan=2)
            song_streams_lbl.grid(row=8, column=0, sticky="w", columnspan=2)

            self.lb.bind("<<ListboxSelect>>", self.show_album_record)

        elif len(data[0]) == 6:
            self.artist_frame = tk.Frame(self)
            for rank, one_data in enumerate(data, 1):
                self.lb.insert(tk.END, "%3d. %s" % (rank, one_data[0]))
            self.artist_name = tk.StringVar()
            self.song_streams = tk.IntVar()
            self.weeks_on_chart = tk.IntVar()
            self.top_song = tk.StringVar()
            self.peak_position = tk.IntVar()

            artist_name_lbl = tk.Label(self.artist_frame, textvariable=self.artist_name, font=('Helvetica', 18, 'bold'),
                                       relief="ridge")
            song_streams_lbl = tk.Label(self.artist_frame, textvariable=self.song_streams, font=('Helvetica', 14))
            weeks_on_chart_lbl = tk.Label(self.artist_frame, textvariable=self.weeks_on_chart, font=('Helvetica', 14))
            top_song_lbl = tk.Label(self.artist_frame, textvariable=self.top_song, font=('Helvetica', 14), anchor="w")
            peak_position_lbl = tk.Label(self.artist_frame, textvariable=self.peak_position, font=('Helvetica', 14))

            artist_name_lbl.grid(row=0, column=1, sticky="n")
            peak_position_lbl.grid(row=5, column=0, sticky="w", columnspan=2)
            weeks_on_chart_lbl.grid(row=6, column=0, sticky="w", columnspan=2)
            top_song_lbl.grid(row=7, column=0, sticky="w", columnspan=2)
            song_streams_lbl.grid(row=8, column=0, sticky="w", columnspan=2)

            self.lb.bind("<<ListboxSelect>>", self.show_artist_record)

        s.config(command=self.lb.yview)
        self.lb.grid(row=2, column=0)
        s.grid(row=2, column=1, sticky='ns')
        tk.Label(self).grid(row=2, column=0)

    def show_album_record(self, event):
        self.album_frame.grid()
        selection = self.lb.curselection()[0]

        # loads image from server
        img_url = self.data[selection][-5]
        image = Image.open(urllib.request.urlopen(img_url))
        image = image.resize((100, 100), Image.ANTIALIAS)
        width, height = image.size
        image = ImageTk.PhotoImage(image)
        panel = tk.Label(self.album_frame, image=image, relief="raised")
        panel.image = image
        panel.grid(row=0, column=0, sticky="n", rowspan=2)

        top_songs = self.data[selection][7].split(', ')
        if len(top_songs) != 3:
            top_songs = None

        # display metrics
        self.album_name.set(self.data[selection][0])
        self.artist_name.set(self.data[selection][-3])
        self.album_units.set("Album units: " + str(self.data[selection][2]))
        self.album_sales.set("Album sales: " + str(self.data[selection][3]))
        self.song_sales.set("Song sales: " + str(self.data[selection][4]))
        self.peak_position.set("Peak position: " + str(self.data[selection][5]))
        self.weeks_on_chart.set("Weeks on chart: " + str(self.data[selection][6]))
        if top_songs:
            self.top_songs.set("Top songs:\n" + top_songs[0] + "\n" + top_songs[1] + "\n" + top_songs[2])
        else:
            self.top_songs.set('')
        self.song_streams.set("Song streams: " + str(self.data[selection][9]))

    def show_song_record(self, event):
        self.song_frame.grid()
        selection = self.lb.curselection()[0]

        # loads image from server
        img_url = self.data[selection][-5]
        image = Image.open(urllib.request.urlopen(img_url))
        image = image.resize((100, 100), Image.ANTIALIAS)
        width, height = image.size
        image = ImageTk.PhotoImage(image)
        panel = tk.Label(self.song_frame, image=image, relief="raised")
        panel.image = image
        panel.grid(row=0, column=0, sticky="n", rowspan=2)

        top_cities = self.data[selection][5].split('\n')[:-1]
        if len(top_cities) != 3:
            top_cities = None

        # display metrics
        self.song_name.set(self.data[selection][0])
        self.artist_name.set(self.data[selection][-3])
        self.label.set("Label: " + str(self.data[selection][-1]))
        self.peak_position.set("Peak position: " + str(self.data[selection][3]))
        self.weeks_on_chart.set("Weeks on chart: " + str(self.data[selection][6]))
        if top_cities:
            self.top_cities.set("Top cities:\n" + top_cities[0] + "\n" + top_cities[1] + "\n" + top_cities[2])
        else:
            self.top_cities.set('')
        self.song_streams.set("Song streams: " + str(self.data[selection][7]))

    def show_artist_record(self, event):
        self.artist_frame.grid()
        selection = self.lb.curselection()[0]

        # loads image from server
        img_url = self.data[selection][-1]
        image = Image.open(urllib.request.urlopen(img_url))
        image = image.resize((100, 100), Image.ANTIALIAS)
        width, height = image.size
        image = ImageTk.PhotoImage(image)
        panel = tk.Label(self.artist_frame, image=image, relief="raised")
        panel.image = image
        panel.grid(row=0, column=0, sticky="n", rowspan=2)

        # display metrics
        self.artist_name.set(self.data[selection][0])
        self.song_streams.set("Song streams: " + str(self.data[selection][1]))
        self.weeks_on_chart.set("Weeks on chart: " + str(self.data[selection][2]))
        self.peak_position.set("Peak position: " + str(self.data[selection][4]))
        self.top_song.set("Top song: " + str(self.data[selection][3]))


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


app = MainWindow()
app.mainloop()
