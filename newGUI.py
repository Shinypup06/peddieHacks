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

# initialize input files
input1 = ""
input2 = ""
name = ""
score = 0.0


def openWelcomeScreen():
    global input1, input2, name, score, runButton
    input1=""
    input2=""
    name=""
    score=0


    



    welcomeFrame.lift()

def openRecordScreen():
    global fileLabel, input1
    input1=""
    startRecordingButton.configure(state="disabled")
    deleteRecordingButton.configure(state="disabled")
    generateLyricsButton.configure(state="disabled")
    saveAnalyzeButton.configure(state="disabled")
    lyricsBox.delete(1.0, tk.END)
    lyricsBox.insert(tk.END, "Your lyrics will show up here! Search for your song below, or upload an audio file and generate lyrics using AI. If you really want, you could type them out yourself.")
    hideButtons(playFrame)
    fileLabel.configure(text="File 1:")
    recordFrame.lift()
    
def openAnalyzeScreen():
    global runButton, file1_label, file2_label

    hideButtons(file1_buttons_frame)
    hideButtons(file2_buttons_frame)
    runButton.configure(state="disabled")
    file1_label.configure(text="File 1:")
    file1_label.configure(text="File 2:")

    analyzeFrame.lift()

def openLeaderBoard():
    global singer_entry, addEntryButton, label_artist1, label_score
    singer_entry.configure(state="normal")
    addEntryButton.configure(state="normal")
    # Artist
    label_artist1 = tk.Label(leaderboardFrame, text=f"Song: {name}", font=HEADER_FONT, bg=LIGHT_PURPLE, fg=DARK_PURPLE)
    label_artist1.place(relx=0.25, rely= 0.37, anchor="n")
    # Score
    label_score = tk.Label(leaderboardFrame, text=f"Score: {score}", font=HEADER_FONT, bg=LIGHT_PURPLE, fg=DARK_PURPLE)
    label_score.place(relx=0.25, rely= 0.49, anchor="n")
    leaderboardFrame.lift()

def add_to_leaderboard(entry_name, leaderboard):
    global name
    singer = entry_name.get()

    if singer and score >= 0:
        # Current entires is a list of tuples with (score, name)
        global current_entries

        # Add the new score and name to the list
        current_entries.append((score, singer, name))

        # Sort the list by score in descending order
        current_entries.sort(reverse=True, key=lambda x: x[0])

        # Clear the leaderboard and insert sorted entries
        leaderboard.delete(0, tk.END)
        for entry in current_entries:
            leaderboard.insert(tk.END, f"{entry[1]}: {entry[0]:.2f} -- {name}")

        # Clear the input fields after adding to the leaderboard
        entry_name.delete(0, tk.END)
        addEntryButton.configure(state="disabled")

def loadUploaded():
    loadingFrame.lift()
    threading.Thread(target=analyzeAudio).start()

def splitAudio(input, output):
    subprocess.run(["python", "splitter.py", input, output])

def analyzeAudio():
    global score

    print("Original Vocals: " + "output/" + name + "/vocals.wav")
    print("Recorded Vocals: " + input2)

    # Create a new process for Spleeter
    spleeter_process = multiprocessing.Process(target=splitAudio, args=(input1, "output/"))
    print("Running Spleeter...")
    spleeter_process.start()

    # Wait for the Spleeter process to finish
    spleeter_process.join()

    score = scaleToScore(compareaudios("output/" + name + "/vocals.wav", input2))

    global score_label
    score_label.config(text=f"{score}%")
    resultsFrame.lift()

def loadRecorded():
    loadingFrame.lift()
    # Run the long task in a separate thread to prevent GUI freezing
    threading.Thread(target=analyzeRecordedAudio).start()

def analyzeRecordedAudio():
    global score
    score = scaleToScore(compareaudios("output/" + name + "/vocals.wav", "output.wav"))
    global score_label
    score_label.config(text=f"{score}%")
    resultsFrame.lift()

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

    loading_text.config(text="")

