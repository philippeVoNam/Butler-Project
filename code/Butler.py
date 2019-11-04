 # * author : Philippe Vo 
 # * date : Sep-28-2019 22:00:11

# * Imports
# 3rd Party Imports
import datetime
from gtts import gTTS # text to speech
import os
import time
from termcolor import colored, cprint
from datetime import datetime
import sys
import notify2
import subprocess
# User Imports
from Weather import Weather
from Schedule import Schedule
from Timer import Timer
from Screenshot import Screenshot

# * Code
class Butler():
    """
    - greets 
        - different greets depend on the time of day
        - morning = after 6am and before 12pm
        - afternoon = after 12pm and before 6pm
        - night = after 6pm  and before 6am
    - tells the current time
    - manages weather info
    """
    def __init__(self):
        """ init the variables """
        # Greetings
        self.greeting = "Hey there Sifu Nam !"
        self.masterName = "Sifu Nam"

        # Datetime
        datetimeInfo = datetime.now()
        self.date = datetimeInfo.strftime("%A, %B %d %Y")
        self.time = datetimeInfo.strftime("%X")
        self.hour = int(datetimeInfo.hour)

        # Weather Info
        weatherController = Weather()
        self.weatherInfo = weatherController.get_weather_data()
        self.clothingInfo = weatherController.get_clothing_data()
        self.generalWeatherStatus = weatherController.get_weather_status()

        # Schedule Info
        self.scheduleController = Schedule()
        self.timeToLeave = self.scheduleController.hourBLH + " hours" + " and " + self.scheduleController.mBLH + " mins"

    def report(self): 
        """ report status of day """
        # Report
        self.text_to_speech(self.generate_greeting(), False)
        self.text_to_speech("Today is " + self.date, False)
        self.text_to_speech("The current time is " + self.time, False)
        self.text_to_speech(self.process_weather_info(), False)
        print("\n")
        self.text_to_speech("You have " + self.timeToLeave + " before leaving the house", False)

    def generate_greeting(self) :
        """ generates a greeting based on time """
        # time process
        if self.hour > 6 and self.hour <= 12 :
            greetingWord = "Good Morning "
        elif self.hour > 12 and self.hour <= 18 :
            greetingWord = "Afternoon there "
        else :
            greetingWord = "Lovely Night there " 

        self.greeting = greetingWord + self.masterName

        return self.greeting

    def text_to_speech(self, text, talkFlag):
        """ converts the text into speech and speaks it """
        # prints the speech
        print(text)
        
        if talkFlag:
            # define variables
            file = "file.mp3"

            # initialize tts, create mp3 and play
            tts = gTTS(text, 'en')
            tts.save(file)
            os.system("mpg123 " + file + " >/dev/null 2>&1") # >dev/null... it is to supress the output string from the command 
        else:
            time.sleep(0.35)

    def process_weather_info(self):
        """ get weather and tells what is needed for the day """
        # Weather info
        weatherInfoStr = """
        the Weather of Today :
        current temperature is {currentTemp} degrees
        maximum temperature is {maxTemp} degrees
        minimum temperature is {minTemp} degrees

        """.format(currentTemp=self.weatherInfo[1], maxTemp = self.weatherInfo[0], minTemp = self.weatherInfo[2])

        # Clothing Status
        if self.clothingInfo[2] == True :
            clothingInfoStr = "you should wear a coat today, its freezing outside"
        elif self.clothingInfo[1] == True :
            clothingInfoStr = "you should wear a jacket today, its cold outside"
        elif self.clothingInfo[0] == True :
            clothingInfoStr = "you should wear a sweater today, its chilly outside"
        else :
            clothingInfoStr = "today's weather looks great, t-shirt should be fine"

        if self.clothingInfo[3] == True :
            umbrellaStr = "\tmaybe you should take your umbrella with you, it is probably going to rain"

        return weatherInfoStr + clothingInfoStr + "\n" + umbrellaStr

    def run_timer(self, mode, timeType, endTime):
        """ runs the timer and speaks the message at the end """
        self.text_to_speech("You needed a timer Sifu Nam ?", False)
        self.text_to_speech("Please press on ENTER to begin the timer", False)
        timer = Timer()
        printOut , message = timer.run_timer(mode, timeType, endTime)
        # sound alarm and speak the message 
        os.system("mpg123 " + " /home/namv/Documents/Personal_Projects/Personal_Board/alarm.mp3 " + " >/dev/null 2>&1") # >dev/null... it is to supress the output string from the command 
        self.text_to_speech(printOut, False)
        self.text_to_speech(message, False)

    def grab_screen(self):
        """ takes a screenshot and return the markdown string in the system clipboard """
        print("May I take a Screenshot for you Sifu ?")
        screengrab = Screenshot()
        screengrab.grab_screen()

    def announce_current_task(self):
        """ prints out the current task I should be doing """
        task = self.scheduleController.current_task()

        message = "Started Task : " +  task["task"]
        self.notify("Task Status",message)

        taskName = "Task Name : " + colored(task["task"], 'red', attrs=['bold'])
        startTime = "Start Time : " + colored(task["startTime"], 'blue', attrs=['bold'])
        endTime = "End Time : " + colored(task["endTime"], 'green', attrs=['bold'])

        self.text_to_speech(taskName, False)
        self.text_to_speech(startTime, False)
        self.text_to_speech(endTime, False)

        now = datetime.now()
        endTime = task["endTime"].split(":")
        endTime = now.replace(hour=int(endTime[0]), minute=int(endTime[1]), second=0, microsecond=0)
        
        while now < endTime:
            now = datetime.now()
            endTime = task["endTime"].split(":")
            endTime = now.replace(hour=int(endTime[0]), minute=int(endTime[1]), second=0, microsecond=0)
            durationRemaining = str(endTime - now)
            durationRemaining = "Duration Remaining : " + colored(durationRemaining, 'white', attrs=['bold'])
            print(durationRemaining, end="\r", flush=True)
            time.sleep(1)

        # Task Done messages
        print("")
        print("Task Done")

        message = "Done with : " +  task["task"]
        self.notify("Task Status",message)

    def show_day_tasks(self):
        """ prints out the task of the day """ 
        print(self.scheduleController.day_tasks())

    def notify(self, title, message):

        notify2.init(title)
        n = notify2.Notification(title, message)
        n.show()
        
    def convertMD2PDF(self, mdFile):
        """ converts the given md file into a pdf file """
        mdFileStr = mdFile + ".md"
        pdfFileStr = mdFile + ".pdf"
        command = "pandoc -o " + pdfFileStr + " " + mdFileStr + " -f markdown-implicit_figures"
        print(command)
        os.system(command)