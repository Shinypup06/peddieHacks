import tkinter as tk
from tkinter import filedialog


def create_header(window, title):
    # Create a header frame with white background
    header_frame = tk.Frame(window, bg="white", height=50)
    header_frame.pack(fill=tk.X, side=tk.TOP)

    # Add header label with indigo text
    header_label = tk.Label(header_frame, text="Cool Name", font=("Helvetica", 16, "bold"), bg="white", fg="#4B0082")
    header_label.pack(pady=10)


def upload_file1():
    file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
    if file_path:
        # Extract and display file name
        file_name = file_path.split("/")[-1]  # For Unix-like paths
        global label_file1
        label_file1.config(text=f"File 1: {file_name}")


def upload_file2():
    file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
    if file_path:
        # Extract and display file name
        file_name = file_path.split("/")[-1]  # For Unix-like paths
        global label_file2
        label_file2.config(text=f"File 2: {file_name}")


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
    fade_out(root, lambda: create_results_window())


def create_results_window():
    global results_window
    results_window = tk.Tk()
    results_window.title("Results")
    results_window.geometry("1920x1080")  # Set the window size to 1920x1080 pixels
    results_window.attributes("-alpha", 0.0)  # Start with invisible window

    # Set the background color for the entire window
    results_window.configure(bg="lavender")
    create_header(results_window, "Results")

    results_frame = tk.Frame(results_window, bg="lavender")
    results_frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame

    results_label = tk.Label(results_frame, text="Here are the results of the processing:", font=("Helvetica", 24),
                             bg="lavender", fg="#4B0082")
    results_label.pack(pady=20)

    result_text = "Result details go here."
    result_display = tk.Label(results_frame, text=result_text, font=("Helvetica", 24), bg="lavender", fg="#4B0082")
    result_display.pack(pady=10)

    back_button = tk.Button(results_frame, text="Back to Welcome",
                            command=lambda: fade_out(results_window, show_welcome_window), width=15, height=2,
                            font=("Helvetica", 24), bg="#4B0082", fg="white")
    back_button.pack(pady=10)

    fade_in(results_window)
    results_window.mainloop()


def show_main_window():
    global welcome_window
    fade_out(welcome_window, create_main_window)


def create_main_window():
    global root
    global label_file1, label_file2
    root = tk.Tk()
    root.title("Upload MP3 Files")
    root.geometry("1920x1080")  # Set the window size to 1920x1080 pixels
    root.attributes("-alpha", 0.0)  # Start with invisible window

    # Set the background color for the entire window
    root.configure(bg="lavender")
    create_header(root, "Upload MP3 Files")

    main_frame = tk.Frame(root, bg="lavender")
    main_frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame

    label_instruction = tk.Label(main_frame, text="Please upload the MP3 files below:", font=("Helvetica", 24),
                                 bg="lavender", fg="#4B0082")
    label_instruction.grid(row=0, column=0, columnspan=2, pady=10)

    # Create a grid for the buttons
    button_upload1 = tk.Button(main_frame, text="Upload MP3 File 1", command=upload_file1, width=19, height=2,
                               font=("Helvetica", 16), bg="white", fg="#4B0082")
    button_upload1.grid(row=1, column=0, padx=20, pady=10)

    global label_file1
    label_file1 = tk.Label(main_frame, text="File 1: None", font=("Helvetica", 24), bg="lavender", fg="#4B0082")
    label_file1.grid(row=2, column=0, pady=5)

    button_upload2 = tk.Button(main_frame, text="Upload MP3 File 2", command=upload_file2, width=19, height=2,
                               font=("Helvetica", 16), bg="white", fg="#4B0082")
    button_upload2.grid(row=1, column=1, padx=20, pady=10)

    global label_file2
    label_file2 = tk.Label(main_frame, text="File 2: None", font=("Helvetica", 24), bg="lavender", fg="#4B0082")
    label_file2.grid(row=2, column=1, pady=5)

    # Add one line of space between the upload labels and the run button
    spacer = tk.Label(main_frame, bg="lavender")
    spacer.grid(row=3, column=0, columnspan=2, pady=10)

    # Adjusted font size and dimensions for run button
    button_run = tk.Button(main_frame, text="Run", command=show_results, width=15, height=2, font=("Helvetica", 24),
                           bg="#4B0082", fg="white")
    button_run.grid(row=4, column=0, columnspan=2, pady=10)

    fade_in(root)
    root.mainloop()


def show_welcome_window():
    global welcome_window
    global results_window
    if 'results_window' in globals():
        results_window.destroy()

    welcome_window = tk.Tk()
    welcome_window.title("Welcome")
    welcome_window.geometry("1920x1080")  # Set the window size to 1920x1080 pixels
    welcome_window.attributes("-alpha", 0.0)  # Start with invisible window

    # Set the background color for the entire window
    welcome_window.configure(bg="lavender")
    create_header(welcome_window, "Welcome")

    welcome_frame = tk.Frame(welcome_window, bg="lavender")
    welcome_frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame

    welcome_label = tk.Label(welcome_frame,
                             text="Welcome to the MP3 File Uploader\n\nPlease read the instructions below and click 'Start' to proceed.",
                             font=("Helvetica", 24), bg="lavender", fg="#4B0082")
    welcome_label.pack(pady=20)

    start_button = tk.Button(welcome_frame, text="Start", command=lambda: fade_out(welcome_window, create_main_window),
                             width=15, height=2, font=("Helvetica", 24), bg="#4B0082", fg="white")
    start_button.pack(pady=10)

    fade_in(welcome_window)
    welcome_window.mainloop()


# Create the initial welcome window
show_welcome_window()
