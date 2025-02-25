import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import time 
import ntpath

from pathlib import Path
from playsound import playsound
import pygame
from pygame import mixer
import ftplib
from ftplib import FTP



PORT = 8079
IP_ADDRESS = '127.0.0.2'
SERVER  = None
BUFFER_SIZE = 4096
global song_counter 
song_counter = 0




name = None 
listbox = None
filePathLabel = None


def openChatWindow():

    print("\n\t\t\t\t MUSICAL APP")

    window=Tk()
    window.title('Music Window')
    window.geometry("300x300")
    window.configure(bg='LightSkyBlue')

    global name 
    global listbox
    global textarea
    global labelchat
    global text_message
    global filePathLabel

    selectlabel = Label(window,text="Select Song",bg='LightSkyBlue',font = ("Calibri",8))
    selectlabel.place(x=2,y=1)

    listbox = Listbox(window,height=10,width= 39,activestyle='dotbox',bg='LightSkyBlue',borderwidth=2,font = ("Calibri",10))
    listbox.place(x=10,y=18)
    for file in os.listdir('shared_files'):
        filename = os.fsdecode(file)
        listbox.insert(song_counter,filename)
        song_counter = song_counter + 1

    scrollbar1  = Scrollbar(listbox)
    scrollbar1.place(relheight=1,relx=1)
    scrollbar1.config(command= listbox.yview)

    PlayButton = Button(window,text="Play",width=10,bd=1,bg='SkyBlue',font=("Calibri",10),command = play)
    PlayButton.place(x=30,y=200)

    Stop = Button(window,text="Stop",width=10,bd=1,bg='SkyBlue',font=("Calibri",10),command = stop)
    Stop.place(x=200,y=200)

    Upload = Button(window,text="Upload",width=10,bd=1,bg='SkyBlue',font=("Calibri",10))
    Upload.place(x=30,y=250)

    Download = Button(window,text="Download",width=10,bd=1,bg='SkyBlue',font=("Calibri",10))
    Download.place(x=200,y=250)

    infoLabel = Label(window,text="",fg="blue",font=("Calibri",8))
    infoLabel.place(x=4,y=280)

    ResumeButton=Button(window,text="Resume",width=10,bd=1,bg='SKyBlue',font=("Calibri",10),command=resume)
    ResumeButton.place(x=30,y=250)

    PauseButton=Button(window,text="Pause",width=10,bd=1,bg='SkyBlue',font=("Calibri",10),command=pause)
    PauseButton.place(x=200,y=250)

    window.mainloop()

def play():
    global song_selected
    global infoLabel
    song_selected = listbox.get(ANCHOR)

    pygame
    mixer.init()
    mixer.music.load('shared_files'+song_selected)
    mixer.music.play()
    if(song_selected != ""):
        infoLabel.configure(text="Now Playing :"+song_selected)
    else:
        infoLabel.configure(text="")

def stop():
    global song_selected
    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.pause()
    infoLabel.configure(text="")

def resume():
    global song_selected
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.play()

def pause():
    global song_selected
    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.pause()

def browseFiles():
    global listbox
    global song_counter
    global filePathLabel

    try:
        filename = filedialog.askopenfilename()
        HOSTNAME = "127.0.0.1"
        USERNAME = "lftpd"
        PASSWORD = "lftpd"

        ftp_server = FTP(HOSTNAME,USERNAME,PASSWORD)
        ftp_server.encoding = "utf-8"
        ftp_server.cwd('shared_files')
        fname = ntpath.basename(filename)
        with open(filename,'rb') as file:
            ftp_server.storbinary(f"STOR {fname}",file)
        ftp_server.dir()
        ftp_server.quit()

        listbox.insert(song_counter,fname)
        song_counter = song_counter+1
        

    except FileNotFoundError:
        print("Cancel Button Pressed")

def download():
    song_to_download=listbox.get(ANCHOR)
    infoLabel.configure(text="Downloading"+song_to_download)
    HOSTNAME = "127.0.0.1"
    USERNAME = "lftpd"
    PASSWORD = "lftpd"
    home=str(Path.home())
    download_path=home+"/Downloads"
    ftp_server = ftplib.FTP(HOSTNAME,USERNAME,PASSWORD)
    ftp_server.encoding = "utf-8"
    ftp_server.cwd('shared_files')
    local_filename = os.path.join(download_path,song_to_download)
    file = open(local_filename,'wb')
    ftp_server.retrbinary('RETR'+song_to_download,file.write)
    ftp_server.dir()
    file.close()
    ftp_server.quit()
    infoLabel.configure(text="Download Complete")
    time.sleep(1)
    if(song_selected !=""):
        infoLabel.configure(text="Now Playing"+song_selected)
    else:
        infoLabel.configure(text="")
def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS,PORT))

    openChatWindow()
setup()
