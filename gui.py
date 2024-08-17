import tkinter as tk
from tkinter import filedialog
import threading
import pygame
import subprocess, multiprocessing
from comparer import *
from splitter import *
from sound import *
from lyricReader import *
from record import *
from lyrics import *

#use pygame mixer for sound playback
pygame.init()
pygame.mixer.init()

current_entries = []
leaderboard_text = ""

def create_header(window, title):
    # Create a header frame with #F7EFE5 background
    header_frame = tk.Frame(window, bg="#674188", height=50)
    header_frame.pack(fill=tk.X, side=tk.TOP)

    # Add header label with indigo text
    header_label = tk.Label(header_frame, text="Karacroakie", font=("Verdana", 16, "bold"), bg="#674188", fg="#F7EFE5")
    header_label.pack(pady=10)

def upload_file1():
    global input1, name
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        # Extract and display file name
        file_name = file_path.split("/")[-1]  # For Unix-like paths
        input1 = file_path
        global label_file1
        label_file1.config(text=f"File 1: {file_name}")
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
        global label_file2
        label_file2.config(text=f"File 2: {file_name}")
        print(f"Input2: {input2}")
        show_buttons2(file2_buttons_frame)
        update_run_button_state()

def show_buttons1(frame):
    for widget in frame.winfo_children():
        widget.grid_forget()  # Hide existing buttons
    # Create 2 square buttons

    button1 = tk.Button(frame, text="▶", width=3, height=0, font=("Verdana", 20), bg="#674188",
                       fg="#F7EFE5", command=lambda: play_file(input1))
    button1.grid(row=0, column=1, padx=10, pady=5)

    button2 = tk.Button(frame, text="■", width=3, height=0, font=("Verdana", 20), bg="#674188",
                       fg="#F7EFE5", command=lambda: stop_playback())
    button2.grid(row=0, column=2, padx=10, pady=5)

def show_buttons2(frame):
    for widget in frame.winfo_children():
        widget.grid_forget()  # Hide existing buttons
    # Create 2 square buttons

    button1 = tk.Button(frame, text="▶", width=3, height=0, font=("Verdana", 20), bg="#674188",
                       fg="#F7EFE5", command=lambda: play_file(input2))
    button1.grid(row=0, column=1, padx=10, pady=5)

    button2 = tk.Button(frame, text="■", width=3, height=0, font=("Verdana", 20), bg="#674188",
                       fg="#F7EFE5", command=lambda: stop_playback())
    button2.grid(row=0, column=2, padx=10, pady=5)

def fade_out(window, callback):
    alpha = 1.0

    def step():
        nonlocal alpha
        if alpha > 0:
            alpha -= 0.1  # Increase step size for faster fade
            if alpha < 0:
                alpha = 0
            window.attributes("-alpha", alpha)
            window.after(30, step)  # Reduce delay for faster fade
        else:
            window.withdraw()  # Hide the window
            callback()

    step()

def fade_in(window):
    alpha = 0.0

    def step():
        nonlocal alpha
        if alpha < 1.0:
            alpha += 0.1  # Increase step size for faster fade
            if alpha > 1:
                alpha = 1
            window.attributes("-alpha", alpha)
            window.after(30, step)  # Reduce delay for faster fade
        else:
            window.deiconify()  # Show the window

    step()

def show_results():
    global root
    fade_out(root, show_loading_screen)

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
    fade_out(loading_window, create_results_window)

def add_to_leaderboard(entry_name, leaderboard, score_label):
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
        score_label.config(text=score)
        btn_add.config(state="disabled")

