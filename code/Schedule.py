 # * author : Philippe Vo 
 # * date : Sep-29-2019 00:16:14
 
# * Imports
# 3rd Party Imports
from datetime import datetime, timedelta
import json
from terminaltables import AsciiTable
from termcolor import colored, cprint
import sys
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
        dayFinished = True

        for idx, task in enumerate(self.todayTasks):
            if self.time_between(task['startTime'], task['endTime']):
                timeIndex = idx
                task = self.todayTasks[timeIndex]
                dayFinished = False
                break
        
        if dayFinished:
            print("You do not have any other tasks today :) ")
            sys.exit()
        
        return task

    def day_tasks(self):
        """ shows the schedule of the day in a table format"""
        tableData = [['Start Time', 'Task', 'End Time']]

        firstFind = True
        dayFinished = True

        for idx, task in enumerate(self.todayTasks):
            if self.time_between(task['startTime'], task['endTime']) and firstFind:
                currentTaskIndex = idx 
                firstFind = False
                dayFinished = False
            taskData = []
            taskData.append(task["startTime"])
            taskData.append(task["task"])
            taskData.append(task["endTime"])

            tableData.append(taskData)
        
        if dayFinished == False:
            tableData[currentTaskIndex + 1][0] = colored(self.todayTasks[currentTaskIndex]["startTime"], 'red', attrs=['bold'])
            tableData[currentTaskIndex + 1][1] = colored(self.todayTasks[currentTaskIndex]["task"], 'white', 'on_red', attrs=['bold'])
            tableData[currentTaskIndex + 1][2] = colored(self.todayTasks[currentTaskIndex]["endTime"], 'green', attrs=['bold'])
            # note : we have to do + 1 since tableData has a header row

        table = AsciiTable(tableData)

        return table.table

    # def week_tasks(self):
    #     """ prints out all the tasks in the week """
    #     tableData = [['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']]

    #     # Read in the schedule data json file of WEEk
    #     self.weekTasks = []
    #     with open('/home/namv/Documents/Personal_Projects/Personal_Board/code/Schedule_Data/schedule.json') as json_file:
    #         data = json.load(json_file)
    #         for p in data[now.strftime("%A")]:
    #             self.weekTasks.append(p)

    
    def time_lessThan(self, timeIn):
        """ compares the current time with the given time (input is string)"""
        # convert time string to datetime
        now = datetime.now()
        timeIn = timeIn.split(":")
        timeIn = now.replace(hour=int(timeIn[0]), minute=int(timeIn[1]), second=0, microsecond=0)
        
        return now < timeIn

    def time_between(self, startTime, endTime):
        """ compares the current time with the given start and end time """
        # convert time string to datetime
        now = datetime.now()
        startTime = startTime.split(":")
        startTime = now.replace(hour=int(startTime[0]), minute=int(startTime[1]), second=0, microsecond=0)
        endTime = endTime.split(":")
        endTime = now.replace(hour=int(endTime[0]), minute=int(endTime[1]), second=0, microsecond=0)

        if (now >= startTime) and (now < endTime) :
            return True
        else :
            return False 