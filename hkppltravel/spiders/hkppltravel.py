from distutils.command.check import check
from typing import Any

import scrapy
from scrapy.http import Response

# checks if url follows conventions
def check_url(urls):
    no_url = True
    no_format = True
    multiple_url = True

    if len(urls) > 0:
        no_url = False
    elif len(urls) == 1:
        multiple_url = False

    return_string = urls[0]

    if 'https' in return_string and ('.com' in return_string or '.hk' in return_string):
        no_format = False

    if no_url:
        return_string += '*'
    if no_format:
        return_string += '@'
    if multiple_url:
        return_string += '#'

    return return_string


# checks if date follows conventions
def check_date(dates):
    no_date = True
    no_format = True
    multiple_date = True

    if len(dates) > 0:
        no_date = False
        return '*'
    elif len(dates) == 1:
        multiple_date = False
    else:
        return '*'

    return_string = dates[0]

    if '月' in return_string and '日' in return_string:
        no_format = False

    if no_date:
        return_string += '*'
    if no_format:
        return_string += '@'
    if multiple_date:
        return_string += '#'

    return return_string


# checks if time follows conventions
def check_time(times):
    no_time = True
    no_format = True
    multiple_time = True

    if len(times) > 0:
        no_time = False
    elif len(times) == 1:
        multiple_time = False
    else:
        return '*'

    return_string = times[0]

    if '時' in return_string or ':' in return_string:
        no_format = False

    if no_time:
        return_string += '*'
    if no_format:
        return_string += '@'
    if multiple_time:
        return_string += '#'

    return return_string


# checks if location follows conventions
def check_location(locs):
    no_loc = True
    no_format = True
    multiple_loc = True

    if len(locs) > 0:
        no_loc = False
        return '*'
    elif len(locs) == 1:
        multiple_loc = False
    else:
        return '*'

    return_string = locs[0]

    if '地點' in return_string or '地址' in return_string:
        no_format = False

    if no_loc:
        return_string += '*'
    if no_format:
        return_string += '@'
    if multiple_loc:
        return_string += '#'

    return return_string


class HKPplTravel(scrapy.Spider):

    name = 'hkppltravel'
    start_urls = ['https://hkppltravel.com/category/events/']

    def parse(self, response):
        list = response.xpath("//div[@class='title-wrap']//@href").getall()
        for link in list:
            yield scrapy.Request(link, callback=self.parselink)


    def parselink(self, response):
        event = {'name': '', 'subcategory activities': [], 'date': '', 'time': '', 'location': '', 'about': '', 'image_link': '', 'website url': ''}

        urls = response.xpath("//link[@rel='canonical']/@href").getall()
        print(urls)
        event['website url'] = check_url(urls)

        subheader_names = response.xpath('//div[1]/div/div/main/article/div[3]/div/h2//text()').getall()

        for subheader_name in subheader_names:
            event['subcategory activities'].append(subheader_name)

        subheader_names =  response.xpath("//strong//text()").getall()

        for subheader_name in subheader_names:
            event['subcategory activities'].append(subheader_name)

        name1 = response.xpath("//h1//text()").get()
        name2 = response.xpath("//h2//text()").get()

        print(name1)
        print(name2)

        if '【' in name1:
            event['name'] = name1
        elif '【' in name2:
            event['name'] = name2
        else:
            return

        event_text = response.xpath("//p//text()").getall()
        dates = []
        times = []
        locations = []

        for text in event_text:
            if '日期：' in text:
                dates.append(text)
            elif '時間：' in text:
                times.append(text)
            elif '地點：' in text or '地址：' in text:
                locations.append(text)
            else:
                event['about'] += text + "\n"

        img_link = response.xpath("//figure[@class='wp-block-image size-large']/img/@data-src").get()

        print(img_link)

        event['image_link'] = img_link

        event['date'] = check_date(dates)

        event['time'] = check_time(times)

        event['location'] = check_location(locations)

        print(len(event['time']))

        yield event
