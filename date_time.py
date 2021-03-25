from talking_engine import engine_say
from datetime import date, datetime

class Say_date_time:
    def run(self, text, audio):
        d = "The date is " + date.today().strftime("%A %B %d, %Y")
        
        # Get year in the form of two numbers so voice assistant can say it the two numbers that make up the year
        lst = d.split()
        year1 = lst[-1][0:2]
        year2 = lst[-1][2:]
        lst.pop()
        lst.append(year1)
        lst.append(year2)
        d = " ".join(lst)
        engine_say(d)
        engine_say("The time is " + datetime.now().strftime("%I %M %p"))
