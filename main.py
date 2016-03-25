import csv
import sys
from Tkinter import *
import tkMessageBox


__version__ = "0.1"

__about__ = "To use: \nType the part number in the box. Press search or enter. Results are displayed.\n  \
         Part number must be exact, no partial searches. Search is not case sensitive.\n\n   \
         Created by Alex Ward, inspired by Liam Smith"

         
class VanStockChecker():
    
    def __init__(self):
        #create main window
        self.main = Tk()
        self.main.title("Van Stock Search")
        self.main.iconbitmap(default='icon.ico')
        self.main.resizable(width=FALSE, height=FALSE)

        #buttons
        self.search_frame = Frame(self.main)
        self.text = StringVar()
        self.entry_label = Label(self.search_frame, text="Enter part number:")
        self.entry_label.grid(row=0,column=0, columnspan=2)
        self.entry_box = Entry(self.search_frame, textvariable=self.text)
        self.entry_box.grid(row=1,column=0, columnspan=2)

        self.b1 = Button(self.search_frame,text="Search",width=6)
        self.b1.configure(command=self.search_button)
        self.b2 = Button(self.search_frame,text="Clear",width=6)
        self.b2.configure(command=self.clear)
        self.b1.grid(row=2,column=0)
        self.b2.grid(row=2,column=1)
        self.search_frame.grid(padx=20, row=0,column=0,stick=W+E+N+S)

        #option box
        self.var = StringVar()
        self.option_frame = Frame(self.main)
        self.options = OptionMenu(self.option_frame, self.var,"North East", "North West", "North Midlands", "South Midlands", \
                                   "London", "South & Wales", "All")
        self.var.set("Choose Area")
        self.options.grid(row=1,column=1,stick=W+E+N+S)
        self.option_frame.grid(row=0, column=1)

        #results
        self.results_frame = Frame(self.main)
        self.results_label = Label(self.results_frame, text="Awaiting search...\n")
        self.results_label.grid(row=3, column=0)
        self.results = Listbox(self.results_frame, height=20, width=70)
        self.results.grid(row=4,column=0)
        #results scroll
        self.sb = Scrollbar(self.results_frame,orient=VERTICAL)
        self.sb.grid(row=4,column=1,stick=N+S)
        self.sb.configure(command=self.results.yview)
        self.results.configure(yscrollcommand=self.sb.set)

        #about
        self.about_frame = Label(self.results_frame, text=__about__)
        self.about_frame.grid(row=5, column=0)

        self.results_frame.grid(row=1,columnspan=2)

        #setup
        self.entry_box.focus()
        self.main.bind('<Return>', self.search_button)
        self.main.bind('<KP_Enter>', self.search_button)

        #run
        self.main.mainloop()
    
    def search_parts(self, *args):
        result = []
        try:
            with open('locations.csv', 'rb') as csv_locations:
                temp = csv.reader(csv_locations, delimiter=',')
                holding_locations = dict(temp)
        except IOError:
            self.error_message("Error: No location list as 'locations.csv'.")
        try:
            with open('areas.csv', 'rb') as csv_areas:
                temp = csv.reader(csv_areas, delimiter=',')
                areas = dict(temp)
        except IOError:
            self.error_message("Error: No area list as 'areas.csv'.")
        try:
            with open('export.csv', 'rb') as csvfile:
                temp = csv.reader(csvfile, delimiter=',')
                for x in temp:
                    if x[0].upper() == args[0].upper():
                        try:
                            if self.var.get() == areas[holding_locations[x[2]]] or self.var.get() == "Choose Area" \
                                            or self.var.get() == "All":
                                result.append([holding_locations[x[2]], x[4], x[1]])
                        except KeyError:
                            continue
        except IOError:
            error_message("Error: No Service Director export found as 'export.csv'")
        return result
    
    def error_message(self, message):
        tkMessageBox.showerror("Error", message)

    def search_button(self, event=None):
        self.results.delete(0, END)
        if len(self.search_parts(self.entry_box.get())) == 0:
            if len(self.entry_box.get()) == 0:
                self.results_label.config(text="Please enter a part number!\n", fg="red")
            else:
                self.results_label.config(text="No Results for {}!\n".format(self.entry_box.get()), fg="black")
                self.results.insert(END, "No Results Found for {}.".format(self.entry_box.get()))
        else:
            for item in self.search_parts(self.entry_box.get()):
                self.results_label.config(text="{}\n".format(item[2]), fg="black")
                self.results.insert(END, "{} : Amount: {}".format(item[0], item[1]))
        self.main.update_idletasks()

    def clear(self):
        self.results.delete(0, END)
        self.results_label.config(text="Awaiting search...\n", fg="black")
        self.entry_box.delete(0, END)
        self.main.update_idletasks()
        self.entry_box.focus()


run=VanStockChecker()