def create_saved_window():
    global saved_window
    global welcome_window
    global btn_add
    saved_window = tk.Toplevel()
    saved_window.title("Leaderboard")
    saved_window.geometry("1920x1080")  # Set the window size to 1920x1080 pixels
    saved_window.configure(bg="#bfc0e2")
    create_header(saved_window, "Leaderboard")

    # Create a main frame to hold both the entry form and the leaderboard side by side
    main_frame = tk.Frame(saved_window, bg="#bfc0e2")
    main_frame.place(relx=0.5, rely=0.5, anchor='center')

    # Create the text input fields and 'Add' button
    saved_frame = tk.Frame(main_frame, bg="#bfc0e2")
    saved_frame.grid(row=0, column=0, padx=20, pady=20)

    tk.Label(saved_frame, text="Name:", font=("Verdana", 18), bg="#bfc0e2", fg="#0a0b40").grid(row=0, column=0, padx=5, pady=5)
    entry_name = tk.Entry(saved_frame, font=("Verdana", 18), width=20, bg="#F7EFE5", fg="#674188")
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(saved_frame, text="Score:", font=("Verdana", 18), bg="#bfc0e2", fg="#0a0b40").grid(row=1, column=0, padx=5, pady=5)
    score_label = tk.Label(saved_frame, text=score, font=("Verdana", 18), bg="#bfc0e2", fg="#674188")
    score_label.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(saved_frame, text="Song:", font=("Verdana", 18), bg="#bfc0e2", fg="#0a0b40").grid(row=2, column=0, padx=5, pady=5)
    song_label = tk.Label(saved_frame, text=name, font=("Verdana", 18), bg="#bfc0e2", fg="#674188")
    song_label.grid(row=2, column=1, padx=5, pady=5)

    # Pass the widgets to the add_to_leaderboard function
    btn_add = tk.Button(saved_frame, text="Add to Leaderboard",
                        command=lambda: add_to_leaderboard(entry_name, leaderboard, score_label),
                        font=("Verdana", 18), bg="#674188", fg="#F7EFE5", width=25, height=2)
    btn_add.grid(row=3, column=0, columnspan=2, pady=10)

    # Create the leaderboard listbox in the frame_leaderboard
    frame_leaderboard = tk.Frame(main_frame, bg="#bfc0e2")
    frame_leaderboard.grid(row=0, column=1, padx=20, pady=20)

    tk.Label(frame_leaderboard, text="Leaderboard:", font=("Verdana", 24), bg="#bfc0e2", fg="#0a0b40").pack()
    leaderboard = tk.Listbox(frame_leaderboard, width=40, height=15, font=("Verdana", 18), bg="#F7EFE5", fg="#674188")
    
    # add previous entries
    leaderboard.delete(0, tk.END)
    for entry in current_entries:
        leaderboard.insert(tk.END, f"{entry[1]}: {entry[0]:.2f} -- {name}")

    leaderboard.pack()

    # Create a frame for buttons at the bottom
    bottom_frame = tk.Frame(saved_window, bg="#bfc0e2")
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    # Add buttons to bottom_frame
    btn_back = tk.Button(bottom_frame, text="Back",
                         command=lambda: fade_out(saved_window, show_welcome_window),
                         width=15, height=2, font=("Verdana", 24), bg="#674188", fg="#F7EFE5")
    btn_back.pack(side=tk.LEFT, padx=10, pady=10)

    fade_in(saved_window)
    saved_window.mainloop()

def show_loading_screen():
    global loading_window
    loading_window = tk.Toplevel()
    loading_window.title("Loading")
    loading_window.geometry("1920x1080")
    loading_window.configure(bg="#bfc0e2")
    create_header(loading_window, "Loading...")

    loading_frame = tk.Frame(loading_window, bg="#bfc0e2")
    loading_frame.place(relx=0.5, rely=0.5, anchor='center')

    loading_label = tk.Label(loading_frame, text="Processing your files, please wait...", font=("Verdana", 24),
                             bg="#bfc0e2", fg="#0a0b40")
    loading_label.pack(pady=20)
    fade_in(loading_window)

    # Run the long task in a separate thread to prevent GUI freezing
    threading.Thread(target=analyzeAudio).start()

