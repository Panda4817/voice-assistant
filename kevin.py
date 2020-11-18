import speech_recognition as sr

from util import fix_transcription, identify_task, print_help
from talking_engine import engine_say

# Introduce kevin
engine_say("Hello, I am KEVIN. How can I help you?")

# obtain audio from the microphone
s = sr.Recognizer()
with sr.Microphone() as source:
    audio = s.listen(source, timeout=5)

# recognize speech using Google Speech Recognition
try:
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    transcribed = fix_transcription(s.recognize_google(audio))
    
    task_words = transcribed.split(" ")
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

