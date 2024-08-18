import requests
import json
import re
import whisper

def getInternetLyrics(artist, track):
    r = requests.get('https://api.lyrics.ovh/v1/' + artist + '/'+ track)
    data = json.loads(r.content)
    s = r.content
    try: #removes message before lyrics from api
        lyrics = re.sub("Paroles de la chanson .* par .*","",data["lyrics"])
    except: #in case the song is not in the library
        lyrics = "No lyrics found."
    return (lyrics)


def getLyrics(file):
    lyrics = whisper.load_model("base").transcribe(file)["text"]
    
    # split into new lines whenever punctuation is encountered
    lyrics = lyrics.replace('.', '\n').replace(',', '\n').replace('?', '?\n').replace('\n ', '\n')

    return lyrics
