from pathlib import Path
from re import search

import scrapy
import json
import re
from datetime import datetime



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
        if re.search('\d{4}', dates[0]):
            year = s
        elif re.search('\D', dates[0]):
            try:
                month = month_dict[s]
            except:
                continue
        else:
            day = s
    d['starting date'] = year + '/' + month + '/' + day

    if len(dates) < 1:
        d['ending date'] = d['starting date']
    else:
        end_date = dates[1].split(" ")
        for s in end_date:
            if re.search('\d{4}', dates[0]):
                year = s
            elif re.search('\D', dates[0]):
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
    for i in range(1, 10):
        start_urls.append('https://www.had.gov.hk/en/18_districts/my_map_0' + str(i) + '_activities.htm')

    for j in range(10, 19):
        start_urls.append('https://www.had.gov.hk/en/18_districts/my_map_' + str(j) + '_activities.htm')


    def parse(self, reponse):
        for url in HkGovHad_Activities.start_urls:
            yield scrapy.Request(url, callback=self.parselink)


    def parselink(self, response):
        rows = response.xpath("//table[@class='content-table high-padding desktop-table']//tbody/tr")
        file = open('scraped_data.out', 'w')
        event_list = []
        district = response.xpath("//div[@class='h1-wrapper']//h2//text()").get()
        district = re.sub('District Activities \(', '', district)
        last_revision_date = response.xpath("//div[@class='bottom-date']//div[@class='bottom-nav_item']//text()")[1].get()
        last_revision_date = re.sub('Last Revision Date :', '', last_revision_date)
        for row in rows:
            columns = row.xpath(".//td")
            first_column = columns[0].xpath(".//text()").getall()
            file.write(str(first_column) + "\n")
            second_column = columns[1].xpath(".//text()").getall()
            file.write(str(second_column) + "\n")
            third_column = columns[2].xpath(".//text()").getall()
            file.write(str(third_column) + "\n")
            fourth_column = columns[3].xpath(".//text()").getall()
            file.write(str(fourth_column) + "\n")
            event = {'event district': district[:len(district)-1], 'event name': '', 'event date string': '', 'event start date': [], 'event end date': [],
                     'event duration': [],
                     'event location': [], 'event description': '', 'event target audience': None,
                     'event contact person': None, 'event contact address': [], 'event contact tele': None,
                     'last update date': last_revision_date}

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
                    event['event duration'].append(string)
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

        # with open("hkgovhad_activites_tc.json", "w") as final:
        #     json.dump(event_list, final)

        # rows = response.xpath("//table[@class='content-table high-padding desktop-table']//tbody/tr")
        # file = open('scraped_data.out', 'w')
        # event_list = []
        # district = response.xpath("//div[@class='h1-wrapper']//h2//text()").get()
        # district = re.sub('District Activities \(', '', district)
        # last_revision_date = response.xpath("//div[@class='bottom-date']//div[@class='bottom-nav_item']//text()")[1].get()
        # last_revision_date = re.sub('Last Revision Date :', '', last_revision_date)
        # for row in rows:
        #     row_info = row.xpath(".//td//text()").getall()
        #     file.write(str(row_info) + "\n")
        #     info = []
        #     i = 0
        #     info_index = 0
        #     event = {
        #         'event district': district[:len(district) - 1],
        #         'event name': None,
        #         'event date': [],
        #         'event duration': [],
        #         'event location': [],
        #         'event description': None,
        #         'event target audience': None,
        #         'event contact person': None,
        #         'event contact address': None,
        #         'event contact tele': None,
        #         'last update date': last_revision_date
        #     }
        #     while i < len(row_info):
        #         if is_subscript(row_info[i]):
        #             info[len(info) - 1] += row_info[i]
        #             info[len(info) - 1] += row_info[i + 1]
        #             i += 1
        #         else:
        #             info.append(row_info[i])
        #         # file.write(str(i) + "\n")
        #         i += 1
        #
        #     print(info)
        #     event['event name'] = info[info_index]
        #     info_index += 1
        #     print(info[info_index])
        #     while is_date(info[info_index]):
        #         event['event date'].append(info[info_index])
        #         info_index += 1
        #     print(info[info_index])
        #     while is_time(info[info_index]):
        #         event['event duration'].append(info[info_index])
        #         info_index += 1
        #     if len(info[info_index]) < len(info[info_index + 1]):
        #         event['event location'].append(info[info_index])
        #         info_index += 1
        #     print(info[info_index])
        #     while re.search(r'\d\.', info[info_index]):
        #         event['event location'].append(info[info_index])
        #         info_index += 1
        #     print(info[info_index])
        #     event['event description'] = info[info_index]
        #     info_index += 1
        #     print(info[info_index])
        #     if refer_target_aud(info[info_index]):
        #         event['event target audience'] = info[info_index]
        #         info_index += 1
        #     event['event contact person'] = info[info_index]
        #     info_index += 1
        #     event['event contact address'] = info[info_index]
        #     info_index += 1
        #     if info_index < len(info):
        #         event['event contact tele'] = info[info_index]

        #     file.write(str(info) + "\n")
        #
        #     event_list.append(event)
        #     yield event
        #
        # with open("hkgovhad_activites_eng.json", "w") as final:
        #     json.dump(event_list, final)




