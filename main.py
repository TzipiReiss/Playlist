import os
import re

from playsound import playsound

def get_song_name(file_path):
    file_name = os.path.basename(file_path)
    song_name = os.path.splitext(file_name)[0]
    song_name_without_numbers = re.sub(r'\d+', '', song_name).strip()
    return song_name_without_numbers

# Set the path to the directory containing your songs
songs_directory = r'D:\\Users\\Music\\נמואל הרוש\\נמואל הרוש - אלף'

song_files = os.listdir(songs_directory)

playlist = []

for song_file in song_files:
    song_path = os.path.join(songs_directory, song_file)
    playlist.append(song_path)

# Loop through the playlist and play each song
for song_path in playlist:
    print("מנגן כעת: "+ get_song_name(song_path))
    playsound(song_path)