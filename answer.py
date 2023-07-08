from talking_engine import engine_say
import os
import urllib

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


class Find_answer:
    def crawl_google(self, text):
        # Get google results
        print(text)
        url_str = urllib.parse.urlencode({"q": text})
        google_url = "https://google-search3.p.rapidapi.com/api/v1/crawl/" + url_str
        headers = {
            "x-rapidapi-key": os.getenv("API_KEY"),
            "x-rapidapi-host": "google-search3.p.rapidapi.com",
        }

        # Parse results using BeautifulSoup
        response = requests.request("GET", google_url, headers=headers)
        r_json = response.json()

        return r_json

    def parse_google(self, res):
        # Get soup
        soup = BeautifulSoup(res["html"], "html.parser")

        # Get to useful information
        useful_info = []
        useful_info.append(soup.find(class_="hgKElc"))
        useful_info.append(soup.find("div", class_="fB3vD"))
        useful_info.append(soup.find("div", class_="vmod"))
        useful_info.append(soup.find_all(class_="dAassd"))
        useful_info.append(soup.find_all(class_="v1uiFd"))
        useful_info.append(soup.find(class_="DI6Ufb"))
        useful_info.append(
            soup.find(class_="webanswers-webanswers_table__webanswers-table")
        )
        useful_info.append(soup.find(class_="X5LH0c"))
        useful_info.append(soup.find_all(class_="junCMe"))

        return useful_info

    def say_parsed_info(self, info):
        # Say useful information
        for i in info:
            if i and isinstance(i, list):
                for ii in i:
                    print(ii.text)
                    engine_say(ii.text)
                return True
            if i:
                print(i.text)
                engine_say(i.text)
                return True
        return False

    def say_wikipedia(self, results):
        # Say the wikipedia result first
        answer_provided = False
        for res in results:
            if "wikipedia" in res["title"].lower():
                engine_say("From wikipedia")
                arr = res["title"].split(" - ")
                print(arr[0])
                engine_say(arr[0])
                arr2 = res["description"].split(".")
                print(arr2[0])
                engine_say(arr2[0])
                answer_provided = True

        return answer_provided

    def other_answer(self, results):
        # Provide other answers
        for res in results["results"]:
            if res["description"] != "":
                arr = res["title"].split(" - ")
                print(arr)
                engine_say(arr[0])
                arr2 = res["description"].split(".")
                print(arr2)
                engine_say(arr2[0])

    def run(self, text, audio):
        # Get google results
        r_json = self.crawl_google(text)
        useful_info = self.parse_google(r_json)

        # Check if answer was provided
        if self.say_parsed_info(useful_info):
            return

        # Check for results section of response
        if not r_json["results"]:
            engine_say("Sorry Google does not know the answer")
            return

        # Check if wikipedia answer was provided
        if self.say_wikipedia(r_json["results"]):
            return

        # Provide another answer
        self.other_answer(r_json["results"])
