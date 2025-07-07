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

    # compares two sorted because sometimes they do not scrape in order
    # sorts by name because that is a common field among all files
    try:
        data1 = sorted(data1, key=lambda d: d['event name'])
        data2 = sorted(data2, key=lambda d: d['event name'])
    except:
        print('unsortable')

    # checks for exact match
    if data1 == data2:
        # updates status for each field

        for item in data2:
            item['event status'] = 'old'

        # print(file_path2)
        with open(file_path2, 'w') as file:
            json.dump(data2, file, indent=4, ensure_ascii=False)

        return "Files are identical."
    else:
        # calls method to generate differences of the two files
        return find_differences(data1, data2, file_path1, file_path2)

# find the differences between two json files
# first data is assumed to be first file
# second data assumed to be second file
def find_differences(data1, data2, file_path1, file_path2):
    # print(type(data1))
    # print(data1)

    # two sets so finding if they are in either data set would be easier
    set1 = {str(item) for item in data1}
    set2 = {str(item) for item in data2}

    # check for items in the old file and not in the new file
    in_set1_not_set2 = set1 - set2

    # type(in_set1_not_set2)
    #
    # print(in_set1_not_set2)

    in_list1_not_list2 = []

    # update status
    for item in data1:
        if str(item) in in_set1_not_set2:
            item['event status'] = 'done'
            in_list1_not_list2.append(item)

    # check for items in the new file but not in the old file
    in_set2_not_set1 = set2 - set1

    # for json dump
    in_list2_not_list1 = []

    # update status
    for item in data2:
        if str(item) in in_set2_not_set1:
            item['event status'] = 'new'
            in_list2_not_list1.append(item)
        else:
            item['event status'] = 'old'

    # dump data back to original file
    with open(file_path2, 'w') as file:
        json.dump(data2, file, indent=4, ensure_ascii=False)

    return in_list1_not_list2, in_list2_not_list1



def hkgovhad_script(date):
    # file of where the python file is
    # may have to change to fit personal device
    directory = "/Users/evan/PycharmProjects/hincare/hkgovhad/hkgovhad"
    os.chdir(directory)

    # construct for output file hkgovhad_activities_eng_[date].json
    file_name1 = 'hkgovhad_activities_eng_' + date + '.json'

    # terminal command to run spider hkgovhad_activities_eng
    command1 = "scrapy crawl hkgovhad_activities_eng -O " + file_name1

    # calls command from system
    os.system(command1)

    # get current epoch time from 1970 (so we know current date)
    timestamp = int(time.time())
    # print(timestamp)

    # get time the day before
    timestamp -= 86400

    # convert timestamp to datetime object
    datetime_object = datetime.fromtimestamp(timestamp)
    # print(datetime_object)

    # turn into year-month-date form
    date_obj = datetime_object.strftime("%Y-%m-%d")
    # print(date)

    # construct the old file path
    old_file_path = directory + '/hkgovhad_activities_eng_' + str(date_obj) + '.json'

    # loop_count to keep track of how many times the loop tries to find an old file
    # prevents forever loop
    loop_count = 0

    # loop to find old file path
    while not os.path.exists(old_file_path):
        print(f"File '{old_file_path}' not found.")
        # wait 1 second due to speed of console
        time.sleep(1)
        # go back a day
        timestamp -= 86400

        # convert to datetime object
        datetime_object = datetime.fromtimestamp(timestamp)
        # print(datetime_object)

        # convert to year-month-day format
        date_obj = datetime_object.strftime("%Y-%m-%d")
        print(date_obj)

        # construct old file path
        old_file_path = directory + '/hkgovhad_activities_eng_' + str(date_obj) + '.json'

        # check loop count over a month ago - could be changed
        if loop_count > 31:
            print('no file at all')
            break
        else:
            loop_count += 1
    else:
        print(f"File '{old_file_path}' found successfully.")

        # construct new file path
        new_file_path = directory + '/' + file_name1

        # return_item due to different return types
        return_item = compare_json_files(old_file_path, new_file_path)

        # check if it was a print statements
        if type(return_item) == str:
            print(return_item)
        else:
            # convert to list
            return_list = list(return_item)
            # old_events first
            old_events = return_list[0]
            new_events = return_list[1]

            print('old events: ' + str(old_events))
            print('new events: ' + str(new_events))

        # os.remove(old_file_path)

    # file name for hkgovhad_activities_tc_[date].json
    file_name2 = 'hkgovhad_activities_tc_' + date + '.json'

    # terminal command for spider hkgovhad_activities_tc
    command2 = "scrapy crawl hkgovhad_activities_tc -O " + file_name2

    # run command on system
    os.system(command2)

    # see hkgovhad_eng (line 115) for checking previous files
    # same logic of finding previous dates

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
# hkppltravel.com/category/events
def hkpptravel_script(date):
    # file directory
    directory = "/Users/evan/PycharmProjects/hincare/hkppltravel/hkppltravel"
    # set directory
    os.chdir(directory)

    # create file name hkppltravel[date].json
    file_name1 = 'hkppltravel' + date + '.json'

    # create command for spider hkppltravel
    command1 = "scrapy crawl hkppltravel -O " + file_name1

    # run command on system
    os.system(command1)

    # again see line 115 for logic

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




# sets how long between each time the script runs
# input is in minutes through console
run_time = float(input('Enter how many minutes you would like the program to run each time (1 day = 1400 minutes): '))

while True:
    now = datetime.now()
    # Get current time
    current_time = now.strftime("%H:%M:%S")

    # Get current date
    current_date = now.strftime("%Y-%m-%d")

    # calls hkgovhad spiders (both english and chinese)
    hkgovhad_script(current_date)

    # due to current authorization problems I am commenting this out
    # hkpptravel_script(current_date)

    # update time in console
    print("\nUpdated at " + current_date + " " + current_time)
    print('Next Run in ' + str(run_time) + ' minutes\n')


    # wait until next loop - this time for debug
    time.sleep(run_time * 60)

    # uncomment below when running per day
    # time.sleep(86400)



