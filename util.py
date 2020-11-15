import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 125)

def engine_say(text):
    engine.say(text)
    engine.runAndWait()

def fix_transcription(transcribed):
    # fix maths symbols
    if 'x' in transcribed.split(" "):
        transcribed = transcribed.replace('x', 'multiplied by')
    if '+' in transcribed.split(" "):
        transcribed = transcribed.replace('+', 'add')
    if '-' in transcribed.split(" "):
        transcribed = transcribed.replace('-', 'subtract')
    if '/' in transcribed.split(" "):
        transcribed = transcribed.replace('/', 'divided by')
    return transcribed

def identify_task(transcribed):
    task = ''
    if 'song' in transcribed.split(" "):
        task = 'song'
    if 'answer' in transcribed.split(" "):
        task ='answer'
    if 'spell' in transcribed.split(" "):
        task = 'spell'
    return task
