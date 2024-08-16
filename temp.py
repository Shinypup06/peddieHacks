import tkinter as tk
from tkinter import filedialog
import pygame

# Initialize Pygame mixer
pygame.mixer.init()

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
    if file_path:
        pygame.mixer.music.load(file_path)
        play_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.NORMAL)

def play_audio():
    pygame.mixer.music.play()

def stop_audio():
    pygame.mixer.music.stop()

# Create the main window
root = tk.Tk()
root.title("Audio Player")

# Create and place buttons
load_button = tk.Button(root, text="Load", command=load_file)
load_button.pack(pady=5)

play_button = tk.Button(root, text="Play", command=play_audio, state=tk.DISABLED)
play_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop", command=stop_audio, state=tk.DISABLED)
stop_button.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()