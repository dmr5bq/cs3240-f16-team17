from tkinter import *
from simplecrypt import encrypt, decrypt
from tkinter import ttk
import os
import platform
from tkinter import simpledialog
from os.path import expanduser

file = ""
home = os.getcwd()
curpath = home
root = Tk()
e = Entry(root, width = 50)
e.insert(0, home)
e.grid(row = 0, column = 0)
l = Listbox(root, height=5)

def get_filenames():
    global sPath
    sPath = e.get()
    global curpath
    curpath = sPath
    return os.listdir(sPath)

def OnClick(event):
    widget = event.widget
    value=str(l.get(l.curselection()))
    global file
    if(platform.mac_ver()[0] == ''):
        file = curpath +"\\" +value
    else:
        file = curpath + "/" + value
    # value = widget.get(selection[0])
    # print ("selection:", selection, ": '%s'" % value)

def encrypt1():
    with open(file, 'rb') as inp:
        plaintext = inp.read()
    password = simpledialog.askstring('Key Value', "Please Enter a Key", show='*')
    ciphertext = encrypt(password, plaintext)
    with open(file, 'wb') as outp:
        outp.write(ciphertext)
    if (platform.mac_ver()[0] == ''):
        os.startfile(file, "open")

def decrypt1():
    with open(file, 'rb') as inp:
        ciphertext = inp.read()
    password = simpledialog.askstring('Key Value', "Please Enter the Key", show='*')
    plaintext = decrypt(password, ciphertext)
    with open(file, 'wb') as outp:
        outp.write(plaintext)
    if (platform.mac_ver()[0] == ''):
        os.startfile(file, "open")

def updateList():
    l.delete(0, END)
    for filename in get_filenames():
        l.insert(END, filename)

def main():
    button0 = Button(text="Set Path", command = updateList)
    button0.grid(row=0, column=1)
    l.grid(column=0, row=1, sticky=(N,W,E,S))
    s = ttk.Scrollbar(root, orient=VERTICAL, command=l.yview)
    s.grid(column=1, row=1, sticky=(N,S))
    l['yscrollcommand'] = s.set
    ttk.Sizegrip().grid(column=1, row=2, sticky=(S,E))
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    for filename in get_filenames():
        l.insert(END, filename)
    l.bind("<<ListboxSelect>>", OnClick)
    button1 = Button(text="Decrypt", command = decrypt1)
    button2 = Button(text="Encrypt", command = encrypt1)
    button1.grid(row=4)
    button2.grid(row=3)
    root.mainloop()
