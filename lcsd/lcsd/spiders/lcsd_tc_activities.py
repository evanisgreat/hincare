from pathlib import Path

import scrapy
import json
import re
from datetime import datetime


class HkGovHad_Activities(scrapy.Spider):
    name = "hkgovhad_activities_eng"
    start_urls = ['https://www.lcsd.gov.hk/tc/']


    def parse(self, reponse):
        for url in HkGovHad_Activities.start_urls:
            yield scrapy.Request(url, callback=self.parselink)

