import datetime
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, ttk
from mutagen.mp3 import MP3
import pygame
from moviepy.editor import *
from pytube import YouTube
from pyyoutube import Api

# <a href="https://www.flaticon.com/free-icons/ui" title="ui icons">Ui icons created by pictranoosa - Flaticon</a>

tk = Tk()
tk.title("Music App")
tk.geometry("600x310")
tk.configure(bg="white")
tk.resizable(False, False)
pygame.mixer.init()
API_KEY = "AIzaSyA82pzJpJMQ9mWS1TrFDRtjGAcw6ZhMCWM"
songs = [file for file in os.listdir("audio")]
songs_path = [os.path.abspath(f"audio/{file}") for file in os.listdir("audio")]
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
        time_control.config(to=song_length, value=current_time)
        if restart:
            play_btn.config(image=pause_img)
        else:
            play_btn.config(image=play_img)
        current_time_converted = datetime.timedelta(seconds=current_time)
        current_second_label.config(text=current_time_converted)
        return
    elif int(time_control.get()) == int(current_time):
        time_control.config(to=song_length, value=current_time)
    else:
        time_control.config(to=song_length, value=time_control.get())
        current_time_converted = datetime.timedelta(seconds=int(time_control.get()))
        current_second_label.config(text=current_time_converted)
        song_length_label.config(text=song_length_converted)
        next_time = time_control.get() + 1
        time_control.config(value=next_time)
    time_control.after(1200, update)


def slide(x):
    try:
        pygame.mixer.music.play(loops=0, start=time_control.get())
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


def add_song_from_yt(youtube_ids):
    global listbox
    for yt_id in youtube_ids:
        yt = YouTube(f"https://www.youtube.com/watch?v={yt_id}")
        itag = yt.streams.filter(only_audio=True)[-1].itag
        yt = yt.streams.get_by_itag(itag)
        yt_song = yt.download()
        # snd = AudioFileClip(yt_song)
        # song_name = f"audio/{os.path.basename(yt_song)[:-4]}.mp3"
        # snd.write_audiofile(filename=song_name)
        songs_path.append(yt_song)
        songs.append(os.path.basename(yt_song))
        # os.remove(yt_song)
    listbox = Listbox(tk, bg="black", fg="#9ad1ec", width=72, height=10, listvariable=StringVar(value=songs),
                      selectmode=SINGLE)
    listbox.select_set(0)
    listbox.place(x=10, y=30)


def handle_add():
    global search_box, yt_window
    selected_songs.append(search_box.curselection())
    yt_window.destroy()
    add_yt_songs()


def open_win(video_list):
    global selected_songs, search_box, yt_window
    selected_songs = []
    yt_window = Toplevel(tk)
    yt_window.geometry("500x200")
    yt_window.title("New Window")
    search_box = Listbox(yt_window, bg="black", fg="#9ad1ec", width=72, height=10,
                         listvariable=StringVar(value=video_list), selectmode=EXTENDED)
    search_box.pack()
    add = Button(yt_window, text="Add Songs", command=handle_add)
    quit = Button(yt_window, text="Quit", command=yt_window.destroy)
    quit.place(x=250, y=170)
    add.place(x=150, y=170)


def search_song(event=None):
    video_list = []
    api = Api(api_key=API_KEY)
    search = api.search_by_keywords(q=search_entry.get(), count=10)
    for video in search.items:
        video_list.append(video.snippet.title)
    open_win(video_list)


def add_yt_songs():
    global selected_songs
    print(selected_songs)
    api = Api(api_key=API_KEY)
    search = api.search_by_keywords(q=search_entry.get(), count=10)
    yt_ids = [search.items[i].id.videoId for i in selected_songs[0]]
    add_song_from_yt(yt_ids)


play_img = ImageTk.PhotoImage(Image.open("img/play.png"))
pause_img = ImageTk.PhotoImage(Image.open("img/pause.png"))
stop_img = ImageTk.PhotoImage(Image.open("img/stop.png"))
previous_img = ImageTk.PhotoImage(Image.open("img/previous.png"))
next_img = ImageTk.PhotoImage(Image.open("img/next.png"))

add_btn = ttk.Button(tk, text="Add song", command=add_song)
add_btn.place(x=10, y=0)

del_btn = ttk.Button(tk, text="Delete song", command=delete_song)
del_btn.place(x=90, y=0)

search_entry = ttk.Entry(tk)
search_entry.place(x=300, y=2)
search_entry.bind("<Return>", search_song)

search_btn = ttk.Button(tk, text="search", command=search_song)
search_btn.place(x=430, y=0)

listbox = Listbox(tk, bg="black", fg="#9ad1ec", width=82, height=10, listvariable=StringVar(value=songs),
                      selectmode=SINGLE)
listbox.place(x=10, y=30)

play_btn = ttk.Button(tk, image=play_img, command=play, style="TButton")
play_btn.place(x=160, y=230)

stop_btn = ttk.Button(tk, image=stop_img, command=stop_song)
stop_btn.place(x=260, y=230)

previous_btn = ttk.Button(tk, image=previous_img, command=previous_song)
previous_btn.place(x=60, y=230)

next_btn = ttk.Button(tk, image=next_img, command=next_song)
next_btn.place(x=360, y=230)



style = ttk.Style().configure("TScale", background="white")
time_control = ttk.Scale(tk, from_=0, style="TScale", command=slide, length=350)
time_control.place(x=50, y=200)

current_second_label = ttk.Label(tk, text="00:00", background="white")
current_second_label.place(x=10, y=203)

song_length_label = ttk.Label(tk, text="00:00", background="white")
song_length_label.place(x=404, y=203)





# VOLUME


volume_label = ttk.Label(tk, text="Volume", background="white")
volume_label.place(x=520, y=0)

label_0 = ttk.Label(tk, text="0", background="white")
label_0.place(x=538, y=20)

label_100 = ttk.Label(tk, text="100", background="white")
label_100.place(x=530, y=180)

volume_control = ttk.Scale(tk, from_=0, to=100, style="TScale", orient=VERTICAL, value=100, length=145,
                           command=lambda x: pygame.mixer.music.set_volume(volume_control.get() / 100))
volume_control.place(x=530, y=35)



tk.mainloop()
