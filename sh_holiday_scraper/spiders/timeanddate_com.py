import re

import scrapy
import scrapy.http
import dateutil.parser

class TimeAndDate_Com(scrapy.Spider):
    name = "timeanddate_com"

    def __init__(self, country):
        super(TimeAndDate_Com, self).__init__()
        self.country = country

    def start_requests(self):
        yield scrapy.http.Request('http://www.timeanddate.com/holidays/{}/'.format(self.country))

    def parse(self, response):
        days = []
        for row in response.xpath('//table[contains(@class,"tb-cl")]/tbody/tr'):
            columns = [u''.join(column.xpath('.//text()').extract()) for column in row.xpath('./td|./th')]
            holiday_type = columns[3]
            if holiday_type not in ['National holiday', 'Bank holiday']:
                continue
            days.append({
                'date': repr(str(dateutil.parser.parse(columns[0]).date())),
                'title': re.sub('[^\x00-\x7F]', '_', columns[2]),
            })
        print(
            u'Holidays are:\n    [\n{}    ]'.format(u''.join([
                u'        {},  # {}\n'.format(
                    day['date'], 
                    day['title'],
                ) for day in days
            ]))
        )
