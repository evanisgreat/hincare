from pathlib import Path

import scrapy
import json
import re


def is_subscript(string):
    subscipts = ['th', 'rd', 'nd', 'st']
    if string in subscipts:
        return True
    return False


def is_date(string):
    months = ['月']
    for month in months:
        if month in string:
            return True
    return False


time_dict = {
    '上午': 'am',
    '中午': 'pm',
    '下午': 'pm',
    '晚上': 'pm',
    '時': ':',
    '星期一': 'Monday',
    '星期二': 'Tuesday',
    '星期三': 'Wednesday',
    '星期四': 'Thursday',
    '星期五': 'Friday',
    '星期六': 'Saturday',
    '星期日': 'Sunday',
    '十': '10',
    '一': '1',
    '二': '2',
    '三': '3',
    '四': '4',
    '五': '5',
    '六': '6',
    '七': '7',
    '八': '8',
    '九': '9',
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
    '10': '10',
    '11': '11',
    '12': '00'
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
    '10': '22',
    '11': '23',
    '12': '12'
}

number_dict = {
    '1': '01',
    '2': '02',
    '3': '03',
    '4': '04',
    '5': '05',
    '6': '06',
    '7': '07',
    '8': '08',
    '9': '09',
    '10': '10',
    '11': '11',
    '12': '12'
}



