import re
import sys

import scrapy
import scrapy.http
import dateutil.parser

class TimeAndDate_Com(scrapy.Spider):
    name = "timeanddate_com"

    def __init__(self, country, out=None):
        super(TimeAndDate_Com, self).__init__()
        self.country = country
        self.out = out

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
                    'Feriado Nacional', # Brazil
            ]:
                continue
            title = columns[2]
            extra_text = u' '.join(columns[4:])
            if len(extra_text) > 1:
                title = u'{} ({})'.format(title, extra_text)
            days.append({
                'date': unicode(dateutil.parser.parse(columns[0]).date()),
                'title': title,
            })
        if not self.out or self.out == '-':
            outfile = sys.stdout
        else:
            outfile = open(self.out, 'w')
        outfile.write(u'holidays:\n{}'.format(
            u'\n'.join([u'  - {}  # {}'.format(
                day['date'],
                day['title']
            ) for day in days])
        ).encode('utf-8'))
