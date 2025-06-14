import scrapy
import re



def is_subscript(string):
    subscipts = ['th', 'rd', 'nd', 'st']
    if string in subscipts:
        return True
    return False


def is_date(string):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for month in months:
        if month in string:
            return True
    return False


def is_time(string):
    keys = ['Open all day', 'pm', 'time', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'TBC', 'Open all day']
    for key in keys:
        if key in string:
            return True
    return False


def refer_target_aud(string):
    if "Target participants:" in string:
        return True
    return False


def is_tele(string):
    if 'tel:' in string:
        return True
    return False


def is_person(string):
    keys = ['Mr', 'Ms', 'Mister', 'Miss']
    for key in keys:
        if key in string:
            return True
    return False


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


def convert_time(string):
    times = string.replace(' ','').split("-")
    d = dict()
    start_time = times[0]

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

    if len(times) < 2:
        d['ending time'] = d['starting time']
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


def convert_date(string):
    if " to " in string:
        dates = string.split(" to ")
    else :
        dates = string.split(" - ")
    d = dict()
    start_date = dates[0].split(" ")

    year = ''
    month = ''
    day = ''
    for s in start_date:
        # print(s)
        if re.search('\d{4}', s):
            year = s
        elif re.search('\D', s):
            try:
                month = month_dict[s]
            except:
                continue
        else:
        #    print(s)
            day = s
    d['starting date'] = year + '/' + month + '/' + day

    # print(day)

    if len(dates) < 2:
        d['ending date'] = d['starting date']
    else:
        end_date = dates[1].split(" ")
        for s in end_date:
            if re.search('\d{4}', s):
                year = s
            elif re.search('\D', s):
                try:
                    month = month_dict[s]
                except:
                    continue
            else:
                day = s

        d['ending date'] = year + '/' + month + '/' + day

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
        last_revision_date = response.xpath("//div[@class='bottom-date']//div[@class='bottom-nav_item']//text()")[1].get()
        last_revision_date = re.sub('Last Revision Date :', '', last_revision_date)

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
            event = {'event district': district[:len(district)-1], 'event name': '', 'event date string': '', 'event start date': [], 'event end date': [],
                     'event duration string': [], 'event start time':[], 'event end time':[],
                     'event location': [], 'event description': '', 'event target audience': None,
                     'event contact person': None, 'event contact address': [], 'event contact tele': None,
                     'last update date': last_revision_date, 'event status': ''}

            for string in first_column:
                event['event name'] += string

            for string in second_column:
                if is_date(string):
                    event['event date string'] = string
                    try:
                        event['event start date'].append(convert_date(string)['starting date'])
                        event['event end date'].append(convert_date(string)['ending date'])
                    except:
                        event['event start date'].append("error processing date")
                        event['event end date'].append("error processing date")
                elif is_time(string):
                    event['event duration string'].append(string)
                    try:
                        event['event start time'].append(convert_time(string)['starting time'])
                        event['event end time'].append(convert_time(string)['ending time'])
                    except:
                        event['event start time'].append("error processing time")
                        event['event end time'].append("error processing time")
                else:
                    event['event location'].append(string)

            for string in third_column:
                if refer_target_aud(string):
                    event['event target audience'] = string
                else:
                    event['event description'] += string

            for string in fourth_column:
                if is_tele(string) and is_person(string):
                    index = string.index("電")
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

