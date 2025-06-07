import time
import datetime
import os

timestamp = int(time.time())

# print(timestamp)

timestamp -= 86400

datetime_object = datetime.datetime.fromtimestamp(timestamp)

# print(datetime_object)

date = datetime_object.strftime("%Y-%m-%d")
# print(date)

file_path = '/Users/evan/PycharmProjects/hincare/hkppltravel/hkppltravel' + str(date) + '.json' # Replace with the actual path
while not os.path.exists(file_path):
    print(f"File '{file_path}' not found.")
    time.sleep(1)
    timestamp -= 86400

    datetime_object = datetime.datetime.fromtimestamp(timestamp)

    # print(datetime_object)

    date = datetime_object.strftime("%Y-%m-%d")
    print(date)

    file_path = '/Users/evan/PycharmProjects/hincare/hkppltravel/hkppltravel/hkppltravel' + str(date) + '.json'
else:
    print(f"File '{file_path}' found successfully.")

