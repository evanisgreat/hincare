from typing import Any

import scrapy
from scrapy.http import Response


class HKPplTravel(scrapy.Spider):

    name = 'hkppltravel'
    start_urls = ['https://hkppltravel.com/category/events/']

    def parse(self, response):
        list = response.xpath("//div[@class='title-wrap']//@href").getall()
        for link in list:
            yield scrapy.Request(link, callback=self.parselink)


    def parselink(self, response):
        event = {'name': '', 'subcategory activities': [], 'date': [], 'time': [], 'location': [], 'about': '', 'image_link': '', 'website url': ''}

        url = response.xpath("//link[@rel='canonical']/@href").get()

        subheader_names = response.xpath('//div[1]/div/div/main/article/div[3]/div/h2//text()').getall()

        for subheader_name in subheader_names:
            event['subcategory activities'].append(subheader_name)

        event['website url'] = url

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

        for text in event_text:
            if '日期：' in text:
                event['date'].append(text)
            elif '時間：' in text:
                event['time'].append(text)
            elif '地點：' in text or '地址：' in text:
                event['location'].append(text)
            else:
                event['about'] += text + "\n"

        img_link = response.xpath("//figure[@class='wp-block-image size-large']/img/@data-src").get()

        print(img_link)

        event['image_link'] = img_link

        if len(event['date']) == 0:
            event['date'].append("any time")

        if len(event['time']) == 0:
            event['time'].append("any time")

        yield event
