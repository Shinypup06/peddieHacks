import tkinter as tk
import customtkinter
from tkinter import font
from PIL import Image, ImageTk
from tkinter import filedialog
import threading
import pygame
import subprocess, multiprocessing
from comparer import *
from splitter import *
from sound import *
from record import *
from lyrics import *

#COLORS
LIGHT_PURPLE = "#bfc0e2"
DARK_PURPLE = "#674188"
MED_PURPLE = "#9581c7"
WHITE = "#f7f7ff"
BLACK = "#000000"

def openWelcomeScreen():
    welcomeFrame.lift()

def openRecordScreen():
    recordFrame.lift()
    
def openAnalyzeScreen():
    analyzeFrame.lift()

def getGeneratedLyrics():
    print("test")

def uploadOriginalSong():
    global input1, name
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        # Extract and display file name
        file_name = file_path.split("/")[-1]  # For Unix-like paths
        input1 = file_path
        global fileLabel
        name = file_name[:-4]
        fileLabel.config(text=f"File 1: {file_name}")
        print(f"Input1: {input1}")
        print(f"fileName: {name}")

        #TODO: uncomment this
        # Split audio and get lyrics in a separate thread to prevent GUI freezing
        threading.Thread(target=processOriginalSong).start()

def processOriginalSong():
    loading_text.config(text="loading...")
    global lyrics
    
    separate_audio(input1,'output/')
    print("done separating audio")

    generateLyricsButton.configure(state="normal")
    startRecordingButton.configure(state="normal")
    loading_text.config(text="")

def enableRecordingPlayback():

        for widget in playFrame.winfo_children():
            widget.grid_forget()  # Hide existing buttons

        # Create 2 square buttons
        button1 = customtkinter.CTkButton(
            playFrame, 
            text="▶", 
            command=lambda: play_file("output.wav"), 
            width=80, 
            height=80, 
            corner_radius=50, 
            border_color=MED_PURPLE,
            border_spacing=10,
            border_width=3,
            hover_color=LIGHT_PURPLE,
            font=BUTTON_FONT, 
            fg_color=WHITE, 
            text_color=DARK_PURPLE)
        button1.grid(row=4, column=1, padx=10, pady=5)

        button2 = customtkinter.CTkButton(
            playFrame, 
            text="■", 
            command=lambda: stop_playback(), 
            width=80, 
            height=80, 
            corner_radius=50, 
            border_color=MED_PURPLE,
            border_spacing=10,
            border_width=3,
            hover_color=LIGHT_PURPLE,
            font=BUTTON_FONT, 
            fg_color=WHITE, 
            text_color=DARK_PURPLE)
        button2.grid(row=4, column=2, padx=10, pady=5)

        # Enable the Save and Analyze button
        saveAnalyzeButton.configure(state="normal")

def getGeneratedLyrics():
    loading_text.config(text="loading...")
    threading.Thread(target=generateLyrics).start()

def generateLyrics():
    global lyrics
    lyrics = getLyrics("output/" + name + "/vocals.wav")

    # Insert generated lyrics into the lyrics box
    lyricsBox.delete('1.0', tk.END)
    lyricsBox.insert(tk.END, lyrics)
    loading_text.config(text="")

def searchLyrics():
    loading_text.config(text="loading...")
    global lyrics
    artist = artist_entry.get()
    title = song_entry.get()

    lyrics = getInternetLyrics(artist, title)

    # Insert generated lyrics into the lyrics box
    lyricsBox.delete('1.0', tk.END)
    lyricsBox.insert(tk.END, lyrics)

    startRecordingButton.configure(state="normal")  # Enable the Rec/Play button
    loading_text.config(text="")

