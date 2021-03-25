from talking_engine import engine_say

class Help:
    def __init__(self):
        self.help_text = [
            "Hello I am KEVIN. Kanta's Eccentric, Vastly Intelligent Natural voice assistant.",
            "Say song, then play a tune or say lyrics, to search for song names.",
            "Say answer, then ask a question.",
            "Say time or date, for today's date and time.",
            "Say spell, then the word or words you would like Kevin to spell.",
            "Say help if you you would like information on commands,"
        ]

    def print_help(self):
        for sentence in self.help_text:
            print(sentence)
    
    def say_help_text(self):
        for sentence in self.help_text:
            engine_say(sentence)

    def run(self, text, audio):
        self.print_help()
        self.say_help_text()