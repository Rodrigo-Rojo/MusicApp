from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, ttk
from mutagen.mp3 import MP3
import pygame
import os
from time import sleep
# <a href="https://www.flaticon.com/free-icons/ui" title="ui icons">Ui icons created by pictranoosa - Flaticon</a>

tk = Tk()
tk.title("Music App")
tk.configure(bg="white")
pygame.mixer.init()
songs = []
songs_path = []
pause = False
song = ""

# audio = MP3("audio/Midnight City.mp3")
# print(audio.info.length)
# print(audio.info.bitrate)


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
    # audio = MP3(songs_path[0])
    # lenght = audio.info.length
    # song_control = ttk.Scale(tk, from_=0, to=lenght, command=lambda x: pygame.mixer.music.set_pos(song_control.get()))
    # song_control.grid(column=1, row=3)


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


def slide(x):
    song = listbox.get(ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(song_control.get()))


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
        # audio = MP3(songs_path[song])
        # lenght = audio.info.length
        # song_control = ttk.Scale(tk, from_=0, to=lenght,
        #                          command=lambda x: pygame.mixer.music.set_pos(song_control.get()))
        # song_control.grid(column=1, row=3)
    mixer_play_song(song)


def song_data():
    song = listbox.get(ACTIVE)
    audio = MP3(songs_path[song])
    lenght = audio.info.length
    current_time = pygame.mixer.music.get_pos() / 1000
    song_control.config(to=lenght, value=current_time)
    song_control.after(1000, song_data())


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
volume_control = ttk.Scale(tk, from_=0, to=100, value=100, command=lambda x: pygame.mixer.music.set_volume(volume_control.get() / 100))
song_control = ttk.Scale(tk, from_=0, to=100, command=slide, length=360, value=0)

del_btn.grid(column=1, row=0)
add_btn.grid(column=0, row=0)
listbox.grid(column=0, row=1, columnspan=5)
play_btn.grid(column=2, row=2)
pause_btn.grid(column=1, row=2)
stop_btn.grid(column=3, row=2)
previous_btn.grid(column=0, row=2)
next_btn.grid(column=4, row=2)
volume_control.grid(column=0, row=3)
song_control.grid(column=1, row=3)


tk.mainloop()
