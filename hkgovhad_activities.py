from turtledemo.penrose import start

import scrapy
import re



## function to determine if a string contains a subscripts
## due to website formatting many subscripts separate strings
## used when strings may be separated by subscripts
def is_subscript(string):
    subscipts = ['th', 'rd', 'nd', 'st']
    if string in subscipts:
        return True
    return False


## function to figure if a string is a date
## returns true or false
def is_date(string):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for month in months:
        if month in string:
            return True
    return False


## determines if a string is time
## look for key words in the string
def is_time(string):
    keys = ['Open all day', 'am', 'pm', 'time', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'TBC', 'Open all day']
    for key in keys:
        if key in string:
            return True
    return False


## checks for target audience as a field
def refer_target_aud(string):
    if "target participants:" in string.lower():
        return True
    return False


### checks if a string is a telephone number for categorizing
def is_tele(string):
    if 'tel:' in string.lower():
        return True
    return False


### checks if a string is a contact person
def is_person(string):
    keys = ['mr', 'ms', 'mister', 'miss']
    for key in keys:
        if key in string.lower():
            return True
    return False


### dictionary that maps each month to its corresponding number
month_dict = {
    'January': '01',
    'Jan': '01',
    'February': '02',
    'Feb': '02',
    'March': '03',
    'Mar': '03',
    'April': '04',
    'Apr': '04',
    'May': '05',
    'June': '06',
    'Jun': '06',
    'July': '07',
    'Jul': '07',
    'August': '08',
    'Aug': '08',
    'September': '09',
    'Sep': '09',
    'October': '10',
    'Oct': '10',
    'November': '11',
    'Nov': '11',
    'December': '12',
    'Dec':'12'
}


## dictionary to convert hours in 24-hour double-digit system (for pm)
pm_dict = {
    '1': '13',
    '2': '14',
    '3': '15',
    '4': '16',
    '5': '17',
    '6': '18',
    '7': '19',
    '8': '20',
    '9': '21',
    '10':'22',
    '11': '23',
    '12': '12'
}


## dictionary to convert hours into 24-hour double-digit system (for am)
am_dict = {
    '1': '01',
    '2': '02',
    '3': '03',
    '4': '04',
    '5': '05',
    '6': '06',
    '7': '07',
    '8': '08',
    '9': '09',
    '10':'10',
    '11': '11',
    '12': '00'
}


##### given a string, find starting time and ending time
## ex: 12nn - 1:30pm
def convert_time(string):
    ## split based on '-'
    times = string.replace(' ','').split("-")

    ## create return dict
    d = dict()

    ## assume first one in list is start time
    start_time = times[0]

    ### convert all numbers to 24 hour system based on index and am/pm
    if 'am' in start_time:
        if ':' in start_time:
            d['starting time'] = am_dict[start_time[:start_time.index(':')]] + times[1][times[1].index(':'):times[1].index('am')]
        else:
            d['starting time'] = am_dict[start_time[:start_time.index('am')]] + ':00'
    elif 'pm' in start_time:
        if ':' in start_time:
            d['starting time'] = pm_dict[start_time[:start_time.index(':')]] + times[1][times[1].index(':'):times[1].index('pm')]
        else:
            d['starting time'] = pm_dict[start_time[:start_time.index('pm')]] + ':00'
    elif 'nn' in start_time:
        if ':' in start_time:
            d['starting time'] = start_time[:start_time.index('nn')]
        else:
            d['starting time'] = start_time[:start_time.index('nn')] + ':00'
    else:
        d['starting time'] = start_time

    # if only one date assume ending time is same
    if len(times) < 2:
        d['ending time'] = d['starting time']

    # repeat process of converting time to 24 hour system
    elif 'am' in times[1]:
        if ':' in times[1]:
            d['ending time'] = am_dict[times[1][:times[1].index(':')]] + times[1][times[1].index(':'):times[1].index('am')]
        else:
            d['ending time'] = am_dict[times[1][:times[1].index('am')]] + ':00'
    elif 'pm' in times[1]:
        if ':' in times[1]:
            d['ending time'] = pm_dict[times[1][:times[1].index(':')]] + times[1][times[1].index(':'):times[1].index('pm')]
        else:
            d['ending time'] = pm_dict[times[1][:times[1].index('pm')]] + ':00'
    elif 'nn' in times[1]:
        if ':' in times[1]:
            d['ending time'] = times[1][:times[1].index('nn')]
        else:
            d['ending time'] = times[1][:times[1].index('nn')] + ':00'
    else:
        d['ending time'] = times[1]

    return d


### processes date by finding the year, month and day of the string
def process_date(date):
    strings = date.strip().split(' ')
    year = ''
    month = ''
    day = ''

    ### if the string is 4 numbers, it is year
    ### if it is another number, it is day
    ### else it is month if month_dict does not throw error
    for s in strings:
        if re.search('\d{4}', s):
            year = s
        elif re.search('\D', s):
            try:
                month = month_dict[s]
            except:
                continue
        else:
            #    print(s)
            try:
                if int(s) < 10:
                    day += '0'
                day += s
            except:
                day += s
    ### if only month is given, assume is the 1st
    ### '#' means guess
    if len(day) == 0:
        day = '01#'
    return year, month, day


