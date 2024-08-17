import requests
import json
import re

def getInternetLyrics(artist, track):
    # artist = 'Fall Out Boy'
    # track = 'Sugar, We\'re Going Down'

    r = requests.get('https://api.lyrics.ovh/v1/' + artist + '/'+ track)
    data = json.loads(r.content)
    s = r.content
    try:
        lyrics = re.sub("Paroles de la chanson .* par .*","",data["lyrics"])
    except:
        lyrics = "No lyrics found."

    # print(r.content)
    return (lyrics)

# getlyrics('Casey Edwards','Bury the Light')