from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import pygame
import os

# <a href="https://www.flaticon.com/free-icons/ui" title="ui icons">Ui icons created by pictranoosa - Flaticon</a>

tk = Tk()
tk.title("Music App")
tk.configure(bg="white")
pygame.mixer.init()
songs = []
songs_path = []
pause = False
song = ""


def add_song():
    global listbox
    filetypes = (
        ("mp3 files", "*.mp3"),
    )
    filename = filedialog.askopenfilenames(title="Find one or multiples mp3 files.", initialdir="/Documents/MusicApp/audio/", filetypes=filetypes)
    for i in filename:
        songs_path.append(i)
        songs.append(os.path.basename(i))
    listbox = Listbox(tk, bg="black", fg="#9ad1ec", width=60, height=10, listvariable=StringVar(value=songs),
                      selectmode=SINGLE)
    listbox.grid(column=0, row=1, columnspan=5)
    listbox.select_set(0)


def delete_song():
    global listbox
    for i in listbox.curselection():
        songs.remove(listbox.get(i))
    listbox = Listbox(tk, bg="black", fg="#9ad1ec", width=60, height=10, listvariable=StringVar(value=songs),
                      selectmode=SINGLE)
    listbox.grid(column=0, row=1, columnspan=5)


def mixer_play_song(song):
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()


def play():
    global song
    for i in listbox.curselection():
        song = songs_path[i]
        mixer_play_song(song)


def next_song():
    global song
    if song == "":
        return
    if len(songs_path) - 1 > songs_path.index(song):
        song = songs_path.index(song) + 1
        listbox.selection_clear(0, END)
        listbox.select_set(song)
        song = songs_path[song]
    mixer_play_song(song)


def previous_song():
    global song
    if song == "":
        return
    if 0 < songs_path.index(song):
        song = songs_path.index(song) + -1
        listbox.selection_clear(0, END)
        listbox.select_set(song)
        song = songs_path[song]
    mixer_play_song(song)


def pause_song():
    global pause
    if pause:
        pygame.mixer.music.unpause()
        pause = False
    else:
        pause = True
        pygame.mixer.music.pause()


def stop_song():
    pygame.mixer.music.stop()


play_img = ImageTk.PhotoImage(Image.open("img/play.png"))
pause_img = ImageTk.PhotoImage(Image.open("img/pause.png"))
stop_img = ImageTk.PhotoImage(Image.open("img/stop.png"))
previous_img = ImageTk.PhotoImage(Image.open("img/previous.png"))
next_img = ImageTk.PhotoImage(Image.open("img/next.png"))


listbox = Listbox(tk, bg="black", fg="#9ad1ec", width=70,
                  height=10, selectmode=SINGLE)
add_btn = Button(tk, text="Add song", bg="white", command=add_song, width=10, height=2)
del_btn = Button(tk, text="Delete song", bg="white",
                 command=delete_song, width=10, height=2)
play_btn = Button(tk, image=play_img, bg="white", highlightthickness=0, borderwidth=0, command=play)
pause_btn = Button(tk, image=pause_img, bg="white", highlightthickness=0, borderwidth=0, command=pause_song)
stop_btn = Button(tk, image=stop_img, bg="white", highlightthickness=0, borderwidth=0, command=stop_song)
previous_btn = Button(tk, image=previous_img, bg="white", highlightthickness=0, borderwidth=0, command=previous_song)
next_btn = Button(tk, image=next_img, bg="white", highlightthickness=0, borderwidth=0, command=next_song)

del_btn.grid(column=1, row=0)
add_btn.grid(column=0, row=0)
listbox.grid(column=0, row=1, columnspan=5)
play_btn.grid(column=2, row=2)
pause_btn.grid(column=1, row=2)
stop_btn.grid(column=3, row=2)
previous_btn.grid(column=0, row=2)
next_btn.grid(column=4, row=2)

tk.mainloop()
