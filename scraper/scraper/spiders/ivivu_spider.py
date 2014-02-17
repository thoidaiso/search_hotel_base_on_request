# -*- coding: utf-8 -*-
__author__ = 'sepdau'

from hotel_spider import HotelSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log
import urllib
from post_data import *
from datetime import datetime, timedelta
import re

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
#        from scrapy.shell import inspect_response
#        inspect_response(response, self)
        info = sel.xpath('//div[@id="results-list"]')
        name = info.xpath('.//li/div/h2/a[@class="hrefHD"]/text()').extract()
        href = info.xpath('.//li/div/h2/a/@href').extract()
        address = info.xpath('.//li/div/span/text()').extract()
        description = ''

        star_rating = info.xpath('//li/div/h2/img[@class="rating"]/@src').re(r'([0-9-]+\.[0-9])')
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
#        print "star name==",name
#        print "star href==",href
#        print "star address==",address
#        print "star users_rating==",users_rating
#        print "star rating==",star_rating
#        print currency
        print "price==",lowest_price
        for url in href:
            yield Request(url=url, callback=self.hotel_detail)

        area = ['' for x in name]
        
#        Get location city of hotel
        location = sel.xpath('//span[@itemprop="offerCount"]/text()').extract()
#        print "\n location===",location
        location = len(location) and location[0].replace('hotels in','')
        location = re.sub('[(1-9]', '', location).strip()   
#        print "\n location===",location
        
        location_obj = self.create_location(location)
        self.create_hotel('ivivu.com', name, href, location_obj, star_rating, users_rating, currency, lowest_price, address,
                          area, 2)
        
        print '\n NEXT PAGE--------', self.page
        if name:
            self.page += 1
            ivivu_search['page'] = self.page
            yield Request(url='http://www.ivivu.com/request.php?' + urllib.urlencode(ivivu_search),
                          callback=self.after_search)

    def get_detail(self, response):
        """
        Response:: Room Info
        @param response:
        """
        hotel_name = response.meta['hotel']
        sel = Selector(response)
#        from scrapy.shell import inspect_response
#        inspect_response(response, self)
        rooms = sel.xpath('//div[@class="table_hoteldetail after"]')
        room_name = rooms.xpath('.//h2/text()').extract()
        print room_name
        price = rooms.xpath('//span[@class="price "]/text()').re(r'([0-9-].[0-9-])')
        print 'PRICE -------------------', price
        number_of_people_data = rooms.xpath('.//td[@valign="middle"][@class="col_2"]/text()').extract()
        number_of_people = []
        for number in number_of_people_data:
            number_of_people.append( number.replace('\r\n','').strip()) 
        print "\n number_of_people==",number_of_people
        
#        print "\n hotel_name==",hotel_name
        self.create_room(hotel_name, room_name, number_of_people, price)

    def hotel_detail(self, response):
        """

        @param response:
        """
        sel = Selector(response)
#        from scrapy.shell import inspect_response
#        inspect_response(response, self)
        img = sel.xpath('//div[@class="contents_new_box"]/ul/li/a[@class="hover_bg_inset"]/@href').extract()
#        print '\n\nIMAGE ----------', img
        ivivu_detail['hotelId'] = response.url.split('/')[-2].split('-')[-1]
        print ivivu_detail
        
        description =  sel.xpath('//div[@class="new_box"]/div/div').extract()[2]
        if '<div' in description:
            description = description[ description.index('>')+1:]
            description = description.replace('</div>','').replace('\r\n','').replace('<br>','').strip()
        
        service_data = sel.xpath('//ul[contains(@class,"facilities")]/li/text()').extract()
        service = self.get_hotel_service(service_data)
        
        hotel_name = sel.xpath('//h1[@id="hotelName"]/text()').extract()[0]
        hotel_name = hotel_name.encode('ascii', 'ignore').strip()
        print "\n description===",description
#        print "\n service==",service
#        print "\n hotel name==",hotel_name
        self.update_hotel(hotel_name, description, service)
        for image in img:
            self.create_image(hotel_name, image, False)
        
        yield Request(url='http://www.ivivu.com/request.php?' + urllib.urlencode(ivivu_detail),
                      callback=self.get_detail, meta={'hotel': hotel_name})
