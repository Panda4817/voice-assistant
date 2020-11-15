import os
import base64

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

from util import engine_say


def shazam_it(audio):
    # Find song matches through shazam
    url = "https://shazam.p.rapidapi.com/songs/detect"

    raw_data=audio.get_wav_data()
    byteslist = bytearray(raw_data)
    data = base64.b64encode(byteslist)
    payload = data
    headers = {
        'content-type': "text/plain",
        'x-rapidapi-key': os.getenv("API_KEY"),
        'x-rapidapi-host': "shazam.p.rapidapi.com"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code != 200:
        return False
    
    r = response.json()
    if not r["matches"]:
        engine_say("Shazam found no matches for the tune. I will try searching for lyrics.")
        return False
    
    engine_say(r["track"]["title"])
    engine_say(r["track"]["subtitle"])
    print(r["track"]["title"], ' - ', r["track"]["subtitle"])
    return True

def crawl_songsear(text):
    # Find song title and artist by the lyrics or title
    song_url = 'https://songsear.ch/q/' + text
    page = requests.get(song_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    song_by_name = soup.find(class_='by-name')
    if song_by_name:
        engine_say("songs with the title " + text)
        for name in song_by_name.find_all('a'):
            engine_say(name.text)
            print(name.text)
    other_songs = soup.find(class_='results')
    if other_songs:
        engine_say("Top 10 songs with the lyrics " + text)
        x = 0
        for song in other_songs.find_all(class_='head'):
            x += 1
            if x > 10:
                break
            h2 = song.find('h2')
            engine_say(h2.text)
            h3 = song.find('h3')
            engine_say(h3.text)
            print(h2.text, " - ", h3.text)
        return True
    return False

def find_song(text, audio):
    if shazam_it(audio):
        return True
    if crawl_songsear(text):
        return True
    
    engine_say("I could not find the song title.") 
    return False