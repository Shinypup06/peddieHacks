import whisper

def getLyrics(file):
    lyrics = whisper.load_model("base").transcribe(file)["text"]
    
    # split into new lines whenever punctuation is encountered
    lyrics = lyrics.replace('.', '\n').replace(',', '\n').replace('?', '?\n').replace('\n ', '\n')

    return lyrics