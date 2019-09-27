"""
author : Philippe Vo
date : 2019-September-27 19:37:46
"""

# * Imports

# * Code

import pyowm

owm = pyowm.OWM('c9ff246e7d7fb123387433a19c436e14')  # You MUST provide a valid API key

# Search for current weather in London (Great Britain)
observation = owm.weather_at_place('London,GB')
w = observation.get_weather()
print(w)    

# class Weather():
#     """
#     - fetches weather data
#     - processes weather data
#     """
#     def __init__(self):


        
