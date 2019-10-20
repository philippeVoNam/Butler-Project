import json

timeList = []

with open('data.json') as json_file:
    data = json.load(json_file)
    for p in data['Saturday']:
        timeList.append(p)

# 3rd Party Imports
from datetime import datetime, timedelta
now = datetime.now()

def get_current_time():
    """ get current time in HH:MM format """
    now = datetime.now()
    
    return now.strftime("%H:%M")

def time_lessThan(timeIn):
    """ compares the current time with the given time (input is string)"""
    # convert time string to datetime
    now = datetime.now()
    timeIn = timeIn.split(":")
    timeIn = now.replace(hour=int(timeIn[0]), minute=int(timeIn[1]), second=0, microsecond=0)
    
    return now < timeIn

def current_task(timeList):
    """ get the current task depending on the current time """

    for idx, val in enumerate(timeList):
        if time_lessThan(val['startTime']):
            timeIndex = idx - 1 # get the previous one
            task = timeList[timeIndex]
            break
    
    return task

print("Current Task")
print(current_task(timeList))