import pygame
from pydub import AudioSegment

def play_file(input):
    pygame.mixer.music.load(input)
    pygame.mixer.music.play()

def stop_playback():
    pygame.mixer.music.stop()

# adjusts volume to a certain target dBFS
def adjust_volume(input, output, target_dBFS):
    audio = AudioSegment.from_file(input)
    change_in_dBFS = target_dBFS - audio.dBFS
    adjusted_audio = audio.apply_gain(change_in_dBFS)
    adjusted_audio.export(output, format='wav')