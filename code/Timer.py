 # * author : Philippe Vo 
 # * date : Sep-29-2019 13:28:54
 
# * Imports
# 3rd Party Imports
import time
import datetime
# User Imports

# * Code
class Timer():
    """
    - runs a timer
    - when the timer is done :
        - say go to break
        - say go back to study/work
    - records all sessions inside a log file -> need a database or just folder ? 
    """
    def __init__(self):
        """ init all variables needed """
        self.mode = "study"

    def run_timer(self, mode, timeType, endTime):
        """ runs a timer and says to stop with custom string depending on mode """
        # print('Press ENTER to begin. Afterwards, press ENTER to "click" the stopwatch. Press Ctrl-C to quit.')
        input()                    # press Enter to begin
        print('Started.')
        startTime = time.time()    # get the first lap's start time
        totalTime = 0

        endTime = self.return_sec(timeType, endTime)

        # Start tracking the lap times.
        try:
            while endTime > totalTime:
                totalTime = round(time.time() - startTime, 2)
                print(totalTime, end='\r')
            printOut, message = self.done_timer(mode, totalTime)

        except KeyboardInterrupt:
                printOut, message = self.done_timer(mode, totalTime)

        return printOut, message

    def done_timer(self, mode, totalTime):
        """ prints the total time and close message """

        # Handle the Ctrl-C exception to keep its error message from displaying.
        txt = str(datetime.timedelta(seconds=round(totalTime)))

        # spilt string
        x = txt.split(":")
        printOut = "Total Time : " + x[0] + " hours " + x[1] + " mins " + x[2] + " secs "
        message = "You should go back to your " + mode

        return printOut, message

    def return_sec(self, timeType, time):
        """ converts the time into seconds """

        if timeType == "seconds":
            time = time
        elif timeType == "mins":
            time = time * 60
        else: # time = hours
            time = time * 60 * 60

        return time