import pyaudio
import wave
import threading
import time
from sound import *

def get_audio_length(file_path):
    with wave.open(file_path, 'rb') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
    return duration

def startRecording(songName, outputName, afterRecord, input1, afterStart):
    global FORMAT, CHANNELS, RATE, CHUNK, RECORD_SECONDS, OUTPUT_FILENAME, stop_recording

    # Parameters
    FORMAT = pyaudio.paInt16  # Format of sampling
    CHANNELS = 1  # Number of channels: 1 for mono, 2 for stereo
    RATE = 44100  # Sampling rate: 44100 samples per second
    CHUNK = 1024  # Number of audio frames per buffer
    RECORD_SECONDS = get_audio_length(input1)  # Max duration of recording in seconds
    OUTPUT_FILENAME = outputName  # Output file name

    # Global variable to control recording, set to true when re-record is clicked
    stop_recording = False

    # Start recording audio in a separate thread
    recording_thread = threading.Thread(target=lambda: record_audio(songName, afterRecord))
    recording_thread.start()
    afterStart()
    


def record_audio(songName, afterRecord):
        audio = pyaudio.PyAudio()

        # plays the spliced audio accompaniment
        play_file("output/" + songName + "/accompaniment.wav")

        # Start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        print("Recording...")

        frames = []
        start_time = time.time()

        #keep recording until backtrack ends OR until user hits re-record
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

        # Adjust volume so that track volume and recorded volume are not obnoxiously different
        # third param is target volume in dBFS
        adjust_volume(OUTPUT_FILENAME, OUTPUT_FILENAME, -16.0)

        afterRecord()

def stop_rec():
    global stop_recording
    stop_recording = True
    stop_playback()
