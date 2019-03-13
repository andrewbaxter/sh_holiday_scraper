import datetime

import scrapy
import scrapy.http
import dateparser


class TimeAndDate_Com(scrapy.Spider):
    name = "timeanddate_com"
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    def __init__(self, country, years='', out=None):
        super(TimeAndDate_Com, self).__init__()
        self.country = country
        self.years = years.split(',')
        if not self.years[0]:
            self.years = [datetime.datetime.now().year]
        self.out = out

    def start_requests(self):
        url = 'https://www.timeanddate.com/holidays/{}/'.format(self.country)
        for year in self.years:
            yield scrapy.http.Request(url + year, meta={'year': year})

    def parse(self, response):
        for row in response.xpath(
                '//table[contains(@class,"tb-cl")]/tbody/tr'):
            columns = [
                u''.join(column.xpath('.//text()').extract())
                for column in row.xpath('./td|./th')
            ]
            holiday_type = columns[3]
            if holiday_type not in [
                    'National holiday',
                    'Bank holiday',
                    'Local holiday',
                    'Common Local holidays',
                    'Feriado Nacional',  # Brazil
            ]:
                continue
            title = columns[2]
            extra_text = u' '.join(columns[4:])
            if len(extra_text) > 1:
                title = u'{} ({})'.format(title, extra_text)
            date = dateparser.parse(columns[0]).date()
            date = date.replace(year=int(response.meta['year']))
            yield {
                'date': str(date),
                'title': title,
            }
