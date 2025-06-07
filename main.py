import subprocess
import os
import time
import sys
from datetime import datetime

from pynput import keyboard

import json


def compare_json_files(file_path1, file_path2):
    """
    Compares two JSON files and returns a dictionary of differences.
    """
    try:
        with open(file_path1, 'r') as f1, open(file_path2, 'r') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
    except FileNotFoundError:
         return "Error: One or both files not found."
    except json.JSONDecodeError:
        return "Error: Invalid JSON format in one or both files."

    try:
        data1 = sorted(data1, key=lambda d: d['name'])
        data2 = sorted(data2, key=lambda d:d['name'])
    except:
        print('unsortable')

    if data1 == data2:
        return "Files are identical."
    else:
        return find_differences(data1, data2)

def find_differences(data1, data2):
    set1 = {str(item) for item in data1}
    set2 = {str(item) for item in data2}

    in_list1_not_list2 = [eval(item) for item in set1 - set2]
    in_list2_not_list1 = [eval(item) for item in set2 - set1]

    return in_list1_not_list2, in_list2_not_list1



def hkgovhad_script(date):
    directory = "/Users/evan/PycharmProjects/hincare/hkgovhad/hkgovhad"
    os.chdir(directory)

    file_name1 = 'hkgovhad_activities_eng_' + date + '.json'
    command1 = "scrapy crawl hkgovhad_activities_eng -O " + file_name1

    os.system(command1)

    timestamp = int(time.time())

    # print(timestamp)

    timestamp -= 86400

    datetime_object = datetime.fromtimestamp(timestamp)

    # print(datetime_object)

    date = datetime_object.strftime("%Y-%m-%d")
    # print(date)

    old_file_path = directory + '/hkgovhad_activities_eng_' + str(date) + '.json'
    while not os.path.exists(old_file_path):
        print(f"File '{old_file_path}' not found.")
        time.sleep(1)
        timestamp -= 86400

        datetime_object = datetime.fromtimestamp(timestamp)

        # print(datetime_object)

        date = datetime_object.strftime("%Y-%m-%d")
        print(date)

        old_file_path = directory + '/hkgovhad_activities_eng_' + str(date) + '.json'
    else:
        print(f"File '{old_file_path}' found successfully.")

    new_file_path = directory + '/' + file_name1

    return_list = list(compare_json_files(old_file_path, new_file_path))

    old_events = return_list[0]
    new_events = return_list[1]

    print('old events: ' + str(old_events))
    print('new events: ' + str(new_events))

    os.remove(old_file_path)

    file_name2 = 'hkgovhad_activities_tc_' + date + '.json'
    command2 = "scrapy crawl hkgovhad_activities_tc -O " + file_name2

    os.system(command2)

def hkpptravel_script(date):
    directory = "/Users/evan/PycharmProjects/hincare/hkppltravel/hkppltravel"
    os.chdir(directory)

    file_name1 = 'hkppltravel' + date + '.json'
    command1 = "scrapy crawl hkppltravel -O " + file_name1

    os.system(command1)

    timestamp = int(time.time())

    # print(timestamp)

    timestamp -= 86400

    datetime_object = datetime.fromtimestamp(timestamp)

    # print(datetime_object)

    date = datetime_object.strftime("%Y-%m-%d")
    # print(date)

    old_file_path = '/Users/evan/PycharmProjects/hincare/hkppltravel/hkppltravel/hkppltravel' + str(date) + '.json'
    while not os.path.exists(old_file_path):
        print(f"File '{old_file_path}' not found.")
        time.sleep(1)
        timestamp -= 86400

        datetime_object = datetime.fromtimestamp(timestamp)

        # print(datetime_object)

        date = datetime_object.strftime("%Y-%m-%d")
        print(date)

        old_file_path = '/Users/evan/PycharmProjects/hincare/hkppltravel/hkppltravel/hkppltravel' + str(date) + '.json'
    else:
        print(f"File '{old_file_path}' found successfully.")

    new_file_path = directory + '/' + file_name1

    return_list = list(compare_json_files(old_file_path, new_file_path))

    old_events = return_list[0]
    new_events = return_list[1]

    print('old events: ' + str(old_events))
    print('new events: ' + str(new_events))

    os.remove(old_file_path)


def print_hot_keys():
    print("hot keys: \n")
    keys = ['c - kill program', 't - check next run']

    for key in keys:
        print(key)

# Keep the script running to allow the scheduled tasks to execute

# update status - handle how many event
# terminal show how many event handle
# have commands to kill/instant process
# have list of commands
# show updated events

# or can put timer in loop and check for keyboard

# each object in json, match up in the old file, if there is check if it is different/updated

# json "last updated"/"last modified"

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        # sys.exit()
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False




while True:
    now = datetime.now()
    # Get current time
    current_time = now.strftime("%H:%M:%S")

    # Get current date
    current_date = now.strftime("%Y-%m-%d")

    hkgovhad_script(current_date)
    hkpptravel_script(current_date)

    print("Updated at " + current_date + " " + current_time)

    print_hot_keys()

    # Collect events until released
    time.sleep(20)



