
        tk.Button(self, text="Set Week", command=self.update).grid(column=1, row=5)

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