def create_results_window():
    global results_window

    results_window = tk.Tk()
    results_window.title("Results")
    results_window.geometry("1920x1080")  # Set the window size to 1920x1080 pixels
    results_window.attributes("-alpha", 0.0)  # Start with invisible window

    # Set the background color for the entire window
    results_window.configure(bg="#bfc0e2")
    create_header(results_window, "Results")

    results_frame = tk.Frame(results_window, bg="#bfc0e2")
    results_frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame

    results_label = tk.Label(results_frame, text=f"Your Pitch Accuracy Score: {score}%", font=("Verdana", 24),
                             bg="#bfc0e2", fg="#674188")
    results_label.pack(pady=20)

    result_text = "Result details go here."
    result_display = tk.Label(results_frame, text=result_text, font=("Verdana", 24), bg="#bfc0e2", fg="#674188")
    result_display.pack(pady=10)

    # New button placed at the bottom right corner
    new_button = tk.Button(results_window, text="Save results",
                           command=lambda: fade_out(results_window, create_saved_window), width=15, height=2,
                           font=("Verdana", 24), bg="#674188", fg="#F7EFE5")
    new_button.place(relx=0.95, rely=0.95, anchor='se')  # Place at the bottom right corner

    # Back button placed at the bottom left corner
    back_button = tk.Button(results_window, text="Back",
                            command=lambda: fade_out(results_window, show_welcome_window), width=15, height=2,
                            font=("Verdana", 24), bg="#674188", fg="#F7EFE5")
    back_button.place(relx=0.05, rely=0.95, anchor='sw')  # Place at the bottom left corner

    fade_in(results_window)
    results_window.mainloop()

def create_main_window():
    global root
    global label_file1, label_file2, file1_buttons_frame, file2_buttons_frame
    global input1, input2
    global button_run
    input1 = None
    input2 = None

    root = tk.Tk()
    root.title("Upload WAV Files")
    root.geometry("1920x1080")  # Set the window size to 1920x1080 pixels
    root.attributes("-alpha", 0.0)  # Start with invisible window

    # Set the background color for the entire window
    root.configure(bg="#bfc0e2")
    create_header(root, "Upload WAV Files")


    main_frame = tk.Frame(root, bg="#bfc0e2")
    main_frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame

    label_instruction = tk.Label(main_frame, text="Please upload the WAV files below:", font=("Verdana", 24),
                                 bg="#bfc0e2", fg="#0a0b40")
    label_instruction.grid(row=0, column=0, columnspan=2, pady=10)

    # Create a grid for the buttons
    button_upload1 = tk.Button(main_frame, text="Upload original song", command=upload_file1, width=19, height=2,
                               font=("Verdana", 16), bg="#F7EFE5", fg="#674188")
    button_upload1.grid(row=1, column=0, padx=20, pady=10)

    global label_file1
    label_file1 = tk.Label(main_frame, text="File 1: None", font=("Verdana", 24), bg="#bfc0e2", fg="#674188")
    label_file1.grid(row=2, column=0, pady=5)

    file1_buttons_frame = tk.Frame(main_frame, bg="#bfc0e2")
    file1_buttons_frame.grid(row=3, column=0, pady=10)

    button_upload2 = tk.Button(main_frame, text="Upload your singing", command=upload_file2, width=19, height=2,
                               font=("Verdana", 16), bg="#F7EFE5", fg="#674188")
    button_upload2.grid(row=1, column=1, padx=20, pady=10)

    global label_file2
    label_file2 = tk.Label(main_frame, text="File 2: None", font=("Verdana", 24), bg="#bfc0e2", fg="#674188")
    label_file2.grid(row=2, column=1, pady=5)

    file2_buttons_frame = tk.Frame(main_frame, bg="#bfc0e2")
    file2_buttons_frame.grid(row=3, column=1, pady=10)

    # Add one line of space between the upload labels and the run button
    spacer = tk.Label(main_frame, bg="#bfc0e2")
    spacer.grid(row=3, column=0, columnspan=2, pady=10)

    # Adjusted font size and dimensions for run button
    button_run = tk.Button(main_frame, text="Run", command=show_results, width=15, height=2, font=("Verdana", 24),
                           bg="#674188", fg="#F7EFE5", state=tk.DISABLED)
    button_run.grid(row=4, column=0, columnspan=2, pady=10)

    # Create a frame for buttons at the bottom
    bottom_frame = tk.Frame(root, bg="#bfc0e2")
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    # Add buttons to bottom_frame
    back_button = tk.Button(bottom_frame, text="Back",
                            command=lambda: fade_out(root, show_welcome_window), width=15, height=2,
                            font=("Verdana", 24), bg="#674188", fg="#F7EFE5")
    back_button.pack(side=tk.LEFT, padx=10, pady=10)

    fade_in(root)
    root.mainloop()

