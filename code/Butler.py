 # * author : Philippe Vo 
 # * date : Sep-28-2019 22:00:11

# * Imports
# 3rd Party Imports
import datetime
from gtts import gTTS # text to speech
import os
# User Imports
from Weather import Weather
from Schedule import Schedule
from Timer import Timer

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
        datetimeInfo = datetime.datetime.now()
        self.date = datetimeInfo.strftime("%A, %B %d %Y")
        self.time = datetimeInfo.strftime("%X")
        self.hour = int(datetimeInfo.hour)

        # Weather Info
        weatherController = Weather()
        self.weatherInfo = weatherController.get_weather_data()
        self.clothingInfo = weatherController.get_clothing_data()
        self.generalWeatherStatus = weatherController.get_weather_status()

        # Schedule Info
        scheduleController = Schedule()
        self.timeToLeave = scheduleController.hourBLH + " hours" + " and " + scheduleController.mBLH + " mins"

    def report(self): 
        """ report status of day """
        # Report
        self.text_to_speech(self.generate_greeting())
        self.text_to_speech("Today is " + self.date)
        self.text_to_speech("The current time is " + self.time)
        self.text_to_speech(self.process_weather_info())
        print("\n")
        self.text_to_speech("You have " + self.timeToLeave + " before leaving the house")

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

    def text_to_speech(self, text):
        """ converts the text into speech and speaks it """
        # prints the speech
        print(text)

        # define variables
        file = "file.mp3"

        # initialize tts, create mp3 and play
        tts = gTTS(text, 'en')
        tts.save(file)
        os.system("mpg123 " + file + " >/dev/null 2>&1") # >dev/null... it is to supress the output string from the command 

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
        self.text_to_speech("You needed a timer Sifu Nam ?")
        self.text_to_speech("Please press on ENTER to begin the timer")
        timer = Timer()
        printOut , message = timer.run_timer(mode, timeType, endTime)
        # sound alarm and speak the message 
        os.system("mpg123 " + " /home/namv/Documents/Personal_Projects/Personal_Board/alarm.mp3 " + " >/dev/null 2>&1") # >dev/null... it is to supress the output string from the command 
        self.text_to_speech(printOut)
        self.text_to_speech(message)