if __name__ == "__main__":

    # use pygame mixer for sound playback
    pygame.init()
    pygame.mixer.init()

    # Default leaderboard data
    current_entries = []
    leaderboard_text = ""

    # Define root window
    root = tk.Tk()

    #FONTS
    TITLE_FONT = font.Font(family="Fredoka Semibold", size=30)
    HEADER_FONT = font.Font(family="Fredoka Semibold", size=25)
    NORMAL_FONT = font.Font(family="Rubik Light", size=20)

    BUTTON_FONT= customtkinter.CTkFont(family='Fredoka', size=30)
    CUSTOM_FONT= customtkinter.CTkFont(family='Rubik Light', size=20)


    #ANALYZE SCREEN
    analyzeFrame=tk.Frame(root, bg=LIGHT_PURPLE)
    analyzeFrame.place(
        relx=0, 
        rely=0.06, 
        relwidth=1, 
        relheight=0.94)

    analyze_label = tk.Label(
        analyzeFrame,
        text="Please upload the WAV files below:",
        font=HEADER_FONT,
        bg=LIGHT_PURPLE,
        fg=DARK_PURPLE)

    analyze_label.place(
        relx=0.5,
        rely=0.38,
        anchor="center")

    #Background images

    topImage = ImageTk.PhotoImage(Image.open("images/top.png"))
    topImageLabel = tk.Label(analyzeFrame, image=topImage, bg=LIGHT_PURPLE)
    topImageLabel.place(relx=0.5, rely=0.19, anchor="center")

    frogImage = ImageTk.PhotoImage(Image.open("images/plain.png"))
    frogImageLabel = tk.Label(analyzeFrame, image=frogImage, bg=LIGHT_PURPLE)
    frogImageLabel.place(relx=0.5, rely=0.56, anchor="center")

    #File1 Button

    analyze_frame = tk.Frame(analyzeFrame, bg=LIGHT_PURPLE)
    analyze_frame.place(
        relx=0.3,
        rely= 0.55,
        anchor="center")

    file1_button = customtkinter.CTkButton(
        analyze_frame,
        text="Upload",
        command=uploadOriginalSong,
        width=250,
        height=80,
        corner_radius=50,
        border_color=WHITE,
        border_spacing=10,
        border_width=3,
        hover_color=MED_PURPLE,
        font=BUTTON_FONT,
        fg_color=DARK_PURPLE,
        text_color=WHITE)
    file1_button.pack()

    record_label = tk.Label(
        analyze_frame,
        text="File 1: FILENAME",
        font=NORMAL_FONT,
        bg=LIGHT_PURPLE,
        fg=DARK_PURPLE)
    record_label.pack(pady=10)

    #File2 Button
    analyze_frame = tk.Frame(analyzeFrame, bg=LIGHT_PURPLE)
    analyze_frame.place(
        relx=0.7,
        rely= 0.55,
        anchor="center")


    file2_button = customtkinter.CTkButton(
        analyze_frame,
        text="Upload",
        command=uploadOriginalSong,
        width=250,
        height=80,
        corner_radius=50,
        border_color=WHITE,
        border_spacing=10,
        border_width=3,
        hover_color=MED_PURPLE,
        font=BUTTON_FONT,
        fg_color=DARK_PURPLE,
        text_color=WHITE)
    file2_button.pack()

    analyze_label = tk.Label(
        analyze_frame,
        text="File 2: FILENAME",
        font=NORMAL_FONT,
        bg=LIGHT_PURPLE,
        fg=DARK_PURPLE)
    analyze_label.pack(pady=10)

    #Run Button
    uploadOriginalButton = customtkinter.CTkButton(
        analyzeFrame,
        text="Run",
        #command=loadingScreen,
        width=350,
        height=60,
        corner_radius=50,
        border_color=MED_PURPLE,
        border_spacing=10,
        border_width=3,
        hover_color=LIGHT_PURPLE,
        font=BUTTON_FONT,
        fg_color=WHITE,
        text_color=DARK_PURPLE)
    uploadOriginalButton.place(relx=0.5, rely=0.7, anchor="n")

    #Back button
    backButton = customtkinter.CTkButton(
        analyzeFrame,
        text="Back",
        command=openWelcomeScreen,
        width=300,
        height=80,
        corner_radius=50,
        border_color=WHITE,
        border_spacing=10,
        border_width=3,
        hover_color=MED_PURPLE,
        font=BUTTON_FONT,
        fg_color=DARK_PURPLE,
        text_color=WHITE)
    backButton.place(relx=0.15, rely=0.8, anchor="n")

    #RECORD SCREEN
    recordFrame=tk.Frame(root, bg=LIGHT_PURPLE)
    recordFrame.place(
        relx=0, 
        rely=0.06, 
        relwidth=1, 
        relheight=0.94)

    recordInstructions = tk.Label(
        recordFrame, 
        text="Please upload a WAV file of\nthe original song below:",
        font=HEADER_FONT,
        bg=LIGHT_PURPLE, 
        fg=DARK_PURPLE)
    recordInstructions.place(
        relx=0.2, 
        rely=0.15, 
        anchor="center")

    # Button to upload the original song
    uploadOriginalButton = customtkinter.CTkButton(
        recordFrame, 
        text="Upload Original Song", 
        command=uploadOriginalSong, 
        width=350, 
        height=60, 
        corner_radius=50, 
        border_color=MED_PURPLE,
        border_spacing=10,
        border_width=3,
        hover_color=LIGHT_PURPLE,
        font=BUTTON_FONT, 
        fg_color=WHITE, 
        text_color=DARK_PURPLE)
    uploadOriginalButton.place(relx=0.2, rely=0.25, anchor="n")

    # Display filename of uploaded file
    fileLabel = tk.Label(recordFrame, text="File: None", font=NORMAL_FONT, bg=LIGHT_PURPLE, fg=DARK_PURPLE)
    fileLabel.place(relx=0.2, rely=0.33, anchor="n") 

    # Button to start recording
    startRecordingButton = customtkinter.CTkButton(
        recordFrame, 
        text="Start Recording", 
        command= lambda: startRecording(name, "output.wav", enableRecordingPlayback, input1, lambda: deleteRecordingButton.configure(state="normal")), 
        width=350, 
        height=60, 
        corner_radius=50, 
        border_color=MED_PURPLE,
        border_spacing=10,
        border_width=3,
        hover_color=LIGHT_PURPLE,
        font=BUTTON_FONT, 
        fg_color=WHITE, 
        text_color=DARK_PURPLE,
        state="disabled")
    startRecordingButton.place(relx=0.2, rely=0.4, anchor="n") 

    # Button to stop recording
    deleteRecordingButton = customtkinter.CTkButton(
        recordFrame, 
        text="Delete Recording", 
        command=lambda: stop_rec(),
        width=350, 
        height=60, 
        corner_radius=50, 
        border_color=MED_PURPLE,
        border_spacing=10,
        border_width=3,
        hover_color=LIGHT_PURPLE,
        font=BUTTON_FONT, 
        fg_color=WHITE, 
        text_color=DARK_PURPLE,
        state="disabled")
    deleteRecordingButton.place(relx=0.2, rely=0.5, anchor="n")

    # Frame for the play and pause buttons for playback
    playFrame = tk.Frame(recordFrame, bg="#bfc0e2")
    playFrame.place(relx=0.2, rely=0.6, anchor="n")

    # loading text for processing time
    loading_text = tk.Label(recordFrame, text="", font=NORMAL_FONT, bg=LIGHT_PURPLE, fg=DARK_PURPLE)
    loading_text.place(relx=0.2, rely=0.75, anchor="n")

    #Generate AI lyrics
    generateLyricsButton = customtkinter.CTkButton(
        recordFrame, 
        text="Generate Lyrics", 
        command=getGeneratedLyrics, 
        width=250, 
        height=60, 
        corner_radius=50, 
        border_color=WHITE,
        border_spacing=10,
        border_width=3,
        hover_color=MED_PURPLE,
        font=BUTTON_FONT, 
        fg_color=DARK_PURPLE, 
        text_color=WHITE,
        state="disabled")
    generateLyricsButton.place(
        relx=0.85,
        rely=0.15,
        anchor="center"
    )

    # Lyrics box
    lyricsBox = customtkinter.CTkTextbox(
        recordFrame, 
        wrap='word', 
        height=450, 
        width=500, 
        font=CUSTOM_FONT, 
        fg_color=WHITE,
        text_color=BLACK,
        corner_radius=30,
        border_width=3,
        border_color=DARK_PURPLE)
    lyricsBox.place(relx=0.55, rely=0.07, anchor="n")
    lyricsBox.insert(tk.END, "Your lyrics will show up here! Search for your song below, or upload an audio file and generate lyrics using AI. If you really want, you could type them out yourself.")

    # Song input
    label_song = tk.Label(recordFrame, text="Song:", font=HEADER_FONT, bg=LIGHT_PURPLE, fg=DARK_PURPLE)
    label_song.place(relx=0.55, rely=0.65, anchor="n")
    song_entry = customtkinter.CTkEntry(
        recordFrame, 
        font=BUTTON_FONT, 
        width=400, 
        fg_color=WHITE, 
        text_color=BLACK)
    song_entry.place(relx=0.55, rely= 0.7, anchor="n")

    # Artist input
    label_artist = tk.Label(recordFrame, text="Artist:", font=HEADER_FONT, bg=LIGHT_PURPLE, fg=DARK_PURPLE)
    label_artist.place(relx=0.55, rely= 0.77, anchor="n")
    artist_entry = customtkinter.CTkEntry(
        recordFrame, 
        font=BUTTON_FONT, 
        width=400, 
        fg_color=WHITE, 
        text_color=BLACK)
    artist_entry.place(relx=0.55, rely= 0.82, anchor="n")

    searchLyricsButton = customtkinter.CTkButton(
        recordFrame, 
        text="Search Lyrics", 
        command=searchLyrics, 
        width=250, 
        height=60, 
        corner_radius=50, 
        border_color=WHITE,
        border_spacing=10,
        border_width=3,
        hover_color=MED_PURPLE,
        font=BUTTON_FONT, 
        fg_color=DARK_PURPLE, 
        text_color=WHITE)
    searchLyricsButton.place(relx=0.55, rely= 0.9, anchor="n")

    backButton = customtkinter.CTkButton(
        recordFrame, 
        text="Back", 
        command=openWelcomeScreen, 
        width=300, 
        height=80, 
        corner_radius=50, 
        border_color=WHITE,
        border_spacing=10,
        border_width=3,
        hover_color=MED_PURPLE,
        font=BUTTON_FONT, 
        fg_color=DARK_PURPLE, 
        text_color=WHITE)
    backButton.place(relx=0.15, rely=0.8, anchor="n")

    saveAnalyzeButton = customtkinter.CTkButton(
        recordFrame, 
        text="Analyze Recording", 
        # command=showLoadingWindow2, 
        width=300, 
        height=80, 
        corner_radius=50, 
        border_color=WHITE,
        border_spacing=10,
        border_width=3,
        hover_color=MED_PURPLE,
        font=BUTTON_FONT, 
        fg_color=DARK_PURPLE, 
        text_color=WHITE,
        state="disabled")
    saveAnalyzeButton.place(relx=0.85, rely=0.8, anchor="n")

    #FROG images
    headphonesImage = ImageTk.PhotoImage(Image.open("images/headphones.png"))
    headphonesLabel = tk.Label(recordFrame, image=headphonesImage, bg=LIGHT_PURPLE)
    headphonesLabel.place(relx=0.86, rely=0.5, anchor="center")




    #WELCOME SCREEN
    welcomeFrame=tk.Frame(root, bg=LIGHT_PURPLE)
    welcomeFrame.place(
        relx=0, 
        rely=0.06, 
        relwidth=1, 
        relheight=0.94)


    welcome_label = tk.Label(
        welcomeFrame, 
        text="Select one of the two options to evaluate your singing skills!", 
        font=HEADER_FONT, 
        bg=LIGHT_PURPLE, 
        fg=DARK_PURPLE)

    welcome_label.place(
        relx=0.5, 
        rely=0.38, 
        anchor="center")

    #Background images
    musicStaffImage = ImageTk.PhotoImage(Image.open("images/top.png"))
    musicStaffLabel = tk.Label(welcomeFrame, image=musicStaffImage, bg=LIGHT_PURPLE)
    musicStaffLabel.place(relx=0, rely=0.75)

    frogWelcomeImage = ImageTk.PhotoImage(Image.open("images/frogWelcome.png"))
    frogWelcomeLabel = tk.Label(welcomeFrame, image=frogWelcomeImage, bg=LIGHT_PURPLE)
    frogWelcomeLabel.place(relx=0.5, rely=0.19, anchor="center")

    #Record Button
    record_frame = tk.Frame(welcomeFrame, bg=LIGHT_PURPLE)
    record_frame.place(
        relx=0.3, 
        rely= 0.55, 
        anchor="center")

    record_label = tk.Label(
        record_frame, 
        text="Upload a WAV file of any song &\nRecord your singing with an\nautomatically generated backtrack", 
        font=NORMAL_FONT, 
        bg=LIGHT_PURPLE, 
        fg=DARK_PURPLE)
    record_label.pack(pady=10)

    record_button = customtkinter.CTkButton(
        record_frame, 
        text="Record", 
        command=openRecordScreen, 
        width=250, 
        height=80, 
        corner_radius=50, 
        border_color=WHITE,
        border_spacing=10,
        border_width=3,
        hover_color=MED_PURPLE,
        font=BUTTON_FONT, 
        fg_color=DARK_PURPLE, 
        text_color=WHITE)
    record_button.pack()

    #Analyze Button
    analyze_frame = tk.Frame(welcomeFrame, bg=LIGHT_PURPLE)
    analyze_frame.place(
        relx=0.7, 
        rely= 0.55,
        anchor="center")

    analyze_label = tk.Label(
        analyze_frame, 
        text="Have a recording of your singing?\nUpload the original song and\nyour recording as WAV files", 
        font=NORMAL_FONT, 
        bg=LIGHT_PURPLE, 
        fg=DARK_PURPLE)
    analyze_label.pack(pady=10)

    analyze_button = customtkinter.CTkButton(
        analyze_frame, 
        text="Analyze", 
        command=openAnalyzeScreen, 
        width=250, 
        height=80, 
        corner_radius=50, 
        border_color=WHITE,
        border_spacing=10,
        border_width=3,
        hover_color=MED_PURPLE,
        font=BUTTON_FONT, 
        fg_color=DARK_PURPLE, 
        text_color=WHITE)
    analyze_button.pack()


    # KARACROAKIE HEADER
    headerBar=tk.Frame(root, bg=DARK_PURPLE)
    headerBar.place(relx=0, rely=0, relwidth=1, relheight=0.06)
    header_label = tk.Label(headerBar, text="Karacroakie", font=TITLE_FONT, bg=DARK_PURPLE, fg="#F7EFE5")
    header_label.pack(pady=10)


    # Update GUI
    root.title("Karacroakie")
    root.geometry("1920x1080")
    root.configure(bg=LIGHT_PURPLE)
    root.update()
    root.mainloop()