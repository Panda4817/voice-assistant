import speech_recognition as sr
import pyttsx3
import requests
import os
import base64
import pprint
import urllib

from bs4 import BeautifulSoup

from dotenv import load_dotenv
load_dotenv()

engine = pyttsx3.init()
engine.setProperty('rate', 125)

def engine_say(text):
    engine.say(text)
    engine.runAndWait()

# obtain audio from the microphone
s = sr.Recognizer()
engine_say("Hello I am KEVIN. Kanta's Excellent Vastly Intelligent Natural A.I.")
engine_say("I can search for songs or answer your question. Say song, then play a tune or say lyrics. Or, say answer, then ask a question.")
with sr.Microphone() as source:
    audio = s.listen(source, timeout=5)

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    transcribed = s.recognize_google(audio)

    if 'x' in transcribed.split(" "):
        transcribed = transcribed.replace('x', 'multiplied by')
    elif '+' in transcribed.split(" "):
        transcribed = transcribed.replace('+', 'add')
    elif '-' in transcribed.split(" "):
        transcribed = transcribed.replace('-', 'subtract')
    elif '/' in transcribed.split(" "):
        transcribed = transcribed.replace('/', 'divided by')
    engine_say("Google Speech Recognition thinks you said " + transcribed)
    
    print(transcribed)
    if 'song' in transcribed.split(" "):
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
            engine_say("I could not find the song title.")
        else:
            r = response.json()
            if r["matches"]:
                engine_say(r["track"]["title"])
                engine_say(r["track"]["subtitle"])
                print(r["track"]["title"], ' - ', r["track"]["subtitle"])
            else:
                engine_say("Shazam found no matches for the tune. I will try searching for lyrics.") 

                # Find song title and artist by the lyrics or title
                text = transcribed.split("song ")
                song_url = 'https://songsear.ch/q/' + text[1]
                page = requests.get(song_url)
                soup = BeautifulSoup(page.content, 'html.parser')
                song_by_name = soup.find(class_='by-name')
                if song_by_name:
                    engine_say("songs with the title " + text[1])
                    for name in song_by_name.find_all('a'):
                        engine_say(name.text)
                        print(name.text)
                other_songs = soup.find(class_='results')
                if other_songs:
                    engine_say("Top 10 songs with the lyrics " + text[1])
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

    elif 'answer' in transcribed.split(" "):
        text = transcribed.split("answer ")
        print(text)
        url_str = urllib.parse.urlencode({'q': text[1]})
        google_url = "https://google-search3.p.rapidapi.com/api/v1/crawl/" + url_str
        headers = {
        'x-rapidapi-key': os.getenv("API_KEY"),
        'x-rapidapi-host': "google-search3.p.rapidapi.com"
        }

        response = requests.request("GET", google_url, headers=headers)
        r_json = response.json()
        soup = BeautifulSoup(r_json['html'], 'html.parser')
        featured = soup.find(class_='hgKElc')
        calc = soup.find('div', class_='fB3vD')
        dic = soup.find('div', class_='vmod')
        people = soup.find_all(class_='dAassd')
        recipe = soup.find_all(class_='v1uiFd')
        synopis = soup.find(class_='DI6Ufb')
        if featured or calc or dic or people or recipe or synopis:
            if featured is not None: engine_say(featured.text)
            if calc is not None: engine_say(calc.text)
            if dic is not None: engine_say(dic.text)
            if synopis is not None: engine_say(synopis.text)
            if people is not None:
                for p in people:
                    engine_say(p.text)
            if recipe is not None:
                for r in recipe:
                    engine_say(r.text)
                    print(r.text)
        elif r_json['results']:
            answer = False
            for res in r_json['results']:
                if 'wikipedia' in res['title'].lower():
                    arr = res['title'].split(' - ')
                    print(arr)
                    engine_say(arr[0])
                    arr2 = res['description'].split('.')
                    print(arr2)
                    engine_say(arr2[0])
                    answer = True
            if answer is False:
                for res in r_json['results']:
                    if res['description'] != '':
                        arr = res['title'].split(' - ')
                        print(arr)
                        engine_say(arr[0])
                        arr2 = res['description'].split('.')
                        print(arr2)
                        engine_say(arr2[0])
            
        else:
            engine_say("Sorry Google does not know the answer")
    else:
        engine_say("Sorry I am not programmed to do that yet.")


except sr.UnknownValueError:
    engine_say("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    engine_say("Could not request results from Google Speech Recognition service; {0}".format(e))

