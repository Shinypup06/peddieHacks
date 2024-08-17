import tkinter as tk
from tkinter import filedialog
import time
import threading
from spleeter.separator import Separator
import os
import warnings
import wave
import pyaudio
import pygame
import whisper


#filter out warnings (idk if it actually does filter out warnings though)
warnings.filterwarnings('ignore')

#use pygame mixer for sound playback
pygame.init()
pygame.mixer.init()

def separate_audio(input_file, output_dir):

    # 2 stems splits into vocal and accompaniment
    separator = Separator('spleeter:2stems')

    # Create an output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Perform separation
    separator.separate_to_file(input_file, output_dir)

def create_header(window, title):
    # Create a header frame with #F7EFE5 background
    header_frame = tk.Frame(window, bg="#674188", height=50)
    header_frame.pack(fill=tk.X, side=tk.TOP)

    # Add header label with indigo text
    header_label = tk.Label(header_frame, text="Cool Name", font=("Verdana", 16, "bold"), bg="#674188", fg="#F7EFE5")
    header_label.pack(pady=10)

def upload_file1():
    global input1
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        # Extract and display file name
        file_name = file_path.split("/")[-1]  # For Unix-like paths
        input1 = file_path
        global label_file1
        label_file1.config(text=f"File 1: {file_name}")
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

def play_file(input):
    pygame.mixer.music.load(input)
    pygame.mixer.music.play()

def stop_playback():
    pygame.mixer.music.stop()

def show_buttons1(frame):
    for widget in frame.winfo_children():
        widget.grid_forget()  # Hide existing buttons
    # Create 2 square buttons

    button1 = tk.Button(frame, text="▶", width=3, height=0, font=("Verdana", 20), bg="#674188",
                       fg="#F7EFE5", command=lambda: play_file(input1))
    button1.grid(row=0, column=1, padx=10, pady=5)

    button2 = tk.Button(frame, text="◼", width=3, height=0, font=("Verdana", 20), bg="#674188",
                       fg="#F7EFE5", command=lambda: stop_playback())
    button2.grid(row=0, column=2, padx=10, pady=5)

