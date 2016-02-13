import csv
import sys
from Tkinter import *
import tkMessageBox


__version__ = "0.1"

__about__ = "To use: \nType the part number in the box. Press search or enter. Results are displayed.\n\
                Part number must be exact, no partial searches. Search is not case sensitive.\n\
                Created by Alex Ward."



def search_parts(*args):
    result = []
    try:
        with open('locations.csv', 'rb') as csv_locations:
            temp = csv.reader(csv_engineers, delimiter=',')
            holding_locations = dict(temp)
    except IOError:
        error_message("Error: No engineer list as 'engineers.csv'.")
    try:
        with open('areas.csv', 'rb') as csv_areas:
            temp = csv.reader(csv_areas, delimiter=',')
            areas = dict(temp)
    except IOError:
        error_message("Error: No area list as 'areas.csv'.")
    try:
        with open('export.csv', 'rb') as csvfile:
            temp = csv.reader(csvfile, delimiter=',')
            for x in temp:
                if x[0].upper() == args[0].upper():
                    try:
                        if var.get() == areas[holding_locations[x[2]]] or var.get() == "Choose Area" \
                                        or var.get() == "All":
                            result.append([holding_locations[x[2]], x[4], x[1]])
                    except KeyError:
                        continue
    except IOError:
        error_message("Error: No export found as 'export.csv'")
    return result

def error_message(message):
    tkMessageBox.showerror("Error", message)

def search_button(event=None):
    results.delete(0, END)
    if len(search_parts(entry_box.get())) == 0:
        if len(entry_box.get()) == 0:
            results_label.config(text="Please enter a part number!\n", fg="red")
        else:
            results_label.config(text="No Results for {}!\n".format(entry_box.get()), fg="black")
            results.insert(END, "No Results Found for {}.".format(entry_box.get()))
    else:
        for item in search_parts(entry_box.get()):
            results_label.config(text="{}\n".format(item[2]), fg="black")
            results.insert(END, "{} : Amount: {}".format(item[0], item[1]))
    main.update_idletasks()

def clear():
    results.delete(0, END)
    results_label.config(text="Awaiting search...\n", fg="black")
    entry_box.delete(0, END)
    main.update_idletasks()
    entry_box.focus()

#create main window
main = Tk()
main.title("Stock Search")
main.resizable(width=FALSE, height=FALSE)


#buttons
search_frame = Frame(main)
text = StringVar()
entry_label = Label(search_frame, text="Enter part number:")
entry_label.grid(row=0,column=0, columnspan=2)
entry_box = Entry(search_frame, textvariable=text)
entry_box.grid(row=1,column=0, columnspan=2)

b1 = Button(search_frame,text="Search",width=6)
b1.configure(command=search_button)
b2 = Button(search_frame,text="Clear",width=6)
b2.configure(command=clear)
b1.grid(row=2,column=0)
b2.grid(row=2,column=1)
search_frame.grid(padx=20, row=0,column=0,stick=W+E+N+S)

#option box
var = StringVar()
option_frame = Frame(main)
options = OptionMenu(option_frame, var,"North East", "North West", "North Midlands", "South Midlands", \
                           "London", "South & Wales", "All")
var.set("Choose Area")
options.grid(row=1,column=1,stick=W+E+N+S)
option_frame.grid(row=0, column=1)

#results
results_frame = Frame(main)
results_label = Label(results_frame, text="Awaiting search...\n")
results_label.grid(row=3, column=0)
results = Listbox(results_frame, height=20, width=70)
results.grid(row=4,column=0)
#results scroll
sb = Scrollbar(results_frame,orient=VERTICAL)
sb.grid(row=4,column=1,stick=N+S)
sb.configure(command=results.yview)
results.configure(yscrollcommand=sb.set)

#about
about_frame = Label(results_frame, text=__about__)
about_frame.grid(row=5, column=0)

results_frame.grid(row=1,columnspan=2)

#setup
entry_box.focus()
main.bind('<Return>', search_button)
main.bind('<KP_Enter>', search_button)

#run
main.mainloop()