## given a string, find starting date and ending date
## ex: 24 April 2025 to 5 March 2026
def convert_date(string):
    # split string into two different dates
    if " to " in string:
        dates = string.split(" to ")
    else :
        dates = string.split("-")

    # define return dictionary
    d = dict()

    ## assume first string is starting date
    start_date = dates[0]

    ### turn return of process_date into list
    parts_of_date_start = list(process_date(start_date))

    missing_year = False
    missing_month = False

    ### parts_of_date_start[0] = year
    ### parts_of_date_start[0] = month
    ### parts_of_date_start[0] = day
    if len(parts_of_date_start[0]) > 0 and len(parts_of_date_start[1]) > 0 and len(parts_of_date_start[2]) > 0:
        d['starting date'] = parts_of_date_start[0] + '/' + parts_of_date_start[1] + '/' + parts_of_date_start[2]
    else:
        d['starting date'] = '*'
        if len(parts_of_date_start[0]) == 0:
            missing_year = True
        if len(parts_of_date_start[1]) == 0:
            missing_month = True
    # print(day)

    ### the reason why missing year and missing month is checked is because dates could show up as 1 - 7 April 2025

    ### if there is only one date set them equal
    ### else repeat process for ending date
    if len(dates) < 2:
        d['ending date'] = d['starting date']
    else:
        end_date = dates[1]
        parts_of_date_end = list(process_date(end_date))
        d['ending date'] = parts_of_date_end[0] + '/' + parts_of_date_end[1] + '/' + parts_of_date_end[2]
        if missing_year and missing_month:
            d['starting date'] = parts_of_date_end[0] + '/' + parts_of_date_end[1] + '/' + parts_of_date_start[2] + '#'
        elif missing_year:
            d['starting date'] = parts_of_date_end[0] + '/' + parts_of_date_start[1] + '/' + parts_of_date_start[2] + '#'
        elif missing_month:
            d['starting date'] = parts_of_date_start[0] + '/' + parts_of_date_end[1] + '/' + parts_of_date_start[2] + '#'

    return d


class HkGovHad_Activities(scrapy.Spider):
    name = "hkgovhad_activities_eng"
    start_urls = []

    # each district's link is labeled by number in specific pattern
    # here I added each 18 to start_urls

    for i in range(1, 10):
        start_urls.append('https://www.had.gov.hk/en/18_districts/my_map_0' + str(i) + '_activities.htm')

    for j in range(10, 19):
        start_urls.append('https://www.had.gov.hk/en/18_districts/my_map_' + str(j) + '_activities.htm')

    # parse each url
    def parse(self, reponse):
        for url in HkGovHad_Activities.start_urls:
            yield scrapy.Request(url, callback=self.parselink)


    def parselink(self, response):
        rows = response.xpath("//table[@class='content-table high-padding desktop-table']//tbody/tr")

        # create log file for debugging
        file = open('scraped_data.out', 'w')

        # create list of events
        event_list = []

        # grab district the event is in
        district = response.xpath("//div[@class='h1-wrapper']//h2//text()").get()
        district = re.sub('District Activities \(', '', district)

        # grab last revised date
        last_revision_date_grab = response.xpath("//div[@class='bottom-date']//div[@class='bottom-nav_item']//text()")[1].get()
        last_revision_date_re = re.sub('Last Revision Date :', '', last_revision_date_grab)
        last_revision_date_list = list(process_date(last_revision_date_re))
        last_revision_date = last_revision_date_list[0] + '/' + last_revision_date_list[1] + '/' + last_revision_date_list[2]


        # loop through each row of the table
        for row in rows:
            # get list of column
            columns = row.xpath(".//td")

            # assign each column to its variable
            first_column = columns[0].xpath(".//text()").getall()
            file.write(str(first_column) + "\n")
            second_column = columns[1].xpath(".//text()").getall()
            file.write(str(second_column) + "\n")
            third_column = columns[2].xpath(".//text()").getall()
            file.write(str(third_column) + "\n")
            fourth_column = columns[3].xpath(".//text()").getall()
            file.write(str(fourth_column) + "\n")

            # create event dictionary
            event = {'event district': district[:len(district)-1], 'event name': '', 'event date string': '*', 'event start date': [], 'event end date': [],
                     'event duration string': [], 'event start time':[], 'event end time':[],
                     'event location': [], 'event description': '', 'event target audience': '*',
                     'event contact person': '*', 'event contact address': [], 'event contact tele': '*',
                     'last update date': last_revision_date, 'event status': '*'}

            ### construct the event name by strings in the first column
            for string in first_column:
                event['event name'] += string

            ### for second column it may contain date, location and time (duration)
            for string in second_column:
                if is_date(string):
                    event['event date string'] = string
                    try:
                        event['event start date'].append(convert_date(string)['starting date'])
                        event['event end date'].append(convert_date(string)['ending date'])
                    except:
                        event['event start date'].append("error processing date, @")
                        event['event end date'].append("error processing date, @")
                elif is_time(string):
                    event['event duration string'].append(string)
                    try:
                        event['event start time'].append(convert_time(string)['starting time'])
                        event['event end time'].append(convert_time(string)['ending time'])
                    except:
                        event['event start time'].append("error processing time, @")
                        event['event end time'].append("error processing time, @")
                else:
                    event['event location'].append(string)

            ### for third column it may contain description and target audience
            for string in third_column:
                if refer_target_aud(string):
                    event['event target audience'] = string
                else:
                    event['event description'] += string

            ### for fourth column it may contain event contact person, telephone number and contact address
            for string in fourth_column:
                if is_tele(string) and is_person(string):
                    index = string.lower().index("tel:")
                    event['event contact person'] = string[:index]
                    event['event contact tele'] = string[index:]
                elif is_tele(string):
                    event['event contact tele'] = string
                elif is_person(string):
                    event['event contact person'] = string
                else:
                    event['event contact address'].append(string)

            event_list.append(event)
            yield event

