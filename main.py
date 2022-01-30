import datetime
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, ttk
from mutagen.mp3 import MP3
import pygame
import os
# <a href="https://www.flaticon.com/free-icons/ui" title="ui icons">Ui icons created by pictranoosa - Flaticon</a>

tk = Tk()
tk.title("Music App")
tk.geometry("500x310")
tk.configure(bg="white")
tk.resizable(False, False)
pygame.mixer.init()
songs = []
songs_path = []
pause = False
song = ""


def update(restart=False):
    global song
    song_data = MP3(song)
    song_length = song_data.info.length
    current_time = pygame.mixer.music.get_pos() / 1000
    song_length_converted = datetime.timedelta(seconds=int(song_length))
    if pygame.mixer.music.get_pos() / 1000 < 0 or restart:
        current_time = 0
        song_control.config(to=song_length, value=current_time)
        if restart:
            play_btn.config(image=pause_img)
        else:
            play_btn.config(image=play_img)
        current_time_converted = datetime.timedelta(seconds=current_time)
        current_song_second.config(text=current_time_converted)
        return
    elif int(song_control.get()) == int(current_time):
        song_control.config(to=song_length, value=current_time)
    else:
        song_control.config(to=song_length, value=song_control.get())
        current_time_converted = datetime.timedelta(seconds=int(song_control.get()))
        current_song_second.config(text=current_time_converted)
        song_length_label.config(text=song_length_converted)
        next_time = song_control.get() + 1
        song_control.config(value=next_time)
    song_control.after(1200, update)


def slide(x):
    try:
        pygame.mixer.music.play(loops=0, start=song_control.get())
    except pygame.error:
        pass


def add_song():
    global listbox
    filetypes = (
        ("mp3 files", "*.mp3"),
    )
    filename = filedialog.askopenfilenames(title="Find one or multiples mp3 files.", initialdir="/Documents/MusicApp/audio/", filetypes=filetypes)
    for i in filename:
        songs_path.append(i)
        songs.append(os.path.basename(i))
    listbox = Listbox(tk, bg="black", fg="#9ad1ec", width=72, height=10, listvariable=StringVar(value=songs),
                      selectmode=SINGLE)
    listbox.select_set(0)
    listbox.place(x=10, y=30)


def delete_song():
    global listbox, song
    if len(songs) == 0:
        return
    selected_song = listbox.get(ACTIVE)
    for i, song in enumerate(songs_path):
        if selected_song in song:
            songs_path.remove(songs_path[i])
            songs.remove(selected_song)
            item = i
    listbox = Listbox(tk, bg="black", fg="#9ad1ec", width=72, height=10, listvariable=StringVar(value=songs),
                      selectmode=SINGLE)
    if selected_song not in songs:
        if len(songs) > 0 and len(songs) > item:
            listbox.select_set(item)
        else:
            listbox.select_set(item - 1)
    stop_song()
    listbox.place(x=10, y=30)
    play()
    update(restart=True)


def mixer_play_song(song):
    global pause
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    update()
    play_btn.config(image=pause_img)
    pause = False


def play():
    global pause, song
    if len(songs) == 0:
        return
    if not pygame.mixer.music.get_busy() and pygame.mixer.music.get_pos() < 0:
        song = listbox.get(ACTIVE)
        for i in range(len(songs)):
            if song in songs_path[i]:
                song = songs_path[i]
        mixer_play_song(song)
    if pygame.mixer.music.get_pos() > 1:
        if pause:
            pygame.mixer.music.unpause()
            pause = False
            play_btn.config(image=pause_img)
        else:
            pause = True
            pygame.mixer.music.pause()
            play_btn.config(image=play_img)


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


def stop_song():
    pygame.mixer.music.stop()


play_img = ImageTk.PhotoImage(Image.open("img/play.png"))
pause_img = ImageTk.PhotoImage(Image.open("img/pause.png"))
stop_img = ImageTk.PhotoImage(Image.open("img/stop.png"))
previous_img = ImageTk.PhotoImage(Image.open("img/previous.png"))
next_img = ImageTk.PhotoImage(Image.open("img/next.png"))


listbox = Listbox(tk, bg="black", fg="#9ad1ec", width=72,
                  height=10, selectmode=SINGLE)
style = ttk.Style()
style.configure("TButton", padding=0, background="#ffffff", borderwidth=0)
add_btn = ttk.Button(tk, text="Add song", command=add_song)
del_btn = ttk.Button(tk, text="Delete song", command=delete_song)
play_btn = ttk.Button(tk, image=play_img, command=play, style="TButton")
stop_btn = ttk.Button(tk, image=stop_img, command=stop_song)
previous_btn = ttk.Button(tk, image=previous_img, command=previous_song)
next_btn = ttk.Button(tk, image=next_img, command=next_song)
style = ttk.Style()
style.configure("TScale", background="white")
volume_label = ttk.Label(tk, text="Volume", background="white")
label_0 = ttk.Label(tk, text="0", background="white")
label_100 = ttk.Label(tk, text="100", background="white")
volume_control = ttk.Scale(tk, from_=0, to=100, style="TScale", orient=VERTICAL, value=100, length=145,
                           command=lambda x: pygame.mixer.music.set_volume(volume_control.get() / 100))
song_control = ttk.Scale(tk, from_=0, style="TScale", command=slide, length=350)
current_song_second = ttk.Label(tk, text="00:00", background="white")
song_length_label = ttk.Label(tk, text="00:00", background="white")

del_btn.place(x=90, y=0)
add_btn.place(x=10, y=0)
listbox.place(x=10, y=30)
play_btn.place(x=160, y=230)
stop_btn.place(x=260, y=230)
previous_btn.place(x=60, y=230)
next_btn.place(x=360, y=230)
volume_label.place(x=450, y=0)
label_0.place(x=468, y=20)
label_100.place(x=460, y=180)
volume_control.place(x=460, y=35)
song_control.place(x=50, y=200)
current_song_second.place(x=10, y=203)
song_length_label.place(x=404, y=203)


tk.mainloop()