def update_run_button_state():
    if input1 and input2:
        button_run.config(state=tk.NORMAL)  # Enable the Run button
    else:
        button_run.config(state=tk.DISABLED)  # Disable the Run button

def create_record_window():
    global record_window
    global label_file1, file_buttons_frame, playFrame
    global input1
    global rec_play_button
    global re_record_button
    global save_analyze_button
    global text_block
    global artist_entry, song_entry
    default_text = "Your lyrics will show up here after you upload your song! Feel free to change them. Lyric detection is still under development."
    input1 = None

    record_window = tk.Tk()
    record_window.title("Record")
    record_window.geometry("1920x1080")  # Set the window size to 1920x1080 pixels
    record_window.attributes("-alpha", 0.0)  # Start with invisible window

    # Set the background color for the entire window
    record_window.configure(bg="#bfc0e2")
    create_header(record_window, "Record")

    # Create a frame to center the top frame
    center_frame = tk.Frame(record_window, bg="#bfc0e2")
    center_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Create a frame for the top half of the window
    record_frame = tk.Frame(center_frame, bg="#bfc0e2")
    record_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=(0, 70), pady=(70, 0))

    label_instruction = tk.Label(record_frame, text="Please upload a WAV file of\nthe original song below:",
                                 font=("Verdana", 24),
                                 bg="#bfc0e2", fg="#0a0b40")
    label_instruction.grid(row=0, column=0, columnspan=2, pady=(50,5))  # Adjusted pady to move down

    # New label directly above the text block
    label_above_text = tk.Label(record_frame,
                                text="         Use the generated lyrics or\n         paste from the internet:",
                                font=("Verdana", 24),
                                bg="#bfc0e2", fg="#0a0b40")
    label_above_text.grid(row=0, column=2, pady=(50, 5), sticky='w')  # Adjusted pady to move down

    # Create a block of editable text
    text_block = tk.Text(record_frame, wrap='word', height=5, width=30, font=("Verdana", 18), bg="#F7EFE5",
                         fg="#674188")
    text_block.grid(row=1, column=2, rowspan=3, padx=20, pady=10, sticky='nsew')  # Adjusted pady to move down

    text_block.insert(tk.END, default_text)

    # Create a grid for the buttons
    button_upload1 = tk.Button(record_frame, text="Upload original song", command=upload_fileRec, width=19, height=2,
                               font=("Verdana", 16), bg="#F7EFE5", fg="#674188")
    button_upload1.grid(row=1, column=0, padx=20, pady=10)

    rec_play_button = tk.Button(record_frame, text="Rec/Play",
                                command=lambda: startRecording(name, "output.wav", enableRecordingPlayback, input1,
                                                               re_record_button.config(state=tk.NORMAL)), width=15,
                                height=2,
                                font=("Verdana", 16), bg="#F7EFE5", fg="black",
                                state=tk.DISABLED)  # Disabled by default
    rec_play_button.grid(row=1, column=1, padx=20, pady=10)  # Positioned to the right of the upload button

    re_record_button = tk.Button(record_frame, text="Re-record", command=lambda: stop_rec(), width=15,
                                 height=2, font=("Verdana", 16), bg="#F7EFE5", fg="#0a0b40", state=tk.DISABLED)
    re_record_button.grid(row=2, column=1, padx=20, pady=10)  # Positioned below the Rec/Play button

    playFrame = tk.Frame(record_frame, bg="#bfc0e2")
    playFrame.grid(row=3, column=0, columnspan=2, pady=10)

    label_file1 = tk.Label(record_frame, text="File 1: None", font=("Verdana", 24), bg="#bfc0e2", fg="#674188")
    label_file1.grid(row=2, column=0, pady=5)  # Adjusted columnspan to 1

    file_buttons_frame = tk.Frame(record_frame, bg="#bfc0e2")
    file_buttons_frame.grid(row=3, column=1, pady=10, columnspan=2)

    # Create a frame for the middle section
    middle_frame = tk.Frame(record_window, bg="#bfc0e2")
    middle_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    label_blank = tk.Label(middle_frame, text="    ", font=("Verdana", 18), bg="#bfc0e2", fg="#0a0b40")
    label_blank.grid(row=0, column=0, padx=10, pady=10, sticky='e')

    # Song input
    label_song = tk.Label(middle_frame, text="Song:", font=("Verdana", 18), bg="#bfc0e2", fg="#0a0b40")
    label_song.grid(row=1, column=0, padx=10, pady=10, sticky='e')
    song_entry = tk.Entry(middle_frame, font=("Verdana", 18), width=30, bg="#F7EFE5", fg="#674188")  # Set width to make it shorter
    song_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    # Artist input
    label_artist = tk.Label(middle_frame, text="Artist:", font=("Verdana", 18), bg="#bfc0e2", fg="#0a0b40")
    label_artist.grid(row=2, column=0, padx=10, pady=10, sticky='e')
    artist_entry = tk.Entry(middle_frame, font=("Verdana", 18), width=30, bg="#F7EFE5", fg="#674188")  # Set width to make it shorter
    artist_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    # Search button
    search_button = tk.Button(middle_frame, text="Search", command=searchLyrics, font=("Verdana", 20), bg="#674188", fg="#F7EFE5")
    search_button.grid(row=3, column=0, columnspan=2, pady=20)

    # Create a frame for buttons at the bottom
    bottom_frame = tk.Frame(record_window, bg="#bfc0e2")
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    # Add buttons to bottom_frame
    back_button = tk.Button(bottom_frame, text="Back",
                                    command=lambda: fade_out(record_window, show_welcome_window), width=15, height=2,
                                    font=("Verdana", 24), bg="#674188", fg="#F7EFE5")
    back_button.pack(side=tk.LEFT, padx=10, pady=10)

    save_analyze_button = tk.Button(bottom_frame, text="Save & Analyze",
                                    command=lambda: fade_out(record_window, showLoadingWindow2), width=15, height=2,
                                    font=("Verdana", 24), bg="#674188", fg="#F7EFE5", state=tk.DISABLED)
    save_analyze_button.pack(side=tk.RIGHT, padx=10, pady=10)  # Positioned to the right side of the bottom frame

    # Adjust the grid configuration to ensure proper centering
    record_frame.grid_rowconfigure(0, weight=1)
    record_frame.grid_rowconfigure(1, weight=1)
    record_frame.grid_rowconfigure(2, weight=1)
    record_frame.grid_columnconfigure(0, weight=1)
    record_frame.grid_columnconfigure(1, weight=1)
    record_frame.grid_columnconfigure(2, weight=1)

    middle_frame.grid_columnconfigure(0, weight=1)
    middle_frame.grid_columnconfigure(1, weight=1)

    fade_in(record_window)
    record_window.mainloop()

