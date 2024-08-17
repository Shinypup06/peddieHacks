import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def filter_audio(input_file, output_file, lowcut, highcut):
    # Read the audio file
    fs, data = wavfile.read(input_file)

    # Apply the bandpass filter
    filtered_data = butter_bandpass_filter(data, lowcut, highcut, fs)

    # Ensure the output is in the correct format (e.g., 16-bit PCM)
    filtered_data = np.int16(filtered_data / np.max(np.abs(filtered_data)) * 32767)

    # Save the filtered audio
    wavfile.write(output_file, fs, filtered_data)

# Example usage
input_file = 'sampleAudios/mammamiavoice.wav'
output_file = 'filtered_audio.wav'
lowcut = 200.0  # Low cutoff frequency in Hz
highcut = 1500.0  # High cutoff frequency in Hz

filter_audio(input_file, output_file, lowcut, highcut)