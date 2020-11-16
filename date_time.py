from talking_engine import engine_say
from datetime import date, datetime

class Say_date_time:
    def run(self, text, audio):
        engine_say("The date is " + date.today().strftime("%A %B %d, %Y"))
        engine_say("The time is " + datetime.now().strftime("%I %M %p"))
