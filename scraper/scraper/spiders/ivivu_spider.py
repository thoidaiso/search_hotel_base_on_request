# -*- coding: utf-8 -*-
__author__ = 'sepdau'

from hotel_spider import HotelSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log
import urllib
from post_data import *
from datetime import datetime, timedelta


class IvivuSpider(HotelSpider):
    name = "ivivu"
    allowed_domains = ["ivivu.com"]
    start_urls = [
        "http://www.ivivu.com/en/hotels/asia/vietnam/ho-chi-minh-city/all/1162/",
    ]

    def __init__(self, args={}, from_date=datetime.now() + timedelta(days=1),
                 to_date=datetime.now() + timedelta(days=3)):
        """

        @param args:
        @param from_date:
        @param to_date:
        """
        self.page = 1
        super(IvivuSpider, self).__init__(args, from_date, to_date)

    def parse(self, response):
        """

        @param response:
        """
        # initial data
        ivivu_search['datefrom'] = self.from_date.strftime("%Y-%m-%d")
        ivivu_detail['date_from'] = self.from_date.strftime("%d-%m-%Y")
        ivivu_detail['date_to'] = self.to_date.strftime("%d-%m-%Y")

        log.msg("Start Scraping ....", level=log.INFO)
        url = 'http://www.ivivu.com/request.php?' + urllib.urlencode(ivivu_search)
        yield Request(url=url, callback=self.after_search)

    def after_search(self, response):
        """

        @param response:
        @return:
        """
        sel = Selector(response)
        info = sel.xpath('//div[@id="results-list"]')
        name = info.xpath('.//li/div/h2/a[@class="hrefHD"]/text()').extract()
        href = info.xpath('.//li/div/h2/a/@href').extract()
        address = info.xpath('.//li/div/span/text()').extract()
        description = ''

        star_rating = info.xpath('//li/div/h2/img[@class="rating"]/@src').re(r'([0-9-]+\.[0])')
        users_rating = info.xpath('.//strong[@class="review_score"]/text()').re(r'([0-9-].[0-9-])')
        lowest_price = []
        if ivivu_search['iso_currency_code'] == 'VND':
            currency = sel.xpath('.//div/span/div[@class="price_from"]').re(r'([A-Za-z-]+)')
            list_price = sel.xpath('.//div/span/div[@class="price_from"]/text()').re(r'([0-9-]+)')
        elif ivivu_search['iso_currency_code'] == 'USD':
            currency = sel.xpath('.//span[@class="amount block"]/text()').re(r'([A-Za-z-]+)')
            list_price = sel.xpath('.//span[@class="amount block"]/text()').re(r'([0-9-]+)')

        for price in list_price:
            try:
                lowest_price.append(int(price))
            except:
                pass
        print users_rating
        print currency
        print list_price
        for url in href[0:1]:
            yield Request(url=url, callback=self.hotel_detail)

        print '\n NEXT PAGE--------'
        if not name:
            print 'Complete ----------'
            return
            self.page += 1
            ivivu_search['page'] = self.page
            yield Request(url='http://www.ivivu.com/request.php?' + urllib.urlencode(ivivu_search),
                          callback=self.after_search)

    def get_detail(self, response):
        """

        @param response:
        """
        sel = Selector(response)
        rooms = sel.xpath('//div[@class="table_hoteldetail after"]')
        room_name = rooms.xpath('.//h2/text()').extract()
        print room_name
        price = rooms.xpath('//span[@class="price "]/text()').re(r'([0-9-].[0-9-])')
        print 'PRICE -------------------', price
        number_of_people = rooms.xpath('.//td[@valign="middle"][@class="col_2"]')
        print number_of_people

    def hotel_detail(self, response):
        """

        @param response:
        """
        sel = Selector(response)
        img = sel.xpath('//div[@class="contents_new_box"]/ul/li/a[@class="hover_bg_inset"]/@href').extract()
        print 'IMAGE ----------', img
        ivivu_detail['hotelId'] = response.url.split('/')[-2].split('-')[-1]
        print ivivu_detail

        yield Request(url='http://www.ivivu.com/request.php?' + urllib.urlencode(ivivu_detail),
                      callback=self.get_detail)
