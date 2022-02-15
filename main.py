import datetime
import random
from tkinter import *
from tkinter.messagebox import showerror
import pytube.exceptions
from PIL import Image, ImageTk
from tkinter import filedialog, ttk
from mutagen.mp3 import MP3
import pygame
from moviepy.editor import *
from pytube import YouTube
from pyyoutube import Api
import os
tk = Tk()
tk.iconbitmap(r"D:\Documents\MusicApp\img\mp3-player.ico")
tk.tk.call("source", r"D:\Documents\MusicApp\sun-valley.tcl")
tk.tk.call("set_theme", "dark")
tk.title("Music App")
tk.geometry("700x400")
tk.resizable(False, False)
API_KEY = "AIzaSyA82pzJpJMQ9mWS1TrFDRtjGAcw6ZhMCWM"
if not os.path.exists("audio"):
    os.makedirs("audio")
songs = [file for file in os.listdir("audio")]
songs_path = [os.path.abspath(f"audio/{file}") for file in os.listdir("audio")]
paused = False
song = ""
stopped = False


def update(restart=False):
    global song, paused
    song_length = MP3(song).info.length
    current_time = pygame.mixer.music.get_pos() / 1000
    song_length_converted = datetime.timedelta(seconds=int(song_length))
    if pygame.mixer.music.get_pos() / 1000 < 0 or restart:
        current_time = 0
        time_control.config(to=song_length, value=current_time)
        if restart:
            play_btn.config(image=paused_img)
        else:
            play_btn.config(image=play_img)
        current_time_converted = datetime.timedelta(seconds=current_time)
        current_second_label.config(text=current_time_converted)
        return
    elif int(time_control.get()) == int(current_time):
        time_control.config(to=song_length, value=current_time)
    else:
        time_control.config(to=song_length, value=time_control.get())
        current_time_converted = datetime.timedelta(
            seconds=int(time_control.get()))
        current_second_label.config(text=current_time_converted)
        song_length_label.config(text=song_length_converted)
        next_time = time_control.get() + 1
        time_control.config(value=next_time)
    time_control.after(1000, update)


def slide(x):
    try:
        pygame.mixer.music.play(loops=0, start=time_control.get())
    except pygame.error:
        pass


def add_song():
    global song_box
    filetypes = (
        ("mp3 files", "*.mp3"),
    )
    filename = filedialog.askopenfilenames(
        title="Find one or multiples mp3 files.", initialdir="/", filetypes=filetypes)
    for i in filename:
        songs_path.append(i)
        songs.append(os.path.basename(i))

    song_box = Listbox(tk, fg="#9ad1ec", width=82, height=10, listvariable=StringVar(value=songs),
                       selectmode=SINGLE)
    song_box.place(x=10, y=70)
    song_box.select_set(0)
    song_box.bind('<Double-1>', play_selected_song)


def delete_song():
    global song_box, song
    if len(songs) == 0:
        return
    selected_song = song_box.get(ACTIVE)
    for i, song in enumerate(songs_path):
        if selected_song in song:
            songs_path.remove(songs_path[i])
            songs.remove(selected_song)
            item = i

    song_box = Listbox(tk, fg="#9ad1ec", width=82, height=10, listvariable=StringVar(value=songs),
                       selectmode=SINGLE)
    if selected_song not in songs:
        if len(songs) > 0 and len(songs) > item:
            song_box.select_set(item)
        else:
            song_box.select_set(item - 1)
    stop_song()
    song_box.place(x=10, y=70)
    song_box.bind('<Double-1>', play_selected_song)
    play()
    update(restart=True)


def mixer_play_song(song):
    global paused, stopped
    pygame.mixer.stop()
    update(restart=True)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    update()
    play_btn.config(image=paused_img)
    paused = False
    stopped = False
    is_over()


def is_over():
    global stopped, paused
    if not pygame.mixer.music.get_busy() and not stopped and not paused:
        next_song()
    tk.after(1000, is_over)


def play(event=None):
    global paused, song
    if len(songs) == 0:
        return
    if not pygame.mixer.music.get_busy() and pygame.mixer.music.get_pos() < 0:
        song = song_box.get(ACTIVE)
        song_box.select_set(ACTIVE)

        for i in range(len(songs)):
            if song in songs_path[i]:
                song = songs_path[i]
        mixer_play_song(song)
    if pygame.mixer.music.get_pos() > 1 or event:
        if paused:
            pygame.mixer.music.unpause()
            paused = False
            play_btn.config(image=paused_img)
        else:
            paused = True
            pygame.mixer.music.pause()
            play_btn.config(image=play_img)


def play_selected_song(event=None):
    global song
    if event:
        for i in song_box.curselection():
            song = songs_path[i]
        mixer_play_song(song)


