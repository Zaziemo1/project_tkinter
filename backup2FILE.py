import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from pytube import YouTube
import os
import spotipy
import pygame
from spotipy.oauth2 import SpotifyClientCredentials
from pydub import AudioSegment
import requests
from io import BytesIO
from PIL import Image, ImageTk

client_id = "4cc048fb419440f5951860cf0a9f9db0"
client_secret = "763a491995ce4b1cad73ecccd6bb9ade"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def download_Spotifysong(track_uri):
    try:
        track_info = sp.track(track_uri)
        track_name = track_info['name']
        artist_name = track_info['artists'][0]['name']

        preview_url = track_info.get('preview_url')
        if not preview_url:
            raise ValueError("Preview URL not available for the selected track.")

        audio_data = download_Spotifyaudio(preview_url)

        audio_segment = AudioSegment.from_file(BytesIO(audio_data), format="mp3")

        download_path = os.path.expanduser('~') + '/Downloads/'
        mp3_filename = f"{artist_name} - {track_name}.mp3"
        mp3_path = os.path.join(download_path, mp3_filename)
        audio_segment.export(mp3_path, format="mp3")

        messagebox.showinfo("Download Complete", "Song downloaded and converted to MP3 successfully.")
    except Exception as e:
        print(f"Error downloading song: {e}")
        messagebox.showerror("Error", "Unable to download song.")

def download_Spotifyaudio(url):
    try:
        response = requests.get(url)
        return response.content
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None

def download_Youtubevideo():
    url = Youtube_url_entry.get()

    try:
        yt = YouTube(url)
        video_stream = yt.streams.get_highest_resolution()
        video_stream.download()
        messagebox.showinfo('Download Complete', f'Download complete: {yt.title}')
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {str(e)}')

def download_preview(track_url):
    try:
        track_id = track_url.split("/")[-1]
        api_key = 'fc7985f3a217be08d8f0bcfbf5e83802s'
        api_url = f'https://api.deezer.com/track/{track_id}?output=json&apikey={api_key}'

        response = requests.get(api_url)
        data = response.json()

        if 'preview' in data:
            preview_url = data['preview']

            audio_response = requests.get(preview_url)
            with open(f"preview_{track_id}.mp3", 'wb') as audio_file:
                audio_file.write(audio_response.content)

            return f"Preview downloaded successfully as preview_{track_id}.mp3"
        else:
            return "Preview not available for this track."

    except Exception as e:
        return f"An error occurred: {e}"

def download_preview_and_show_message():
    track_url = entryDeezer.get()
    message = download_preview(track_url)
    messagebox.showinfo("Download Status", message)

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
    if file_path:
        file_var.set(file_path)

def play_music():
    file_path = file_var.get()
    if file_path and os.path.exists(file_path):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Error playing music: {e}")

def stop_music():
    pygame.mixer.music.stop()

# Create the main window
root = tk.Tk()
frame2 = tk.Frame()
root.resizable(width=False, height=False)
root.geometry("627x500")
root.title('MP4 & MP3 Downloader')

tabControl = ttk.Notebook(master=root)
hometab = ttk.Frame(tabControl)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tabControl.add(hometab, text='Home')
tabControl.add(tab1, text='Youtuber Video Downloader')
tabControl.add(tab2, text='Spotify MP3 preview Downloader')
tabControl.add(tab3, text='Deezer MP3 preview Downloader')
tabControl.add(tab4, text='Play Music Files')

Youtube_url_label = tk.Label(tab1, text='Enter YouTube URL:')
Youtube_url_label.pack(pady=10)
Youtube_url_entry = tk.Entry(tab1, width=40)
Youtube_url_entry.pack(pady=10)

Spotifyurl_label = tk.Label(tab2, text='Enter Spotify URL:')
Spotifyurl_label.pack(pady=10)
Spotifyurl_entry = tk.Entry(tab2, width=40)
Spotifyurl_entry.pack(pady=10)

tabControl.pack(expand=1, fill="both")

