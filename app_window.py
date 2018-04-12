from tkinter import *
from tkinter import ttk

class AppWindow(Frame):
    def __init__(self):
        Frame.__init__(self)
        mainframe = ttk.Frame(self, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        active_time = StringVar()
        self.active_time = active_time  # in seconds
        active_time_entry = ttk.Entry(mainframe, width=7, textvariable=active_time)
        active_time_entry.grid(column=2, row=1, sticky=(W, E))

        url = StringVar()
        self.url = url
        url_entry = ttk.Entry(mainframe, width=7, textvariable=url)
        url_entry.grid(column=2, row=2, sticky=(W, E))

        ttk.Button(mainframe, text="Start!", command=self.coordinator).grid(column=3, row=3, sticky=W)

        ttk.Label(mainframe, text="Desired Time (min)").grid(column=1, row=1, sticky=E)
        ttk.Label(mainframe, text="URL").grid(column=1, row=2, sticky=E)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        active_time_entry.focus()