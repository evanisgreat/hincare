import subprocess
import os
import time
import sys
from datetime import datetime

def hkgovhad_script(date):
    directory = "/Users/evan/PycharmProjects/hincare/hkgovhad/hkgovhad"
    os.chdir(directory)

    file_name1 = 'hkgovhad_activities_eng_' + date + '.json'
    command1 = "scrapy crawl hkgovhad_activities_eng -O " + file_name1

    file_name2 = 'hkgovhad_activities_tc_' + date + '.json'
    command2 = "scrapy crawl hkgovhad_activities_tc -O " + file_name2

    os.system(command1)
    os.system(command2)

def hkpptravel_script(date):
    directory = "/Users/evan/PycharmProjects/hincare/hkppltravel/hkppltravel"
    os.chdir(directory)

    file_name1 = 'hkppltravel' + date + '.json'
    command1 = "scrapy crawl hkppltravel -O " + file_name1

    os.system(command1)

# Keep the script running to allow the scheduled tasks to execute

# update status - handle how many event
# terminal show how many event handle
# have commands to kill/instant process
# have list of commands
# show updated events

# or can put timer in loop and check for keyboard

# each object in json, match up in the old file, if there is check if it is different/updated

# json "last updated"/"last modified"
while True:
    now = datetime.now()
    # Get current time
    current_time = now.strftime("%H:%M:%S")

    # Get current date
    current_date = now.strftime("%Y-%m-%d")

    hkgovhad_script(current_date)
    hkpptravel_script(current_date)

    print("Updated at " + current_date + " " + current_time)
    time.sleep(86400)

