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

    data1 = sorted(data1, key=lambda d: d['event name'])
    data2 = sorted(data2, key=lambda d:d['event name'])

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


# print(compare_json_files('hkgovhad/hkgovhad_activities_tc_2025-05-08.json', 'hkgovhad/hkgovhad/hkgovhad_activities_tc_2025-05-29.json'))

# old_events = return_list[0]
# new_events = return_list[1]
#
# print(new_events)

# see within event
