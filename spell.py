from kevin.util import engine_say

def spell_word(text):
    words = text.split(" ")
    for w in words:
        if w is '':
            continue
        engine_say(w)
        letters = w.split("")
        for l in letters:
            engine_say(l)
    return True