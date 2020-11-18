from talking_engine import engine_say

class Spell_word:
    def run(self, text, audio):
        spelled = []
        words = text.split(" ")
        for w in words:
            if w == '' or w in spelled:
                continue
            engine_say(w)
            for l in w:
                engine_say(l)
            spelled.append(w)
