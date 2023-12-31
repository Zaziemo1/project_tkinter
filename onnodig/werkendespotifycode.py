import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pydub import AudioSegment
import tkinter as tk
from tkinter import messagebox
import requests
from io import BytesIO

def download_song(track_uri):
    try:
        track_info = sp.track(track_uri)
        track_name = track_info['name']
        artist_name = track_info['artists'][0]['name']
        
        # Get the preview URL
        preview_url = track_info.get('preview_url')
        if not preview_url:
            raise ValueError("Preview URL not available for the selected track.")
        
        # Download the audio data
        audio_data = download_audio(preview_url)
        
        # Convert to AudioSegment
        audio_segment = AudioSegment.from_file(BytesIO(audio_data), format="mp3")
        
        # Saving the audio segment to an MP3 file
        download_path = os.path.expanduser('~') + '/Downloads/'
        mp3_filename = f"{artist_name} - {track_name}.mp3"
        mp3_path = os.path.join(download_path, mp3_filename)
        audio_segment.export(mp3_path, format="mp3")

        messagebox.showinfo("Download Complete", "Song downloaded and converted to MP3 successfully.")
    except Exception as e:
        print(f"Error downloading song: {e}")
        messagebox.showerror("Error", "Unable to download song.")

def download_audio(url):
    try:
        response = requests.get(url)
        return response.content
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None

# Spotify API credentials
client_id = "4cc048fb419440f5951860cf0a9f9db0"
client_secret = "763a491995ce4b1cad73ecccd6bb9ade"

# Spotify API authentication
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Create the main window
window = tk.Tk()
window.title("Song Downloader")

# Create and place widgets
url_label = tk.Label(window, text="Enter Spotify Track URI:")
url_label.pack(pady=10)

url_entry = tk.Entry(window, width=40)
url_entry.pack(pady=10)

download_button = tk.Button(window, text="Download", command=lambda: download_song(url_entry.get()))
download_button.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()
