import subprocess
import os
import time
import sys
from datetime import datetime

from pynput import keyboard

import json


# compares two json files
# see if there are differences between old and new file

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
        data1 = sorted(data1, key=lambda d: d['event name'])
        data2 = sorted(data2, key=lambda d:d['event name'])
    except:
        print('unsortable')

    if data1 == data2:
        for item in data2:
            item['event status'] = 'old'

        # print(file_path2)
        with open(file_path2, 'w') as file:
            json.dump(data2, file, indent=4, ensure_ascii=False)

        return "Files are identical."
    else:
        return find_differences(data1, data2, file_path1, file_path2)

# find the differences between two json files
# first data is assumed to be first file
# second data assumed to be second file
def find_differences(data1, data2, file_path1, file_path2):
    # print(type(data1))
    # print(data1)

    set1 = {str(item) for item in data1}
    set2 = {str(item) for item in data2}

    in_set1_not_set2 = set1 - set2

    # type(in_set1_not_set2)
    #
    # print(in_set1_not_set2)

    in_list1_not_list2 = []

    for item in data1:
        if str(item) in in_set1_not_set2:
            item['event status'] = 'done'
            in_list1_not_list2.append(item)

    in_set2_not_set1 = set2 - set1

    in_list2_not_list1 = []

    for item in data2:
        if str(item) in in_set2_not_set1:
            item['event status'] = 'new'
            in_list2_not_list1.append(item)
        else:
            item['event status'] = 'old'

    with open(file_path2, 'w') as file:
        json.dump(data2, file, indent=4, ensure_ascii=False)

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

    date_obj = datetime_object.strftime("%Y-%m-%d")
    # print(date)

    old_file_path = directory + '/hkgovhad_activities_eng_' + str(date_obj) + '.json'
    loop_count = 0
    while not os.path.exists(old_file_path):
        print(f"File '{old_file_path}' not found.")
        time.sleep(1)
        timestamp -= 86400

        datetime_object = datetime.fromtimestamp(timestamp)

        # print(datetime_object)

        date_obj = datetime_object.strftime("%Y-%m-%d")
        print(date_obj)

        old_file_path = directory + '/hkgovhad_activities_eng_' + str(date_obj) + '.json'

        if loop_count > 31:
            print('no file at all')
            break
        else:
            loop_count += 1
    else:
        print(f"File '{old_file_path}' found successfully.")
        new_file_path = directory + '/' + file_name1

        return_item = compare_json_files(old_file_path, new_file_path)

        if type(return_item) == str:
            print(return_item)
        else:
            return_list = list(return_item)
            old_events = return_list[0]
            new_events = return_list[1]

            print('old events: ' + str(old_events))
            print('new events: ' + str(new_events))

        # os.remove(old_file_path)

    file_name2 = 'hkgovhad_activities_tc_' + date + '.json'

    command2 = "scrapy crawl hkgovhad_activities_tc -O " + file_name2

    os.system(command2)

    timestamp = int(time.time())

    # print(timestamp)

    timestamp -= 86400

    datetime_object = datetime.fromtimestamp(timestamp)

    # print(datetime_object)

    date_obj = datetime_object.strftime("%Y-%m-%d")
    # print(date)

    old_file_path = directory + '/hkgovhad_activities_tc_' + str(date_obj) + '.json'

    loop_count = 0
    while not os.path.exists(old_file_path):
        print(f"File '{old_file_path}' not found.")
        time.sleep(1)
        timestamp -= 86400

        datetime_object = datetime.fromtimestamp(timestamp)

        # print(datetime_object)

        date_obj = datetime_object.strftime("%Y-%m-%d")
        print(date_obj)

        old_file_path = directory + '/hkgovhad_activities_tc_' + str(date_obj) + '.json'

        if loop_count > 31:
            print('no file at all')
            break
        else:
            loop_count += 1
    else:
        print(f"File '{old_file_path}' found successfully.")

        new_file_path = directory + '/' + file_name2

        # print(new_file_path)

        return_item = compare_json_files(old_file_path, new_file_path)

        if type(return_item) == str:
            print(return_item)
        else:
            return_list = list(return_item)
            old_events = return_list[0]
            new_events = return_list[1]

            print('old events: ' + str(old_events))
            print('new events: ' + str(new_events))

            # os.remove(old_file_path)

# the website I was scraping for blocked me with 403 error
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
    loop_count = 0
    while not os.path.exists(old_file_path):
        print(f"File '{old_file_path}' not found.")
        time.sleep(1)
        timestamp -= 86400

        datetime_object = datetime.fromtimestamp(timestamp)

        # print(datetime_object)

        date = datetime_object.strftime("%Y-%m-%d")
        print(date)

        old_file_path = '/Users/evan/PycharmProjects/hincare/hkppltravel/hkppltravel/hkppltravel' + str(date) + '.json'

        if loop_count > 31:
            print('no file at all')
            break
        else:
            loop_count += 1
    else:
        print(f"File '{old_file_path}' found successfully.")

        new_file_path = directory + '/' + file_name1

        return_item = compare_json_files(old_file_path, new_file_path)

        if type(return_item) == str:
            print(return_item)
        else:
            return_list = list(return_item)
            old_events = return_list[0]
            new_events = return_list[1]

            print('old events: ' + str(old_events))
            print('new events: ' + str(new_events))

            # os.remove(old_file_path)


# def print_hot_keys():
#     print("hot keys: \n")
#     keys = ['c - kill program', 't - check next run']
#
#     for key in keys:
#         print(key)

# Keep the script running to allow the scheduled tasks to execute


run_time = float(input('Enter how many minutes you would like the program to run each time (1 day = 3600 minutes): '))

while True:
    now = datetime.now()
    # Get current time
    current_time = now.strftime("%H:%M:%S")

    # Get current date
    current_date = now.strftime("%Y-%m-%d")

    hkgovhad_script(current_date)

    # due to current authorization problems I am commenting this out
    # hkpptravel_script(current_date)

    print("\nUpdated at " + current_date + " " + current_time)
    print('Next Run in ' + str(run_time) + ' minutes\n')


    # wait until next loop - this time for debug
    time.sleep(run_time * 60)

    # uncomment below when running per day
    # time.sleep(86400)



