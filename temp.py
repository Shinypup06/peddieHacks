import pyaudio
import wave
import threading
import time

def get_audio_length(file_path):
    with wave.open(file_path, 'rb') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
    return duration

# Parameters
FORMAT = pyaudio.paInt16  # Format of sampling
CHANNELS = 1  # Number of channels: 1 for mono, 2 for stereo
RATE = 44100  # Sampling rate: 44100 samples per second
CHUNK = 1024  # Number of audio frames per buffer
RECORD_SECONDS = get_audio_length("sampleAudios/mammamia.wav")  # Max duration of recording in seconds
OUTPUT_FILENAME = "output.wav"  # Output file name

# Global variable to control recording
stop_recording = False

# Function to stop recording
def stop_recording_function():
    global stop_recording
    stop_recording = True

# Function to record audio
def record_audio():
    global stop_recording
    audio = pyaudio.PyAudio()

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

# Start recording audio in a separate thread
recording_thread = threading.Thread(target=record_audio)
recording_thread.start()

# Example usage: Call this function to stop recording before the time is up
# stop_recording_function()  # Uncomment to stop recording early

# Wait for the recording thread to finish
recording_thread.join()
