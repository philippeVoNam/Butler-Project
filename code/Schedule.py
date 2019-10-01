 # * author : Philippe Vo 
 # * date : Sep-29-2019 00:16:14
 
# * Imports
# 3rd Party Imports
from datetime import datetime, timedelta
# User Imports

# * Code
class Schedule():
    """
    - fetches my schedule
    - processes schedule data

    """
    def __init__(self):
        """ init schedule """
        now = datetime.now()

        self.firstClassTime = {
            "Monday" : datetime.strptime(str(now.date()) + " 08:45", '%Y-%m-%d %H:%M'),
            "Tuesday" : datetime.strptime(str(now.date()) + " 08:45", '%Y-%m-%d %H:%M'),
            "Wednesday" : datetime.strptime(str(now.date()) + " 10:00", '%Y-%m-%d %H:%M'),
            "Thursday" : datetime.strptime(str(now.date()) + " 10:00", '%Y-%m-%d %H:%M'),
            "Friday" : datetime.strptime(str(now.date()) + " 08:45", '%Y-%m-%d %H:%M'),
            "Saturday" : datetime.strptime(str(now.date()) + " 10:00", '%Y-%m-%d %H:%M'),
            "Sunday" : datetime.strptime(str(now.date()) + " 10:00", '%Y-%m-%d %H:%M')
        }

        self.timeToLeave = self.firstClassTime[now.strftime("%A")] - timedelta(hours=1,minutes=30) 
        self.timeBeforeLeavingHouse = str(self.timeToLeave - now)
        self.timeBeforeLeavingHouse = self.timeBeforeLeavingHouse.split(":")
        self.hourBLH, self.mBLH, self.sBLH = [self.timeBeforeLeavingHouse[0],self.timeBeforeLeavingHouse[1],self.timeBeforeLeavingHouse[2]]