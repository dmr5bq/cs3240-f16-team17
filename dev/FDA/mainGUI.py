from tkinter import *
from simplecrypt import encrypt, decrypt
from tkinter import ttk
import os
import platform
from tkinter import simpledialog
from tkinter import messagebox
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES
import struct

file = ""
home = os.getcwd()
curpath = home
root = Tk()
e = Entry(root, width = 50)
e.insert(0, home)
e.grid(row = 0, column = 0)
l = Listbox(root, height=5)
selection = ""

def get_filenames():
    global sPath
    sPath = e.get()
    global curpath
    curpath = sPath
    return os.listdir(sPath)

def OnClick(event):
    widget = event.widget
    value=str(l.get(l.curselection()))
    global selection
    selection = value
    global file
    if(platform.mac_ver()[0] == ''):
        file = curpath +"\\" +value
    else:
        file = curpath + "/" + value
    # value = widget.get(selection[0])
    # print ("selection:", selection, ": '%s'" % value)

def decrypt_file():
    sk = simpledialog.askstring('Key Value', "Please Enter the Secret Key", show='*')
    if len(sk) not in (16, 24, 32):
        if(len(sk) < 16):
            sk = sk + ('0' * (16 - len(sk)))
        elif(len(sk) < 16):
            sk = sk + ('0' * (24 - len(sk)))
        elif(len(sk) < 32):
            sk = sk + ('0' * (32 - len(sk)))
        else:
            sk = sk[0:32]
    if '.enc' == file[len(file)-4:len(file)]:
        try:
            with open(file, 'rb') as inFile:
                fSize = struct.unpack('<Q', inFile.read(struct.calcsize('Q')))[0]
                initVector = inFile.read(16)
                AES_dec = AES.new(sk, AES.MODE_CBC, initVector)
                with open('DEC_' + selection[0:len(selection)-4], 'wb') as outFile:
                    while True:
                        chunk = inFile.read(1024)
                        if len(chunk) == 0:
                            break
                        outFile.write(AES_dec.decrypt(chunk))
                    outFile.truncate(fSize)
                    outFile.close()
                inFile.close()
            updateList()
            return True
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "File does not exist")
            return False
    else:
        print("Invalid extension, must end in .enc")
        messagebox.showerror("Invalid Extension", "File must end in .enc")
        return False

def encrypt_file():
    sk = simpledialog.askstring('Key Value', "Please Enter the Secret Key", show='*')
    if len(sk) not in (16, 24, 32):
        if(len(sk) < 16):
            sk = sk + ('0' * (16 - len(sk)))
        elif(len(sk) < 16):
            sk = sk + ('0' * (24 - len(sk)))
        elif(len(sk) < 32):
            sk = sk + ('0' * (32 - len(sk)))
        else:
            sk = sk[0:32]
    initVector = os.urandom(16)
    AES_enc = AES.new(sk, AES.MODE_CBC, initVector)
    filesize = os.path.getsize(file)
    try:
        with open(file, 'rb') as inFile:
            with open(file + '.enc', 'wb') as outFile:
                outFile.write(struct.pack('<Q', filesize))
                outFile.write(initVector)
                while True:
                    chunk = inFile.read(1024)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += (' ' * (16 - len(chunk) % 16)).encode()
                    outFile.write(AES_enc.encrypt(chunk))
                outFile.close()
            inFile.close()
        updateList()
        return True
    except FileNotFoundError:
        messagebox.showerror("File Not Found", "File does not exist")
        return False

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
    button1 = Button(text="Encrypt", command = encrypt_file)
    button2 = Button(text="Decrypt", command=decrypt_file)
    button1.grid(row=3)
    button2.grid(row=4)
    root.mainloop()