def upload_file1():
    global input1, name
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        # Extract and display file name
        file_name = file_path.split("/")[-1]  # For Unix-like paths
        input1 = file_path
        global file1_label
        file1_label.config(text=f"File 1: {file_name}")
        name = file_name[:-4]
        print(f"Input1: {input1}")
        show_buttons1(file1_buttons_frame)
        update_run_button_state()

def upload_file2():
    global input2
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        # Extract and display file name
        file_name = file_path.split("/")[-1]  # For Unix-like paths
        input2 = file_path
        global file2_label
        file2_label.config(text=f"File 2: {file_name}")
        print(f"Input2: {input2}")
        show_buttons2(file2_buttons_frame)
        update_run_button_state()

def show_buttons1(frame):
    hideButtons(frame)
    # Create 2 square buttons

    button1 = tk.Button(frame, text="▶", width=3, height=0, font=("Verdana", 20), bg="#674188",
                       fg="#F7EFE5", command=lambda: play_file(input1))
    button1.grid(row=0, column=1, padx=10, pady=5)

    button2 = tk.Button(frame, text="■", width=3, height=0, font=("Verdana", 20), bg="#674188",
                       fg="#F7EFE5", command=lambda: stop_playback())
    button2.grid(row=0, column=2, padx=10, pady=5)

def show_buttons2(frame):
    hideButtons(frame)
    # Create 2 square buttons

    button1 = tk.Button(frame, text="▶", width=3, height=0, font=("Verdana", 20), bg="#674188",
                       fg="#F7EFE5", command=lambda: play_file(input2))
    button1.grid(row=0, column=1, padx=10, pady=5)

    button2 = tk.Button(frame, text="■", width=3, height=0, font=("Verdana", 20), bg="#674188",
                       fg="#F7EFE5", command=lambda: stop_playback())
    button2.grid(row=0, column=2, padx=10, pady=5)

def hideButtons(frame):
    for widget in frame.winfo_children():
        widget.grid_forget()  # Hide existing buttons

