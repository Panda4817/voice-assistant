from answer import Find_answer
from song import Find_song
from spell import Spell_word
from date_time import Say_date_time
from help import Help

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

def identify_task(task_word):
    task = ''
    if 'song' == task_word:
        task = Find_song()
    if 'answer' == task_word:
        task = Find_answer()
    if 'spell' == task_word:
        task = Spell_word()
    if 'time' == task_word or 'date' == task_word:
        task = Say_date_time()
    if 'help' == task_word:
        task = Help()
    return task

# def random greeting generator