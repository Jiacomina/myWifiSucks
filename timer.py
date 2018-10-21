''' 
Code taken from 'Nicojo' on stackoverflow:
https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
'''

# import packages for program timer
import atexit
from time import time, strftime, localtime
from datetime import timedelta

def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))

def log(s, elapsed=None):
    line = "="*40
    print(line)
    print(secondsToStr(), '-', s)
    if elapsed:
        print("Elapsed time:", elapsed)
    print(line)
    print()

def endlog(start):
    end = time()
    elapsed = end-start
    log("End Program", secondsToStr(elapsed))
    return elapsed