def is_time(string):
    keys = ['全日開放', '上午', '中午', '下午', '晚上', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日', '時間']
    for key in keys:
        if key in string:
            return True
    return False


def process_date(year, month, string):
    print(year)
    print(month)
    print(string)
    if '月' in string and '年' in string:
        try:
            new_string = year + "/" + number_dict[string[string.index('年') + 1:string.index('月')]]
        except:
            new_string = year + "/" + string[string.index('年') + 1:string.index('月')]
    elif '年' in string:
        new_string = year + "/" + string[string.index(year)+1:]
    elif '月' in string:
        try:
            new_string = year + "/" + number_dict[string[:string.index('月')]]
        except:
            new_string = year + "/" + string[:string.index('月')]
    else:
        new_string = year + "/" + month

    if '日' in string:
        if '月' not in string:
            try:
                new_string += number_dict[string[:string.index('日')]]
            except:
                print("error dict")
                new_string += string[:string.index('日')]
        else:
            try:
                new_string += "/" + number_dict[string[string.index('月')+1:string.index('日')]]
            except:
                print("error dict")
                new_string += "/" + string[string.index('月')+1:string.index('日')]
    return new_string


def convert_date(string):
    string = string.replace(' ', '')
    d = dict()
    strings = string.split('至')
    print(strings[0])
    year = ''
    month = ''
    if '年' in strings[0]:
        year = strings[0][:strings[0].index('年')]
        # print(strings[0].index('年'))
        # print(strings[0].index('月'))
        # if '月' in strings[0]:
        #     print("yes")
        #     month = strings[0][strings[0].index('年')+1:strings[0].index('月')]
    # elif '月' in string[0]:
    #     month = strings[0][:strings[0].index('月')]
    # month = '2'
    d['starting date'] = process_date(year, month, strings[0])
    d['ending date'] = ''
    if len(strings) < 2:
        d['ending date'] = d['starting date']
        return d
    if '年' in strings[1]:
        year = strings[1][:strings[1].index('年')]
        if '月' in strings[1]:
            month = strings[1][strings[1].index('年')+1:strings[1].index('月')]
    d['ending date'] = process_date(year, month, strings[1])
    return d


def process_time(string, am):
    new_string = ''
    last_index = 0
    if am:
        if '早上' in string:
            new_string += am_dict[string[string.index('早上') + 2: string.index('時')]]
            last_index = string.index('時')
        elif '上午' in string:
            new_string += am_dict[string[string.index('上午') + 2: string.index('時')]]
            last_index = string.index('時')
        else:
            try:
                new_string += am_dict[string[:string.index('時')]]
                last_index = string.index('時')
            except:
                new_string = 'error'
    else:
        if '下午' in string or '中午' in string:
            new_string += pm_dict[string[string.index('午') + 1: string.index('時')]]
            last_index = string.index('時')
        elif '晚上' in string:
            new_string += pm_dict[string[string.index('晚上') + 2: string.index('時')]]
            last_index = string.index('時')
        else:
            try:
                new_string += pm_dict[string[:string.index('時')]]
                last_index = string.index('時')
            except:
                new_string = 'error'

    if string.index('分') > 0 and '時' in string:
        new_string += ':' + string[last_index + 1:string.index('分')]
    else:
        new_string += ':00'
    return new_string


def convert_time(string):
    string = string.replace(' ','')
    d = dict()
    strings = string.split('至')
    am = False
    if '上午' in strings[0] or '早上' in strings[0]:
        am = True
    d['starting time'] = process_time(strings[0], am)

    if len(strings) < 2:
        d['ending time'] = d['starting time']
    else:
        if '下午' in strings[0] or '中午' in strings[0] or '晚上' in strings[0]:
            am = False
        d['ending time'] = process_time(strings[1], am)
    return d


def is_tbc(string):
    keys = ['(暫定)', '(暫名)']
    for key in keys:
        if key == string:
            return True
    return False


def is_tele(string):
    keys = ['電話', '電 話']
    for key in keys:
        if key in string:
            return True
    return False


def is_person(string):
    keys = ['先生', '女士', '小姐']
    for key in keys:
        if key in string:
            return True
    return False


def refer_target_aud(string):
    if "對象" in string:
        return True
    return False


class HkGovHad_Activities_Tc(scrapy.Spider):
    name = "hkgovhad_activities_tc"
    start_urls = []
    for i in range(1, 10):
        start_urls.append('https://www.had.gov.hk/tc/18_districts/my_map_0' + str(i) + '_activities.htm')

    for j in range(10, 19):
        start_urls.append('https://www.had.gov.hk/tc/18_districts/my_map_' + str(j) + '_activities.htm')


    def parse(self, reponse):
        for url in HkGovHad_Activities_Tc.start_urls:
            yield scrapy.Request(url, callback=self.parselink)


    def parselink(self, response):
        rows = response.xpath("//table[@class='content-table  high-padding  desktop-table']//tbody/tr")
        event_list = []
        image = response.xpath("//div[@class='header-logo-tc']//img/@src").get()
        district = response.xpath("//div[@class='h1-wrapper']//h2//text()").get()
        district = re.sub('活動預告', '', district)
        last_revision_date = response.xpath("//div[@class='bottom-date']//div[@class='bottom-nav_item']//text()")[1].get()
        last_revision_date = re.sub('最近修訂日期 :', '', last_revision_date).strip()
        last_revision_date = process_date(last_revision_date[:last_revision_date.index('年')], '', last_revision_date)
        file = open(district + 'scraped_data.out', 'w')
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
            event = {'event district': district, 'event name': '', 'original date string': [], 'event start date': [], 'event end date':[], 'event duration string': [],
                     'event start time': [], 'event end time': [], 'event location': [], 'event description': '', 'event target audience': None,
                     'event contact person': None, 'event contact address': [], 'event contact tele': None,
                     'last update date': last_revision_date}

            for string in first_column:
                event['event name'] += string

            for string in second_column:
                if is_date(string):
                    event['original date string'].append(string)
                    try:
                        event['event start date'].append(convert_date(string)['starting date'])
                        event['event end date'].append(convert_date(string)['ending date'])
                    except:
                         event['event start date'].append("###")
                         event['event end date'].append("###")
                         print(event['event name'])
                elif is_time(string):
                    event['event duration string'].append(string)
                    try:
                        event['event start time'].append(convert_time(string)['starting time'])
                        event['event end time'].append(convert_time(string)['ending time'])
                    except:
                        event['event start time'].append("時間改變失敗")
                        event['event end time'].append("時間改變失敗")
                        print(event['event name'])
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


