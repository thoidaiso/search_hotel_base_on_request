# -*- coding: utf-8 -*-
__author__ = 'sepdau'

from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import FormRequest, Request
from scrapy import log
from post_data import *
from datetime import datetime, timedelta
from hotel.models import Hotel, Hotel_Domain, Location
import urllib
from random import randint
import re


class IvivuSpider(BaseSpider):
    name = "ivivu"
    allowed_domains = ["ivivu.com"]
    start_urls = [
        "http://www.ivivu.com/en/hotels/asia/vietnam/ho-chi-minh-city/all/1162/",
    ]

    def __init__(self, args={}, from_date=datetime.now() + timedelta(days=1),
                 to_date=datetime.now() + timedelta(days=3)):

        self.from_date = ''
        self.to_date = ''
        if args:
            self.from_date = args.get('from_date', datetime.now() + timedelta(days=1))
            self.to_date = args.get('to_date', datetime.now() + timedelta(days=3))
        elif not args and not self.from_date and not self.to_date:
            self.from_date = datetime.now() + timedelta(days=1)
            self.to_date = datetime.now() + timedelta(days=3)
            # ivivu_search['sbk_date_from'] = from_date.strftime("%d-%m-%Y")
        # ivivu_search['sbk_date_to'] = to_date.strftime("%d-%m-%Y")
        # ivivu_search['sbk_n_nights'] = str((to_date - from_date).days)

        ivivu_search['datefrom'] = from_date.strftime("%Y-%m-%d")
        ivivu_detail['datefrom'] = from_date.strftime("%Y-%m-%d")
        self.page = 1

    def parse(self, response):
        log.msg("Start Scraping ....", level=log.INFO)
        url = 'http://www.ivivu.com/request.php?' + urllib.urlencode(ivivu_search)
        yield Request(url=url, callback=self.after_search, meta={'page': 1})


    def create_location(self, location):
        object, create = Location.objects.get_or_create(name=location)
        return object

    def get_detail(self, response):
        sel = Selector(response)
        rooms = sel.xpath('//div[@class="room"]')
        room_name = rooms.xpath('//div[@class="room"]/table/tbody/tr/th/a/text()').extract()
        print room_name
        price = 0
        for room in rooms:
            days = room.xpath('//div[@class="date-inner"]/span[2]/text()')
            for position, day in enumerate(days):
                print '\n================', day.extract(), position
                if int(day.extract()) in range(self.from_date.day, self.to_date.day):
                    print "x", day.extract(), position
                    print room.xpath('.//div[@class="deal"]/span/text()').extract()
                    price += float(room.xpath('.//div[@class="deal"]/span/text()').extract()[position])
        print 'PRICE -------------------', price

    def hotel_detail(self, response):
        sel = Selector(response)
        img = sel.xpath('//div[@class="slide-image"]/div/ul/li/a/@href').extract()
        print 'IMAGE ----------', img


        yield Request(url='http://www.ivivu.com/request.php?' + urllib.urlencode(ivivu_detail),
                      callback=self.get_detail)

    def after_search(self, response):

        sel = Selector(response)
        info = sel.xpath('//div[@id="results-list"]')
        name = info.xpath('.//li/h2/a[@class="hrefHD"]/text()').extract()
        href = info.xpath('.//li/h2/a/@href').extract()
        address = info.xpath('.//div[@class="location"]/text()').extract()
        description = info.xpath('.//p[@class="desc"]/text()').extract()
        currency = sel.xpath('.//td/span[@class="amount"]/text()').re(r'([A-Za-z-]+)')
        star_rating = info.xpath('.//li/h2/a/img/@src').re(r'([0-9-]+\.[0])')
        users_rating = info.xpath('.//div/span/span/text()').extract()
        lowest_price = []
        list_price = sel.xpath('.//td/span[@class="amount"]/text()').re(r'([0-9-]+)')
        for price in list_price:
            try:
                lowest_price.append(int(price))
            except:
                pass
        print name
        # print href
        # print address
        # print description
        # print currency
        # print star_rating
        # print list_price
        for url in href[0:1]:
            yield Request(url=url, callback=self.hotel_detail)

        print '\n NEXT PAGE--------'
        if not name:
            print 'Complete ----------'
            return
        self.page += 1
        ivivu_search['page'] = self.page
        # yield Request(url='http://www.ivivu.com/request.php?' + urllib.urlencode(ivivu_search),
        #               callback=self.after_search)


    def create_hotel(self, name, href, location_obj, star_rating, users_rating, currency, lowest_price, address, area):
        log.msg("len name ...." + str(len(name)), level=log.INFO)
        for pos in range(0, len(name)):
            log.msg("name ...." + str(pos), level=log.INFO)
            obj, created = Hotel_Domain.objects.get_or_create(name='agoda.com', priority=1)
            rating = star_rating[pos] and star_rating[pos].split(' ')[0].replace('ssrstars', '')[0] or 1
            Hotel.objects.get_or_create(hotel_domain=obj,
                                        src=href[pos],
                                        name=name[pos],
                                        location=location_obj,
                                        currency=currency[pos],
                                        lowest_price=lowest_price[pos],
                                        user_rating=float(users_rating[pos]),
                                        address=address[pos],
                                        area=area[pos],
                                        defaults={'star_rating': rating})