def show_buttons2(frame):
    for widget in frame.winfo_children():
        widget.grid_forget()  # Hide existing buttons
    # Create 2 square buttons

    button1 = tk.Button(frame, text="▶", width=3, height=0, font=("Verdana", 20), bg="#674188",
                       fg="#F7EFE5", command=lambda: play_file(input2))
    button1.grid(row=0, column=1, padx=10, pady=5)

    button2 = tk.Button(frame, text="◼", width=3, height=0, font=("Verdana", 20), bg="#674188",
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

def splitAudio():
    separate_audio(input1,'output/')
    print("done separating audio")
    fade_out(loading_window, create_results_window)

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
                             bg="#bfc0e2", fg="#674188")
    loading_label.pack(pady=20)
    fade_in(loading_window)


    # Run the long task in a separate thread to prevent GUI freezing
    threading.Thread(target=splitAudio).start()

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

    results_label = tk.Label(results_frame, text="Here are the results of the processing:", font=("Verdana", 24),
                             bg="#bfc0e2", fg="#674188")
    results_label.pack(pady=20)

    result_text = "Result details go here."
    result_display = tk.Label(results_frame, text=result_text, font=("Verdana", 24), bg="#bfc0e2", fg="#674188")
    result_display.pack(pady=10)

    back_button = tk.Button(results_frame, text="Back",
                            command=lambda: fade_out(results_window, show_welcome_window), width=15, height=2,
                            font=("Verdana", 24), bg="#674188", fg="#F7EFE5")
    back_button.pack(pady=10)

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
    root.title("Upload MP3 Files")
    root.geometry("1920x1080")  # Set the window size to 1920x1080 pixels
    root.attributes("-alpha", 0.0)  # Start with invisible window

    # Set the background color for the entire window
    root.configure(bg="#bfc0e2")
    create_header(root, "Upload MP3 Files")


    main_frame = tk.Frame(root, bg="#bfc0e2")
    main_frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame

    label_instruction = tk.Label(main_frame, text="Please upload the MP3 files below:", font=("Verdana", 24),
                                 bg="#bfc0e2", fg="#674188")
    label_instruction.grid(row=0, column=0, columnspan=2, pady=10)

    # Create a grid for the buttons
    button_upload1 = tk.Button(main_frame, text="Upload MP3 File 1", command=upload_file1, width=19, height=2,
                               font=("Verdana", 16), bg="#F7EFE5", fg="#674188")
    button_upload1.grid(row=1, column=0, padx=20, pady=10)

    global label_file1
    label_file1 = tk.Label(main_frame, text="File 1: None", font=("Verdana", 24), bg="#bfc0e2", fg="#674188")
    label_file1.grid(row=2, column=0, pady=5)

    file1_buttons_frame = tk.Frame(main_frame, bg="#bfc0e2")
    file1_buttons_frame.grid(row=3, column=0, pady=10)

    button_upload2 = tk.Button(main_frame, text="Upload MP3 File 2", command=upload_file2, width=19, height=2,
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
    """Enable or disable the Run button based on file upload status."""
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

    input1 = None

    record_window = tk.Tk()
    record_window.title("Record")
    record_window.geometry("1920x1080")  # Set the window size to 1920x1080 pixels
    record_window.attributes("-alpha", 0.0)  # Start with invisible window

    # Set the background color for the entire window
    record_window.configure(bg="#bfc0e2")
    create_header(record_window, "Record")

    record_frame = tk.Frame(record_window, bg="#bfc0e2")
    record_frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame

    label_instruction = tk.Label(record_frame, text="Please upload the MP3 files below:", font=("Verdana", 24),
                                 bg="#bfc0e2", fg="#674188")
    label_instruction.grid(row=0, column=0, columnspan=2, pady=10)

    # Create a grid for the buttons
    button_upload1 = tk.Button(record_frame, text="Upload MP3 File 1", command=upload_fileRec, width=19, height=2,
                               font=("Verdana", 16), bg="#F7EFE5", fg="#674188")
    button_upload1.grid(row=1, column=0, padx=20, pady=10)

    rec_play_button = tk.Button(record_frame, text="Rec/Play", command=startRecording, width=15, height=2,
                                font=("Verdana", 16), bg="#F7EFE5", fg="black",
                                state=tk.DISABLED)  # Disabled by default
    rec_play_button.grid(row=1, column=1, padx=20, pady=10)  # Positioned to the right of the upload button

    re_record_button = tk.Button(record_frame, text="Re-record", command=lambda: stop_rec(), width=15,
                                 height=2, font=("Verdana", 16), bg="#F7EFE5", fg="black", state=tk.DISABLED)
    re_record_button.grid(row=2, column=1, padx=20, pady=10)  # Positioned below the Rec/Play button

    playFrame = tk.Frame(record_frame, bg="#bfc0e2")
    playFrame.grid(row=3, column=1, pady=10)

    global label_file1
    label_file1 = tk.Label(record_frame, text="File 1: None", font=("Verdana", 24), bg="#bfc0e2", fg="#674188")
    label_file1.grid(row=2, column=0, pady=5)  # Adjusted columnspan to 1

    file_buttons_frame = tk.Frame(record_frame, bg="#bfc0e2")
    file_buttons_frame.grid(row=3, column=0, pady=10, columnspan=2)

    # Create a frame for buttons at the bottom
    bottom_frame = tk.Frame(record_window, bg="#bfc0e2")
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    # Add buttons to bottom_frame
    back_button = tk.Button(bottom_frame, text="Back",
                                    command=lambda: fade_out(record_window, show_welcome_window), width=15, height=2,
                                    font=("Verdana", 24), bg="#674188", fg="#F7EFE5")
    back_button.pack(side=tk.LEFT, padx=10, pady=10)

    save_analyze_button = tk.Button(bottom_frame, text="Save and Analyze",
                                    command=lambda: fade_out(record_window, create_results_window), width=15, height=2,
                                    font=("Verdana", 24), bg="#674188", fg="#F7EFE5", state=tk.DISABLED)
    save_analyze_button.pack(side=tk.RIGHT, padx=10, pady=10)  # Positioned to the right side of the bottom frame

    fade_in(record_window)
    record_window.mainloop()

def splitAudio2():
    global lyrics
    separate_audio(input1,'output/')
    print("done separating audio")
    lyrics = whisper.load_model("base").transcribe("output/" + name + "/vocals.wav")["text"]
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

        # Run the long task in a separate thread to prevent GUI freezing
        threading.Thread(target=splitAudio2).start()

def get_audio_length(file_path):
    with wave.open(file_path, 'rb') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
    return duration

def startRecording():
    global FORMAT, CHANNELS, RATE, CHUNK, RECORD_SECONDS, OUTPUT_FILENAME, stop_recording

    # Parameters
    FORMAT = pyaudio.paInt16  # Format of sampling
    CHANNELS = 1  # Number of channels: 1 for mono, 2 for stereo
    RATE = 44100  # Sampling rate: 44100 samples per second
    CHUNK = 1024  # Number of audio frames per buffer
    RECORD_SECONDS = get_audio_length(input1)  # Max duration of recording in seconds
    OUTPUT_FILENAME = "output.wav"  # Output file name

    # Global variable to control recording
    stop_recording = False

    # Start recording audio in a separate thread
    recording_thread = threading.Thread(target=record_audio)
    recording_thread.start()

    # Wait for the recording thread to finish
    re_record_button.config(state=tk.NORMAL)  # Enable the Re-record button
    # recording_thread.join()

def record_audio():
        audio = pyaudio.PyAudio()

        play_file("output/" + name + "/accompaniment.wav")

        # Start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        print("Recording...")

        frames = []
        start_time = time.time()

        while not stop_recording and (time.time() - start_time) < RECORD_SECONDS:
            data = stream.read(CHUNK)
            frames.append(data)

        # Stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        print("Finished recording")

        # Save the recorded data as a WAV file
        with wave.open(OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        print(f"Audio saved as {OUTPUT_FILENAME}")
        for widget in playFrame.winfo_children():
            widget.grid_forget()  # Hide existing buttons

        # Create 2 square buttons
        button1 = tk.Button(playFrame, text="▶", width=3, height=0, font=("Verdana", 20), bg="#674188",
                        fg="#F7EFE5", command=lambda: play_file("output.wav"))
        button1.grid(row=0, column=1, padx=10, pady=5)

        button2 = tk.Button(playFrame, text="◼", width=3, height=0, font=("Verdana", 20), bg="#674188",
                        fg="#F7EFE5", command=lambda: stop_playback())
        button2.grid(row=0, column=2, padx=10, pady=5)

        # Enable the Save and Analyze button

        save_analyze_button.config(state=tk.NORMAL)

def stop_rec():
    global stop_recording
    stop_recording = True
    stop_playback()

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

    welcome_label = tk.Label(welcome_frame, text="You can upload an existing file of your singing or record something in the app", font=("Verdana", 24), bg="#bfc0e2", fg="#674188")
    welcome_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Create a frame for the Record button and its label
    record_frame = tk.Frame(welcome_frame, bg="#bfc0e2")
    record_frame.grid(row=5, column=1, padx=20)

    record_label = tk.Label(record_frame, text="Record something new:", font=("Verdana", 18), bg="#bfc0e2",
                            fg="#674188")
    record_label.pack(pady=10)

    record_button = tk.Button(record_frame, text="Record",
                              command=lambda: fade_out(welcome_window, create_record_window), width=15, height=2,
                              font=("Verdana", 18), bg="#674188", fg="#F7EFE5")
    record_button.pack()

    # Create a frame for the Analyze button and its label
    analyze_frame = tk.Frame(welcome_frame, bg="#bfc0e2")
    analyze_frame.grid(row=5, column=0, padx=20)

    analyze_label = tk.Label(analyze_frame, text="Analyze existing files:", font=("Verdana", 18), bg="#bfc0e2",
                             fg="#674188")
    analyze_label.pack(pady=10)

    analyze_button = tk.Button(analyze_frame, text="Analyze",
                               command=lambda: fade_out(welcome_window, create_main_window), width=15, height=2,
                               font=("Verdana", 18), bg="#674188", fg="#F7EFE5")
    analyze_button.pack()


    fade_in(welcome_window)
    welcome_window.mainloop()


# Create the initial welcome window
if __name__ == "__main__":
    show_welcome_window()