def next_song():
    global song
    if song == "":
        return
    if len(songs_path) - 1 > songs_path.index(song):
        song = songs_path.index(song) + 1
        song_box.selection_clear(0, END)
        song_box.select_set(song)
        song = songs_path[song]
    mixer_play_song(song)


def previous_song():
    global song
    if song == "":
        return
    if 0 < songs_path.index(song):
        song = songs_path.index(song) + -1
        song_box.selection_clear(0, END)
        song_box.select_set(song)
        song = songs_path[song]
    mixer_play_song(song)


def stop_song():
    global stopped
    pygame.mixer.music.stop()
    song_box.selection_clear(0, END)
    stopped = True


def shuffle():
    global song_box, songs, songs_path
    stop_song()
    both = list(zip(songs, songs_path))
    random.shuffle(both)
    songs, songs_path = zip(*both)
    songs = list(songs)
    songs_path = list(songs_path)

    song_box = Listbox(tk, fg="#9ad1ec", width=82, height=10, listvariable=StringVar(value=songs),
                       selectmode=SINGLE)
    song_box.select_set(0)
    song_box.place(x=10, y=70)
    song_box.bind('<Double-1>', play_selected_song)
    play()


def add_song_from_yt(youtube_ids):
    global song_box, progress_bar
    progress = 100 / len(youtube_ids)
    loading_label = Label(tk, text=f"Loading...")
    loading_label.place(x=250, y=120)
    for yt_id in youtube_ids:
        progress_bar["value"] += progress
        tk.update_idletasks()
        try:
            yt = YouTube(f"https://www.youtube.com/watch?v={yt_id}")
            itag = yt.streams.filter(only_audio=True)[0].itag
            yt = yt.streams.get_by_itag(itag)
            yt_song = yt.download()

            snd = AudioFileClip(yt_song)
            song_name = f"audio/{os.path.basename(yt_song)[:-4]}.mp3"
            snd.write_audiofile(filename=song_name)
            songs_path.append(song_name)
            songs.append(os.path.basename(song_name))
            os.remove(yt_song)
        except pytube.exceptions.LiveStreamError as e:
            showerror(title=f"Error:", message=f"There was an error while getting your song.\n{e}.").pack()
        except pytube.exceptions.RegexMatchError as e:
            showerror(title=f"Error:", message=f"There was an error while getting your song.\n{e}.").pack()

    song_box = Listbox(tk, fg="#9ad1ec", width=82, height=10, listvariable=StringVar(value=songs),
                       selectmode=SINGLE)
    song_box.select_set(0)
    song_box.place(x=10, y=70)
    song_box.bind('<Double-1>', play_selected_song)
    loading_label.destroy()
    progress_bar.destroy()


def handle_add():
    global search_box, yt_window, progress_bar
    progress_bar = ttk.Progressbar(
        tk, orient=HORIZONTAL, length=300, mode="determinate")
    progress_bar.place(x=150, y=100)
    selected_songs.append(search_box.curselection())
    yt_window.destroy()
    add_yt_songs()


def open_win(video_list):
    global selected_songs, search_box, yt_window
    selected_songs = []
    yt_window = Toplevel(tk)
    yt_window.geometry("500x250")
    yt_window.title("Songs")
    search_box = Listbox(yt_window, fg="#9ad1ec", width=72,
                         listvariable=StringVar(value=video_list), selectmode=SINGLE)
    search_box.place(x=0, y=30)
    Label(yt_window,
          text=f"Select one or multiple songs to keep in the app showing {len(video_list)} you can scroll.").pack()
    add = Button(yt_window, text="Add Songs", command=handle_add)
    close = Button(yt_window, text="Close Window", command=yt_window.destroy)
    close.place(x=250, y=220)
    add.place(x=150, y=220)


def search_song(event=None):
    video_list = []
    api = Api(api_key=API_KEY)
    search = api.search_by_keywords(q=search_entry.get())
    for video in search.items:
        video_list.append(video.snippet.title)
    open_win(video_list)


def add_yt_songs():
    global selected_songs, progress_bar
    api = Api(api_key=API_KEY)
    search = api.search_by_keywords(q=search_entry.get())
    yt_ids = [search.items[i].id.videoId for i in selected_songs[0]]
    add_song_from_yt(yt_ids)


def volume(event):
    global volume_control
    current_volume = volume_control.get()
    if event.keysym == "Up":
        current_volume += 10
    else:
        current_volume -= 10
    pygame.mixer.music.set_volume(current_volume / 100)
    volume_control = ttk.Scale(tk,
                               from_=0, to=100,
                               style="TScale",
                               orient=VERTICAL,
                               value=current_volume, length=120,
                               command=lambda x: pygame.mixer.music.set_volume(volume_control.get() / 100))
    volume_control.place(x=630, y=93)


