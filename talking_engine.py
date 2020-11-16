import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 125)

def engine_say(text):
    engine.say(text)
    engine.runAndWait()