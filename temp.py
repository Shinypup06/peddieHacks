from pydub import AudioSegment

def adjust_volume(input_file, output_file, target_dBFS):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)
    
    # Calculate the difference between the target dBFS and the current dBFS
    change_in_dBFS = target_dBFS - audio.dBFS
    
    # Apply the gain change to the audio
    adjusted_audio = audio.apply_gain(change_in_dBFS)
    
    # Export the adjusted audio
    adjusted_audio.export(output_file, format='wav')

# Example usage
input_file = 'output.wav'
output_file = 'output.wav'
target_dBFS = -16.0  # Target volume in dBFS

adjust_volume(input_file, output_file, target_dBFS)