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
        event = {'name': '', 'date': '', 'location': ''}

        event['name'] = response.xpath("//h2//text()").get()
        event_text = response.xpath("//p//text()").getall()

        for text in event_text:
            if '日期' in text:
                event['date'] = text
            elif '地點' in text:
                event['location'] = text

        yield event
