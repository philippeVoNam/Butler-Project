 # * author : Philippe Vo 
 # * date : Sep-29-2019 00:16:14
 
# * Imports
# 3rd Party Imports
from datetime import datetime, timedelta
import json
from terminaltables import AsciiTable
from termcolor import colored, cprint
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

        # Read in the schedule data json file of TODAY
        self.todayTasks = []
        with open('/home/namv/Documents/Personal_Projects/Personal_Board/code/Schedule_Data/schedule.json') as json_file:
            data = json.load(json_file)
            for p in data[now.strftime("%A")]:
                self.todayTasks.append(p)

    def current_task(self):
        """ get the current task depending on the current time """

        for idx, val in enumerate(self.todayTasks):
            if self.time_lessThan(val['startTime']):
                timeIndex = idx - 1 # get the previous one
                task = self.todayTasks[timeIndex]
                break
        
        return task

    def day_tasks(self):
        """ shows the schedule of the day in a table format"""
        tableData = [['Start Time', 'Task', 'End Time']]

        firstFind = True

        for idx, task in enumerate(self.todayTasks):
            if self.time_lessThan(task['startTime']) and firstFind:
                currentTaskIndex = idx - 1 # get the previous one
                firstFind = False
            taskData = []
            taskData.append(task["startTime"])
            taskData.append(task["task"])
            taskData.append(task["endTime"])

            tableData.append(taskData)

        tableData[currentTaskIndex][0] = colored(self.todayTasks[currentTaskIndex]["startTime"], 'red', attrs=['bold'])
        tableData[currentTaskIndex][1] = colored(self.todayTasks[currentTaskIndex]["task"], 'white', 'on_red', attrs=['bold'])
        tableData[currentTaskIndex][2] = colored(self.todayTasks[currentTaskIndex]["endTime"], 'green', attrs=['bold'])

        table = AsciiTable(tableData)

        return table.table
    
    def time_lessThan(self, timeIn):
        """ compares the current time with the given time (input is string)"""
        # convert time string to datetime
        now = datetime.now()
        timeIn = timeIn.split(":")
        timeIn = now.replace(hour=int(timeIn[0]), minute=int(timeIn[1]), second=0, microsecond=0)
        
        return now < timeIn
