import re

import scrapy
import scrapy.http
import dateutil.parser

def strip_non_ascii(text):
    return re.sub('[^\x00-\x7F]', '_', text)

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
            if holiday_type not in [
                    'National holiday', 
                    'Bank holiday', 
                    'Local holiday',
                    'Common Local holidays',
            ]:
                continue
            title = strip_non_ascii(columns[2])
            extra_text = strip_non_ascii(u' '.join(columns[4:]))
            if len(extra_text) > 1:
                title = '{} ({})'.format(title, extra_text)
            days.append({
                'date': repr(str(dateutil.parser.parse(columns[0]).date())),
                'title': title,
            })
        print(
            u'Holidays are:\n    [\n{}    ]'.format(u''.join([
                u'        {},  # {}\n'.format(
                    day['date'], 
                    day['title'],
                ) for day in days
            ]))
        )
