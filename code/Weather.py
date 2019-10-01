"""
author : Philippe Vo
date : 2019-September-27 19:37:46
"""

# * Imports
import pyowm

# * Code
class Weather():
    """
    - fetches weather data
    - processes weather data

    useful information needed :
    - max temp
    - current temp
        - need sweater ? (less than 20.C)
        - need jacket ? (less than 10.C)
        - need coat ? (less than 5.C)
    - min temp
    - will it rain ?
        - need umbrella or no ?
    - general status

    type of data :
    - weather data
    - clothing data (based upon the weather data -> clothing needed)
    """
    def __init__(self):
        """ init the variables """
        # Temperatures and Rain
        self.maxTemp = 0
        self.currentTemp = 0
        self.minTemp = 0
        self.rainStatus = False

        self.weatherData = []

        # Clothing Options
        self.sweaterNeed = False
        self.jacketNeed = False
        self.coatNeed = False
        self.umbrellaNeed = False

        self.clothingData = []

        # Connecting with pyowm
        owm = pyowm.OWM('c9ff246e7d7fb123387433a19c436e14')  # You MUST provide a valid API key
        observation = owm.weather_at_place('Montreal,CA')
        self.forecast = owm.three_hours_forecast('Montreal,CA')
        self.weather = observation.get_weather()  

        # General Status    
        self.generalWeatherStatus = self.weather.get_detailed_status()     

        # Getting and Processing Weather info 
        self.get_weather_info()
        self.process_weather_info()

    def get_weather_info(self):
        """ fetch weather data from pyowm """
        temp = self.weather.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
        self.maxTemp = temp['temp_max']
        self.currentTemp = temp['temp']
        self.minTemp = temp['temp_min']
        self.rainStatus = self.forecast.will_have_rain()

        self.weatherData.append(self.maxTemp)
        self.weatherData.append(self.currentTemp)
        self.weatherData.append(self.minTemp)
        self.weatherData.append(self.rainStatus)

        return self.weatherData

    def process_weather_info(self):
        """ processes the weather and generates the clothing needed """
        # Clothing needed
        if self.currentTemp < 20 and self.currentTemp >=10 :
            self.sweaterNeed = True
        elif self.currentTemp < 10 and self.currentTemp >=5 :
            self.jacketNeed = True
        elif self.currentTemp < 5 :
            self.coatNeed = True

        if self.rainStatus == True :
            self.umbrellaNeed = True
        elif self.rainStatus == False : 
            self.umbrellaNeed = False
            
        self.clothingData.append(self.sweaterNeed)
        self.clothingData.append(self.jacketNeed)
        self.clothingData.append(self.coatNeed)
        self.clothingData.append(self.umbrellaNeed)

        return self.clothingData

    def get_weather_data(self):
        return self.weatherData

    def get_clothing_data(self):
        return self.clothingData

    def get_weather_status(self):
        return self.generalWeatherStatus

if __name__ == "__main__":
    weatherController = Weather()






        
