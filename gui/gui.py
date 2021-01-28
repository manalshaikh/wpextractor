import tkinter as tk
from tkinter import messagebox
from tkinter import *
import os
import csv
import json
import sys
import requests
import urllib
from urllib.request import Request, urlopen, HTTPError
from urllib.parse import urlparse

win = tk.Tk()

win.geometry("300x100")
win.title("WPExtractor by Manal Shaikh")

#CheckVar
CheckVar1 = IntVar()

#Label
label = Label(win, text="URL - ")
label.place(x=5, y=25)

#Entry
entry1 = Entry(win, text="URL - ")
entry1.place(x=45, y=22.5)

#Checkbox
check1 = Checkbutton(win, text = "Pages", variable=CheckVar1, onvalue=1, offvalue=0)
check1.place(x=220, y=25)
#Function
def checkentry():
    if CheckVar1.get():
        tk.messagebox.showinfo(message=CheckVar1.get())
    else:
        tk.messagebox.showinfo(message="Its off")

##MainCode

def get_urls(filename):
    urls = []

    file = open(filename, "r")

    for i in file:
        i = i.replace("\n", "")
        urls.append(i)
    return urls

def get_data_url(url_link):
    req = Request(url_link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    ## Fetching hostname of the URL
    parsed_uri = urlparse(url_link)
    result = '{uri.netloc}'.format(uri=parsed_uri)
    print(result)
    # Write data to file
    filename = "data/" + result + "-raw.txt"
    file_ = open(filename, 'wb')
    file_.write(webpage)
    file_.close()


    with open(filename) as json_file:
        json_data = json.load(json_file)

    C_data = []

    for n in json_data:  
    
        r={}
        r["Modified"] = n['modified']
        r["Title"] = n['title']['rendered']
        r["Content"] = n['content']['rendered']
        r["Link"] = n['link']

        # JSON Conversion

        j_data = {
            "modified/posted" : r["Modified"],
            "title" : r["Title"],
            "content" : r["Content"],
            "link" : r["Link"]
        }

        C_data.append(j_data)
        print("Title: " + r["Title"])
        print("Status: Downloaded")
        
    json_object = json.dumps(C_data, indent = 4) 

    # Writing to sample.json 
    with open("data/" + result + "-data.json", "w") as outfile: 
        outfile.write(json_object)
    print("Extracted Successfully")

def countdown(count, label):
    if count > 0:
        win.after(1000, countdown, count-1, label)
    elif count == 0:
        win.after(1000, countdown, count-1, label)
    elif count < 0:
        label.destroy()

def execution():
    try:
        url = entry1.get()
        if CheckVar1.get() == 1:
            url = url + "/wp-json/wp/v2/pages/?per_page=100"
        else:
            url = url + "/wp-json/wp/v2/posts/?per_page=100"
        get_data_url(url)
    except urllib.error.HTTPError as e:  # Error handling begins
        ResponseData = e.read().decode("utf8", "ignore")
        fcode = e.code
        if fcode == 404: #Updating Label [Work in Progress]
            status = Label(win, text="Invalid URL!")
        if fcode == 403:
            status = Label(win, text="URL Forbidden")
        if fcode == 401:
            status = Label(win, text="Unauthorized Access")
        if fcode == 408:
            status = Label(win, text="Timed out")
        if fcode == 500:
            status = Label(win, text="Internal Server Error")
        if fcode == 502:
            status = Label(win, text="Bad Gateway")
        status.place(x=150, y=50)
        countdown(10, status)
    statuslabel.place(x=100, y=50)
    
#Button
button1 = Button(win, text="Grab", command=execution)
button1.place(x=45, y=50)

#Status Label [Work in Progress]
statuslabel = Label(win, text="Status:")


#GUI Window Opens here
win.mainloop()