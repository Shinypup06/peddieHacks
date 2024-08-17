import requests
from bs4 import BeautifulSoup

def search_lyrics_lyricsgenius(query):
    headers = {'User-Agent': 'Mozilla/5.0'}
    search_url = f"https://genius.com/search?q={query.replace(' ', '%20')}"
    print(search_url)
    response = requests.get(search_url, headers=headers)
    print(response.status_code)


    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Look for the first search result
        result = soup.find('div', class_='mini_song_card')
        if result and result.find('a'):
            song_url = result.find('a')['href']
            return get_lyrics_genius(song_url)
        else:
            print("No lyrics found.")
            return None
    else:
        print(f"Error: Received status code {response.status_code}")
        return None

def get_lyrics_genius(song_url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(song_url, headers=headers)
    

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Look for the lyrics container, updated with Genius site structure
        lyrics_div = soup.find('div', {'data-lyrics-container': "true"})
        if lyrics_div:
            lyrics = lyrics_div.get_text(separator="\n")
            return lyrics
        else:
            return "Lyrics not found."
    else:
        print(f"Error: Received status code {response.status_code}")
        return None

def main():
    misheard_lyrics = "I want it that way"
    real_lyrics = search_lyrics_lyricsgenius(misheard_lyrics)
    
    if real_lyrics:
        print("Real Lyrics:")
        print(real_lyrics)
    else:
        print("No lyrics could be retrieved.")

if __name__ == "__main__":
    main()