def update_run_button_state():
    if len(input1)>1 and len(input2)>1:
        runButton.configure(state="normal")  # Enable the Run button
    else:
        runButton.configure(state="disabled")  # Disable the Run button


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

    #LEADERBOARD SCREEN
    leaderboardFrame=tk.Frame(root, bg=LIGHT_PURPLE)
    leaderboardFrame.place(
        relx=0, 
        rely=0.06, 
        relwidth=1, 
        relheight=0.94)
    
    # Name input
    label_singer = tk.Label(leaderboardFrame, text="Singer:", font=HEADER_FONT, bg=LIGHT_PURPLE, fg=DARK_PURPLE)
    label_singer.place(relx=0.25, rely=0.25, anchor="n")
    singer_entry = customtkinter.CTkEntry(
        leaderboardFrame, 
        font=BUTTON_FONT, 
        width=400, 
        fg_color=WHITE, 
        text_color=BLACK)
    singer_entry.place(relx=0.25, rely= 0.3, anchor="n")

    # Artist
    label_artist1 = tk.Label(leaderboardFrame, text=f"Song:{name}", font=HEADER_FONT, bg=LIGHT_PURPLE, fg=DARK_PURPLE)
    label_artist1.place(relx=0.25, rely= 0.37, anchor="n")


    # Score
    label_score = tk.Label(leaderboardFrame, text=f"Score:{score}", font=HEADER_FONT, bg=LIGHT_PURPLE, fg=DARK_PURPLE)
    label_score.place(relx=0.25, rely= 0.49, anchor="n")

    addEntryButton = customtkinter.CTkButton(
        leaderboardFrame, 
        text="Save", 
        command=lambda: add_to_leaderboard(singer_entry, leaderboard), 
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
    addEntryButton.place(relx=0.25, rely= 0.62, anchor="n")

    # Create the leaderboard listbox in the frame_leaderboard
    frame_leaderboard = tk.Frame(leaderboardFrame, bg="#bfc0e2")
    frame_leaderboard.place(relx=0.65, rely=0.5, anchor="center")

    tk.Label(frame_leaderboard, text="Leaderboard:", font=("Verdana", 24), bg="#bfc0e2", fg="#0a0b40").place(relx=0.65, rely=0.2, anchor="center")
    leaderboard = tk.Listbox(frame_leaderboard, width=40, height=15, font=("Verdana", 18), bg="#F7EFE5", fg="#674188")
    leaderboard.pack()


    #back buttons
    backHomeButton = customtkinter.CTkButton(
        leaderboardFrame,
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
    backHomeButton.place(relx=0.15, rely=0.8, anchor="n")


    #RESULTS SCREEN
    resultsFrame=tk.Frame(root, bg=LIGHT_PURPLE)
    resultsFrame.place(
        relx=0, 
        rely=0.06, 
        relwidth=1, 
        relheight=0.94)
    
    results_label = tk.Label(resultsFrame, text=f"Your Pitch Accuracy Score:", font=HEADER_FONT,
                             bg=LIGHT_PURPLE, fg=DARK_PURPLE)
    results_label.place(relx=0.5, rely=0.3, anchor="center")

    score_label = tk.Label(resultsFrame, text="", font=TITLE_FONT,
                             bg=LIGHT_PURPLE, fg=DARK_PURPLE)
    score_label.place(relx=0.5, rely=0.4, anchor="center")

    backHomeButton = customtkinter.CTkButton(
        resultsFrame,
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
    backHomeButton.place(relx=0.15, rely=0.8, anchor="n")

    saveResultsButton = customtkinter.CTkButton(
        resultsFrame,
        text="Save Results",
        command=openLeaderBoard,
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
    saveResultsButton.place(relx=0.85, rely=0.8, anchor="n")

    #LOADING SCREEN
    loadingFrame=tk.Frame(root, bg=LIGHT_PURPLE)
    loadingFrame.place(
        relx=0, 
        rely=0.06, 
        relwidth=1, 
        relheight=0.94)
    loading_label = tk.Label(
        loadingFrame, 
        text="Processing your files, please wait...", 
        font=HEADER_FONT,
        bg=LIGHT_PURPLE, 
        fg=DARK_PURPLE)
    loading_label.place(relx=0.5, rely=0.5, anchor="s")

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

    plainFrogImage = ImageTk.PhotoImage(Image.open("images/plain.png"))
    plainFrogImageLabel = tk.Label(analyzeFrame, image=plainFrogImage, bg=LIGHT_PURPLE)
    plainFrogImageLabel.place(relx=0.5, rely=0.56, anchor="center")

    #File1 Button
    file1_frame = tk.Frame(analyzeFrame, bg=LIGHT_PURPLE)
    file1_frame.place(
        relx=0.3,
        rely= 0.55,
        anchor="center")

    file1_button = customtkinter.CTkButton(
        file1_frame,
        text="Upload",
        command=upload_file1,
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

    file1_label = tk.Label(
        file1_frame,
        text="File 1:",
        font=NORMAL_FONT,
        bg=LIGHT_PURPLE,
        fg=DARK_PURPLE)
    file1_label.pack(pady=10)

    file1_buttons_frame = tk.Frame(file1_frame, bg=LIGHT_PURPLE)
    file1_buttons_frame.pack()

    #File2 Button
    file2_frame = tk.Frame(analyzeFrame, bg=LIGHT_PURPLE)
    file2_frame.place(
        relx=0.7,
        rely= 0.55,
        anchor="center")

    file2_button = customtkinter.CTkButton(
        file2_frame,
        text="Upload",
        command=upload_file2,
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

    file2_label = tk.Label(
        file2_frame,
        text="File 2: ",
        font=NORMAL_FONT,
        bg=LIGHT_PURPLE,
        fg=DARK_PURPLE)
    file2_label.pack(pady=10)

    file2_buttons_frame = tk.Frame(file2_frame, bg=LIGHT_PURPLE)
    file2_buttons_frame.pack()

    #Run Button
    runButton = customtkinter.CTkButton(
        analyzeFrame,
        text="Run",
        command= loadUploaded,
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
    runButton.place(relx=0.5, rely=0.7, anchor="n")

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
        command=loadRecorded, 
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