def handle_help():
    help_window = Toplevel(tk)
    help_window.geometry("700x350")
    help_window.title("Help")
    ttk.Button(help_window, text="Add Song").place(x=10, y=10)
    Label(help_window, text="Click add song button to search for mp3 files to add them to the playlist.").place(x=170, y=15)
    ttk.Button(help_window, text="Remove Song").place(x=10, y=50)
    Label(help_window, text="Select a song from the list and click button Remove Song to remove song\n from playlist.").place(x=170, y=55)
    e = ttk.Entry(help_window)
    e.insert(0, "Song Name...")
    e.place(x=10, y=105)
    ttk.Button(help_window, text="Search Online Songs").place(x=10, y=145)
    Label(help_window, text="You have to option to search youtube songs, Use the Entry to search for").place(x=170, y=95)
    Label(help_window, text="any song you wish, press Enter or press 'Search Online Songs'").place(x=170, y=115)
    Label(help_window, text="once you do another window will open with a playlist showing the first").place(x=170, y=135)
    Label(help_window, text="25 options available, select one or many then proceed to click 'Add Songs'").place(x=170, y=155)
    Label(help_window, text="after the app will proceed to download selected songs.").place(x=170, y=175)
    Listbox(help_window, fg="#9ad1ec", width=15, height=4, listvariable=StringVar(value=[f"Song {i}" for i in range(10)]),
            selectmode=SINGLE).place(x=10, y=215)
    Label(help_window, text="You can select a single song from listbox then click ▶ button to play selected song").place(x=170, y=220)
    Label(help_window, text="Or you can double click on a song this will play the selected song.").place(x=170, y=240)
    Label(help_window, text="Sometimes you will have more items that listbox shows you can scroll.").place(x=170, y=260)



play_img = ImageTk.PhotoImage(Image.open(r"D:\Documents\MusicApp\img\play.png"))
paused_img = ImageTk.PhotoImage(Image.open(r"D:\Documents\MusicApp\img\pause.png"))
stop_img = ImageTk.PhotoImage(Image.open(r"D:\Documents\MusicApp\img\stop.png"))
previous_img = ImageTk.PhotoImage(Image.open(r"D:\Documents\MusicApp\img\previous.png"))
next_img = ImageTk.PhotoImage(Image.open(r"D:\Documents\MusicApp\img\next.png"))
shuffle_img = ImageTk.PhotoImage(Image.open(r"D:\Documents\MusicApp\img\shuffle.png"))

add_btn = ttk.Button(tk, text="Add Song", command=add_song)
add_btn.place(x=10, y=10)

del_btn = ttk.Button(tk, text="Delete Song", command=delete_song)
del_btn.place(x=110, y=10)

search_entry = ttk.Entry(tk)
search_entry.place(x=270, y=10)
search_entry.insert(0, "Search Youtube Songs")
search_entry.bind("<Return>", search_song)

search_btn = ttk.Button(tk, text="Search Online Songs", command=search_song)
search_btn.place(x=440, y=10)

help_btn = ttk.Button(tk, text="Help", command=handle_help)
help_btn.place(x=630, y=10)

song_box = Listbox(tk, fg="#9ad1ec", width=82, height=10, listvariable=StringVar(value=songs),
                   selectmode=SINGLE)
song_box.place(x=10, y=70)
song_box.bind('<Double-1>', play_selected_song)

play_btn = ttk.Button(tk, image=play_img, command=play)
play_btn.place(x=150, y=300)

stop_btn = ttk.Button(tk, image=stop_img, command=stop_song)
stop_btn.place(x=250, y=300)

previous_btn = ttk.Button(tk, image=previous_img, command=previous_song)
previous_btn.place(x=50, y=300)

next_btn = ttk.Button(tk, image=next_img, command=next_song)
next_btn.place(x=350, y=300)

shuffle_btn = ttk.Button(tk, image=shuffle_img, command=shuffle)
shuffle_btn.place(x=450, y=300)

style = ttk.Style().configure("TScale")
time_control = ttk.Scale(tk, from_=0, style="TScale",
                         command=slide, length=350)
time_control.place(x=120, y=270)

current_second_label = ttk.Label(tk, text="00:00")
current_second_label.place(x=70, y=273)

song_length_label = ttk.Label(tk, text="00:00")
song_length_label.place(x=485, y=273)

volume_label = ttk.Label(tk, text="Volume")
volume_label.place(x=620, y=50)

label_0 = ttk.Label(tk, text="0")
label_0.place(x=638, y=68)

label_100 = ttk.Label(tk, text="100")
label_100.place(x=630, y=215)

volume_control = ttk.Scale(tk, from_=0, to=100, style="TScale", orient=VERTICAL, value=50, length=120,
                           command=lambda x: pygame.mixer.music.set_volume(volume_control.get() / 100))
volume_control.place(x=630, y=93)

play_btn.bind("<space>", play)
tk.bind("<Up>", volume)
tk.bind("<Down>", volume)

if __name__ == "__main__":
    tk.mainloop()
