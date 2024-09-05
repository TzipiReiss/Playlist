import os
import re
import pygame
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from mutagen.mp3 import MP3


class PlaylistPlayer:
    def __init__(self, directory):
        self.directory = directory
        self.playlist = self.load_songs()
        self.playing = False
        self.paused = False
        self.current_song_index = -1
        self.current_song = None
        self.loop = False
        self.shuffle = False
        self.song_length = 0  # Store song length
        pygame.mixer.init()  # Initialize the mixer for pygame

    def load_songs(self):
        playlist = []
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.lower().endswith('.mp3'):
                    playlist.append(os.path.join(root, file))
        return playlist

    def get_folder_name(self, file_path):
        return os.path.basename(os.path.dirname(file_path))

    def get_song_name(self, file_path):
        file_name = os.path.basename(file_path)
        song_name = os.path.splitext(file_name)[0]
        return re.sub(r'\d+', '', song_name).strip()

    def play_song(self, song_path):
        self.current_song = song_path
        print("Now playing: " + self.get_song_name(song_path))

        # Get the song length using mutagen
        audio = MP3(song_path)
        self.song_length = audio.info.length  # Length of the song in seconds

        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Event triggered when the song ends

    def play_next(self):
        if not self.playing:
            return
        self.current_song_index += 1
        if self.current_song_index < len(self.playlist):
            song_path = self.playlist[self.current_song_index]
            self.play_song(song_path)
        else:
            print("No more songs in the playlist.")

    def play_previous(self):
        if not self.playing:
            return
        self.current_song_index -= 1
        if self.current_song_index >= 0:
            song_path = self.playlist[self.current_song_index]
            self.play_song(song_path)
        else:
            print("No previous song.")

    def play(self):
        if not self.playing:
            self.playing = True
            if self.current_song_index == -1 and self.playlist:
                self.current_song_index = 0
            if self.current_song_index >= 0:
                song_path = self.playlist[self.current_song_index]
                self.play_song(song_path)
        elif self.paused:
            pygame.mixer.music.unpause()
            self.paused = False

    def pause(self):
        pygame.mixer.music.pause()
        self.paused = True

    def stop(self):
        self.playing = False
        pygame.mixer.music.stop()
        print("Playback stopped.")
        self.current_song = None  # Reset current song when stopped

    def replay(self):
        if self.current_song:
            self.play_song(self.current_song)

    def toggle_loop(self):
        self.loop = not self.loop
        print(f"Loop {'enabled' if self.loop else 'disabled'}.")

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle
        print(f"Shuffle {'enabled' if self.shuffle else 'disabled'}.")

    def get_current_folder(self):
        return self.get_folder_name(self.current_song) if self.current_song else "None"

    def get_current_song(self):
        return self.get_song_name(self.current_song) if self.current_song else "None"

    def reset_playlist(self):
        self.current_song_index = -1
        if self.playlist:
            self.play_next()


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Playlist Player")

        self.player = None

        # Load directory button
        self.load_button = tk.Button(self.root, text="Load Directory", command=self.load_directory)
        self.load_button.pack(pady=10)

        # Play button
        self.play_button = tk.Button(self.root, text="Play", command=self.play)
        self.play_button.pack(pady=10)

        # Pause button
        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause)
        self.pause_button.pack(pady=10)

        # Stop button
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop)
        self.stop_button.pack(pady=10)

        # Replay button
        self.replay_button = tk.Button(self.root, text="Replay", command=self.replay)
        self.replay_button.pack(pady=10)

        # Next button
        self.next_button = tk.Button(self.root, text="Next", command=self.next_song)
        self.next_button.pack(pady=10)

        # Previous button
        self.previous_button = tk.Button(self.root, text="Previous", command=self.previous_song)
        self.previous_button.pack(pady=10)

        # Loop button
        self.loop_button = tk.Button(self.root, text="Loop", command=self.toggle_loop)
        self.loop_button.pack(pady=10)

        # Shuffle button
        self.shuffle_button = tk.Button(self.root, text="Shuffle", command=self.toggle_shuffle)
        self.shuffle_button.pack(pady=10)

        # Folder label
        self.folder_label = tk.Label(self.root, text="Current Folder: None")
        self.folder_label.pack(pady=5)

        # Song label
        self.song_label = tk.Label(self.root, text="Current Song: None")
        self.song_label.pack(pady=5)

        # Progress bar
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=10)

        self.update_labels()
        self.update_progress()

    def load_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.player = PlaylistPlayer(directory)
            self.player.reset_playlist()
            self.update_labels()

    def play(self):
        if self.player:
            self.player.play()

    def pause(self):
        if self.player:
            self.player.pause()

    def stop(self):
        if self.player:
            self.player.stop()
            self.update_labels()

    def replay(self):
        if self.player:
            self.player.replay()
            self.update_labels()

    def next_song(self):
        if self.player:
            self.player.play_next()
            self.update_labels()

    def previous_song(self):
        if self.player:
            self.player.play_previous()
            self.update_labels()

    def toggle_loop(self):
        if self.player:
            self.player.toggle_loop()

    def toggle_shuffle(self):
        if self.player:
            self.player.toggle_shuffle()

    def update_labels(self):
        if self.player:
            self.folder_label.config(text="Current Folder: " + self.player.get_current_folder())
            self.song_label.config(text="Current Song: " + self.player.get_current_song())
        self.root.after(1000, self.update_labels)  # Update every second

    def update_progress(self):
        if self.player and self.player.playing:
            current_position = pygame.mixer.music.get_pos() / 1000  # Get position in seconds
            if self.player.song_length > 0:  # Check if the song length is available
                self.progress_bar["value"] = (current_position / self.player.song_length) * 100
        self.root.after(1000, self.update_progress)

    def run(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    gui = GUI(root)
    try:
        gui.run()
    except KeyboardInterrupt:
        print("\nStopping playback...")
        if gui.player:
            gui.player.stop()


if __name__ == "__main__":
    main()