def make_rounded_button(widget):
    widget.config(relief=tk.GROOVE, bd=5, borderwidth=5, highlightthickness=0, bg='#34495e', fg='white')
    widget.update_idletasks()
    widget_height = widget.winfo_height()
    widget_width = widget.winfo_width()
    widget.config(height=widget_height, width=widget_width, borderwidth=0)
    widget.config(highlightthickness=0)
    widget.configure(bg='#3498db')

YTlogo = Image.open(r"afbeeldingen/Youtube_logo.png")
YTlogo = YTlogo.resize((64, 54))
YTlogo = ImageTk.PhotoImage(YTlogo)

SPOTlogo = Image.open(r"afbeeldingen\Spotify_icon.svg.png")
SPOTlogo = SPOTlogo.resize((64, 64))
SPOTlogo = ImageTk.PhotoImage(SPOTlogo)

DEEZERlogo = Image.open(r"afbeeldingen\Deezer_hRGsLeP.png")
DEEZERlogo = DEEZERlogo.resize((64, 34))
DEEZERlogo = ImageTk.PhotoImage(DEEZERlogo)

logoFile = Image.open(r"afbeeldingen\file.png")
logoFile = logoFile.resize((54, 54))
logoFile = ImageTk.PhotoImage(logoFile)

frame1 = tk.Frame(hometab, bg='#3498db')
frame1.grid(row=0, column=0, columnspan=3, pady=10)

title_label = tk.Label(hometab, text='Video/Audio Downloader', font=('Helvetica', 16), fg='black')
title_label.grid(row=0, columnspan=5, pady=20)

def switch_to_tab1():
    tabControl.select(1)

def switch_to_tab2():
    tabControl.select(2)

def switch_to_tab3():
    tabControl.select(3)

def switch_to_tab4():
    tabControl.select(4)

buttonToYoutube = tk.Button(hometab, text="Button 1", image=YTlogo, width=120, command=switch_to_tab1)
buttonToYoutube.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
make_rounded_button(buttonToYoutube)

buttonToSpotify = tk.Button(hometab, text="Button 1", image=SPOTlogo, width=120, command=switch_to_tab2)
buttonToSpotify.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
make_rounded_button(buttonToSpotify)

buttonToDeezer = tk.Button(hometab, text="Button 1", image=DEEZERlogo, width=120, command=switch_to_tab3)
buttonToDeezer.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
make_rounded_button(buttonToDeezer)

buttonToFile = tk.Button(hometab, text="Button 1", image=logoFile, width=120, command=switch_to_tab4)
buttonToFile.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
make_rounded_button(buttonToFile)

for i in range(3):
    hometab.grid_columnconfigure(i, weight=1)

for i in range(3):
    hometab.grid_rowconfigure(i, weight=1)

downloadYoutube_button = tk.Button(tab1, text='Download Video', command=download_Youtubevideo)
downloadYoutube_button.pack(pady=20)

downloadSpotify_button = tk.Button(tab2, text='Download Audio', command=lambda: download_Spotifysong(Spotifyurl_entry.get()))
downloadSpotify_button.pack(pady=20)

labelDeezer = tk.Label(tab3, text="Enter Deezer Track URL:")
labelDeezer.pack(pady=10)

entryDeezer = tk.Entry(tab3, width=50)
entryDeezer.pack(pady=10)

buttonDeezer = tk.Button(tab3, text="Download Preview", command=download_preview_and_show_message)
buttonDeezer.pack(pady=20)

file_var = tk.StringVar()

file_entry4 = tk.Entry(tab4, textvariable=file_var, state='disabled', width=40)
file_entry4.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

browse_button4 = tk.Button(tab4, text="Browse", command=browse_file)
browse_button4.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

playFILE_button = tk.Button(tab4, text="Play", command=play_music)
playFILE_button.grid(row=1, column=0, columnspan=2, pady=10)

stopFILE_button = tk.Button(tab4, text="Stop", command=stop_music)
stopFILE_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
