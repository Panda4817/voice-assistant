import speech_recognition as sr

from util import fix_transcription, identify_task
from talking_engine import engine_say

# obtain audio from the microphone
s = sr.Recognizer()
print("Hello I am KEVIN. Kanta's Eccentric, Vastly Intelligent Natural A.I.")
print("Say song, then play a tune or say lyrics, to search for song names.") 
print("Say answer, then ask a question.")
print("Say time or date, for today's date and time.")
print("Say spell, then the word or words you would like Kevin to spell.")
#engine_say("Hello, I am KEVIN. How can I help you?")
with sr.Microphone() as source:
    audio = s.listen(source, timeout=5)

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    transcribed = fix_transcription(s.recognize_google(audio))
    #engine_say("Google Speech Recognition thinks you said " + transcribed)
    print(transcribed)
    
    task_words = transcribed.split(" ")
    print(task_words)
    task = identify_task(task_words[0])
    main_text = " ".join(task_words[1:])
    try:
        task.run(main_text, audio)
    except Exception as e:
        print(e)
        engine_say("Sorry I am not programmed to do that yet.")

except sr.UnknownValueError:
    engine_say("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    engine_say("Could not request results from Google Speech Recognition service; {0}".format(e))

