import os
import urllib

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

from util import engine_say

def find_answer(text):
    # Get google results
    print(text)
    url_str = urllib.parse.urlencode({'q': text})
    google_url = "https://google-search3.p.rapidapi.com/api/v1/crawl/" + url_str
    headers = {
    'x-rapidapi-key': os.getenv("API_KEY"),
    'x-rapidapi-host': "google-search3.p.rapidapi.com"
    }

    # Parse results using BeautifulSoup
    response = requests.request("GET", google_url, headers=headers)
    r_json = response.json()
    soup = BeautifulSoup(r_json['html'], 'html.parser')
    
    # Get to useful information
    useful_info = []
    useful_info.append(soup.find(class_='hgKElc'))
    useful_info.append(soup.find('div', class_='fB3vD'))
    useful_info.append(soup.find('div', class_='vmod'))
    useful_info.append(soup.find_all(class_='dAassd'))
    useful_info.append(soup.find_all(class_='v1uiFd'))
    useful_info.append(soup.find(class_='DI6Ufb'))
    useful_info.append(soup.find(class_='webanswers-webanswers_table__webanswers-table'))
    useful_info.append(soup.find(class_='X5LH0c'))
    useful_info.append(soup.find_all(class_='junCMe'))
    
    # Say useful information
    for i in useful_info:
        if i and isinstance(i, list):
            for ii in i:
                print(ii.text)
                engine_say(ii.text)
            return True
        if i:
            print(i.text)
            engine_say(i.text)
            return True
    
    
    # Check for results
    if not r_json['results']:
        engine_say("Sorry Google does not know the answer")
        return False
    
    # Say the wikipedia result first
    answer = False
    for res in r_json['results']:
        if 'wikipedia' in res['title'].lower():
            arr = res['title'].split(' - ')
            print(arr[0])
            engine_say(arr[0])
            arr2 = res['description'].split('.')
            print(arr2[0])
            engine_say(arr2[0])
            answer = True
    
    # Check wikipedia answer provided
    if answer is True:
        return True
    
    # Provide other answers (fix with more intelligent AI)
    for res in r_json['results']:
        if res['description'] != '':
            arr = res['title'].split(' - ')
            print(arr)
            engine_say(arr[0])
            arr2 = res['description'].split('.')
            print(arr2)
            engine_say(arr2[0])