def searchLyrics():
    global lyrics
    artist = artist_entry.get()
    title = song_entry.get()
    
    lyrics = getInternetLyrics(artist, title)
    
    # Insert generated lyrics into the lyrics box
    text_block.delete('1.0', tk.END)
    text_block.insert(tk.END, lyrics)

    rec_play_button.config(state=tk.NORMAL)  # Enable the Rec/Play button

# TODO: need a generate lyrics button
def getGeneratedLyrics():
    global lyrics
    lyrics = getLyrics("output/" + name + "/vocals.wav")
    
    # Insert generated lyrics into the lyrics box
    text_block.delete('1.0', tk.END)
    text_block.insert(tk.END, lyrics)

def analyzeRecordedAudio():
    global score
    score = scaleToScore(compareaudios("output/" + name + "/vocals.wav", "output.wav"))
    fade_out(loading_window, create_results_window)

def showLoadingWindow2():
    global loading_window
    loading_window = tk.Toplevel()
    loading_window.title("Loading")
    loading_window.geometry("1920x1080")
    loading_window.configure(bg="#bfc0e2")
    create_header(loading_window, "Loading...")

    loading_frame = tk.Frame(loading_window, bg="#bfc0e2")
    loading_frame.place(relx=0.5, rely=0.5, anchor='center')

    loading_label = tk.Label(loading_frame, text="Processing your files, please wait...", font=("Verdana", 24),
                             bg="#bfc0e2", fg="#0a0b40")
    loading_label.pack(pady=20)
    fade_in(loading_window)

    # Run the long task in a separate thread to prevent GUI freezing
    threading.Thread(target=analyzeRecordedAudio).start()

