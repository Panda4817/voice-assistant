import speech_recognition as sr

from util import *
from song import *
from answer import *
from spell import *

# obtain audio from the microphone
s = sr.Recognizer()
#engine_say("Hello I am KEVIN. Kanta's Eccentric, Vastly Intelligent Natural A.I.")
#engine_say("I can search for songs or answer your question. Say song, then play a tune or say lyrics. Or, say answer, then ask a question.")
with sr.Microphone() as source:
    audio = s.listen(source, timeout=5)

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    transcribed = fix_transcription(s.recognize_google(audio))
    engine_say("Google Speech Recognition thinks you said " + transcribed)
    print(transcribed)
    
    task = identify_task(transcribed)
    main_text = " ".join(transcribed.split(" ")[1:])
    if task == 'song': find_song(main_text, audio)
    elif task == 'answer': find_answer(main_text)   
    elif task == 'spell': spell_word(main_text) 
    else: engine_say("Sorry I am not programmed to do that yet.")

except sr.UnknownValueError:
    engine_say("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    engine_say("Could not request results from Google Speech Recognition service; {0}".format(e))