def processOriginalSong():
    global lyrics
    separate_audio(input1,'output/')
    print("done separating audio")
    
    rec_play_button.config(state=tk.NORMAL)  # Enable the Rec/Play button

def upload_fileRec():
    global input1, name
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        # Extract and display file name
        file_name = file_path.split("/")[-1]  # For Unix-like paths
        input1 = file_path
        global label_file1
        name = file_name[:-4]
        label_file1.config(text=f"File 1: {file_name}")
        print(f"Input1: {input1}")
        print(f"fileName: {name}")

        # Split audio and get lyrics in a separate thread to prevent GUI freezing
        threading.Thread(target=processOriginalSong).start()

def enableRecordingPlayback():
        
        for widget in playFrame.winfo_children():
            widget.grid_forget()  # Hide existing buttons

        # Create 2 square buttons
        button1 = tk.Button(playFrame, text="▶", width=3, height=0, font=("Verdana", 20), bg="#674188",
                        fg="#F7EFE5", command=lambda: play_file("output.wav"))
        button1.grid(row=0, column=1, padx=10, pady=5)

        button2 = tk.Button(playFrame, text="■", width=3, height=0, font=("Verdana", 20), bg="#674188",
                        fg="#F7EFE5", command=lambda: stop_playback())
        button2.grid(row=0, column=2, padx=10, pady=5)

        # Enable the Save and Analyze button
        save_analyze_button.config(state=tk.NORMAL)

def show_welcome_window():
    global welcome_window
    global results_window

    welcome_window = tk.Tk()
    welcome_window.title("Welcome")
    welcome_window.geometry("1920x1080")
    welcome_window.attributes("-alpha", 0.0)
    welcome_window.configure(bg="#bfc0e2")
    create_header(welcome_window, "Welcome")

    welcome_frame = tk.Frame(welcome_window, bg="#bfc0e2")
    welcome_frame.place(relx=0.5, rely=0.5, anchor='center')

    welcome_label = tk.Label(welcome_frame, text="Karacroakie gives enhanced AI karaoke feedback \n Select one of the two options to evaluate your singing skills", font=("Verdana", 24), bg="#bfc0e2", fg="#674188")
    welcome_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))


    # Create a frame for the Record button and its label
    record_frame = tk.Frame(welcome_frame, bg="#bfc0e2")
    record_frame.grid(row=1, column=1, padx=20, pady=(20, 40))

    record_label = tk.Label(record_frame, text="Upload a WAV file of any song \n Record your voice with the \n automatically separated instrumentals", font=("Verdana", 18), bg="#bfc0e2",
                            fg="#0a0b40")
    record_label.pack(pady=10)

    record_button = tk.Button(record_frame, text="Record",
                              command=lambda: fade_out(welcome_window, create_record_window), width=15, height=2,
                              font=("Verdana", 24), bg="#674188", fg="#F7EFE5")
    record_button.pack()

    # Create a frame for the Analyze button and its label
    analyze_frame = tk.Frame(welcome_frame, bg="#bfc0e2")
    analyze_frame.grid(row=1, column=0, padx=20, pady=(20,40))

    analyze_label = tk.Label(analyze_frame, text="Have a recording of your singing? \n Upload the original song and \n your recording as WAV files", font=("Verdana", 18), bg="#bfc0e2",
                             fg="#0a0b40")
    analyze_label.pack(pady=10)

    analyze_button = tk.Button(analyze_frame, text="Analyze",
                               command=lambda: fade_out(welcome_window, create_main_window), width=15, height=2,
                               font=("Verdana", 24), bg="#674188", fg="#F7EFE5")
    analyze_button.pack()




    fade_in(welcome_window)
    welcome_window.mainloop()

# Create the initial welcome window
if __name__ == "__main__":
    show_welcome_window()

