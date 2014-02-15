# -*- coding: utf-8 -*-
__author__ = 'chanhle'
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import FormRequest, Request
from scrapy import log
from post_data import *
from datetime import datetime, timedelta
from hotel.models import Hotel, Hotel_Domain, Location, Room, Price_Book
import urllib
from random import randint
import re

hotel_info_path = {
    'hotel_domain': './/*[@id="ctl00_ContentMain_CitySearchResult_v2_rptSearchResults_ctl00_lnkHotelName"]',
    'name': './/*[@id="ctl00_ContentMain_CitySearchResult_v2_rptSearchResults_ctl00_lnkHotelName"]',
    'hotel_info_tag': '//*[@id="hotel_result_item"]',
    'star': 'ssrstars',
    'start_price': '//span[starts-with(@id,"ctl00_ContentMain_CitySearchResult_v2_rptSearchResults_ctl")][ends-with(@id,"_clblPrice")]',
    'score': '//a[starts-with(@id,"ctl00_ContentMain_CitySearchResult_v2_rptSearchResults_ctl")][ends-with(@id,"_lnkReviewScore")]/text()',

}

# class HotelDetail(CrawlSpider):




class HotelSpider(BaseSpider):
    name = "hotel"
    allowed_domains = ["agoda.com"]
    start_urls = [
        "http://www.agoda.com/city/ho-chi-minh-city-vn.html",
    ]
    
    date_start = None
    date_end = None
    
    def __init__(self, args={}, from_date=datetime.now() + timedelta(days=1),
                 to_date=datetime.now() + timedelta(days=3)):
        """
        Initial post data for search base on location
        """
        if args:
            from_date = args.get('from_date', datetime.now() + timedelta(days=1))
            to_date = args.get('to_date', datetime.now() + timedelta(days=3))
        elif not args and not from_date and not to_date:
            from_date = datetime.now() + timedelta(days=1)
            to_date = datetime.now() + timedelta(days=3)
        

        print "\n args==", args
        print "\n from date==", from_date
        post_data_search_base_on_location[
            'ctl00$ctl00$MainContent$area_promo$CitySearchBox1$arrivaldate'] = from_date.strftime("%m/%d/%Y")
        post_data_search_base_on_location[
            'ctl00$ctl00$MainContent$area_promo$CitySearchBox1$departdate'] = to_date.strftime("%m/%d/%Y")

        post_data_search_base_on_location['ddlCheckInDay'] = from_date.strftime("%d")
        post_data_search_base_on_location['ddlCheckInMonthYear'] = from_date.strftime("%m,%Y")
        post_data_search_base_on_location['ddlCheckOutDay'] = to_date.strftime("%d")
        post_data_search_base_on_location['ddlCheckOutMonthYear'] = to_date.strftime("%m,%Y")
        post_data_search_base_on_location[
            'ctl00$ctl00$MainContent$area_promo$CitySearchBox1$ddlNights'] = str((to_date - from_date).days)

        next_page_data['ctl00$ContentMain$DestinationSearchBox1$arrivaldate'] = from_date.strftime("%m/%d/%Y")
        next_page_data['ctl00$ContentMain$DestinationSearchBox1$ddlNights'] = str((to_date - from_date).days)
        next_page_data['ctl00$ContentMain$DestinationSearchBox1$departdate'] = to_date.strftime("%m/%d/%Y")
        next_page_data['ddlCheckInDay'] = from_date.strftime("%d")
        next_page_data['ddlCheckInMonthYear'] = from_date.strftime("%m,%Y")
        next_page_data['ddlCheckOutDay'] = to_date.strftime("%d")
        next_page_data['ddlCheckInMonthYear'] = to_date.strftime("%m,%Y")
        
        #assign value to global variable for later use
        self.date_start = from_date
        self.date_end = to_date

    def parse(self, response):
        log.msg("Start Scraping ....", level=log.INFO)
        sel = Selector(response)
        VIEWSTATE = sel.xpath('//input[@id="__VIEWSTATE"]/@value').extract()
        post_data_search_base_on_location['__VIEWSTATE'] = VIEWSTATE
        return [FormRequest.from_response(response,
                                          formdata=post_data_search_base_on_location,
                                          dont_click=True,
                                          callback=self.after_search)]

    def hotel_detail(self, response):
        log.msg("hotel detail", level=log.INFO)
        ran = randint(2, 10)  #Inclusive
        filename = 'detail' + str(ran)
        open(filename + '.html', 'wb').write(response.body)
        print 'HOTEL DETAL .....'
        sel = Selector(response)
        #        location = sel.xpath('//td[@id="ctl00_ctl00_MainContent_ContentMain_ThumbPhotos_rLocation"]/text()').extract()
#        number_of_rooms = sel.xpath(
#            '//td[@id="ctl00_ctl00_MainContent_ContentMain_ThumbPhotos_rRooms"]/text()').extract()
#            '//li[@id="ctl00_ctl00_MainContent_ContentMain_mainHotelPhotoHD_rRooms"]/span/text()').extract()
        
        hotel_name = sel.xpath('//span[@id="ctl00_ctl00_MainContent_ContentMain_HotelHeaderHD_lblHotelName"]/text()').extract()
        if len(hotel_name) == 0:
            hotel_name = sel.xpath('//span[@id="ctl00_ctl00_MainContent_ContentMain_hotelheader1_lblHotelName"]/text()').extract()
        
        hotel_name = hotel_name[0]
        
        description = sel.xpath(
            '//div[@id="ctl00_ctl00_MainContent_ContentMain_HotelInformation1_pnlDescription"]/div/text()').extract()
#            '//div[@id="ctl00_ctl00_MainContent_ContentMain_HotelInformation1_pnlDescription"]/div/div/span/text()').extract()
        room = sel.xpath('//tr[@class="tr553"]')
        room_name = room.xpath('.//td[@class="room_name"]/div/a/span/text()').extract()
        number_of_people = room.xpath(
            './/div[starts-with(@id, "ctl00_ctl00_MainContent_ContentMain_RoomTypesListGrid_AB1771_rptRateContent_ct")][contains(@id, "_pnlOccupancy")][@class="dek"]/text()').extract()
        number_of_people = filter(None, map(lambda x: re.sub('[\r\n\t]', '', x.split(',')[0]), number_of_people))
        number_of_people = [x for x in number_of_people if number_of_people.index(x)%2 ==0]
        
        price = room.xpath(
            './/td[contains(@class,"tex_center gray_r sgrayu row_padding_")]/div/span[2]/text()').extract()
        
        price = [x for x in price if price.index(x)%2 ==1]
#        from scrapy.shell import inspect_response
#        inspect_response(response, self)
        log.msg('file==='+'detail' + str(ran), level=log.INFO)
#        log.msg('====number_of_rooms========='+number_of_rooms[0], level=log.INFO)
        log.msg('====hotel_name========='+hotel_name, level=log.INFO)
        log.msg('====room_name========='+room_name[0], level=log.INFO)
        log.msg('======number_of_people======='+ number_of_people[0], level=log.INFO)
        log.msg('======price======='+price[0], level=log.INFO)
        log.msg("======description======="+ description[0], level=log.INFO)
        
        self.update_hotel(hotel_name, description[0])
        self.create_room(hotel_name, room_name, number_of_people, price)
        
    def create_room(self, hotel_name, room_name, number_of_people, price):
        log.msg("create room for"+ hotel_name, level=log.INFO)
        hotel_domain_obj, created = Hotel_Domain.objects.get_or_create(name='agoda.com', priority=1)
        hotel_obj = Hotel.objects.filter(name=hotel_name)[0]
        log.msg("hotel_obj room"+str(hotel_obj.name), level=log.INFO)
        for pos in range(0, len(room_name)):
            log.msg("name ...." + room_name[pos], level=log.INFO)
            room_obj, created = Room.objects.get_or_create(hotel=hotel_obj,
                                       name = room_name[pos],
                                       number_of_people = number_of_people[pos])
            log.msg("price:"+ price[0], level=log.INFO)
            self.create_price_book_period(hotel_obj, room_obj, price[pos])
    
    
    def create_price_book_period(self, hotel_obj, room_obj, price):
        log.msg("create price infog"+price, level=log.INFO)
        hotel_domain_obj, created = Hotel_Domain.objects.get_or_create(name='agoda.com', priority=1)
        Price_Book.objects.get_or_create(hotel = hotel_obj,
                                        room = room_obj,
                                        hotel_domain = hotel_domain_obj,
                                        date_start = self.date_start,
                                        date_end = self.date_end,
                                        price = float(price))

    def create_hotel(self, name, href, location_obj, star_rating, users_rating, currency, lowest_price, address, area):
        
        hotel_domain_obj, created = Hotel_Domain.objects.get_or_create(name='agoda.com', priority=1)
        if len(href) and len(name) and len(currency) and len(users_rating) and len(address) and len(area):
            log.msg("len name ...." + str(name[0]), level=log.INFO)
            for pos in range(0, len(name)):
                log.msg("name ...." + str(pos), level=log.INFO)
                rating = star_rating[pos] and star_rating[pos].split(' ')[0].replace('ssrstars', '')[0] or 1
                hotel_obj, created = Hotel.objects.get_or_create(hotel_domain=hotel_domain_obj,
                                            src=href[pos],
                                            name=name[pos],
                                            location=location_obj,
                                            currency=currency[pos],
                                            address=address[pos],
                                            area=area[pos],
                                            defaults={'star_rating': rating, 
                                                      'user_rating': float(users_rating[pos]),
                                                      'lowest_price': lowest_price[pos],
                                                      }
                                            )
                if not created and lowest_price[pos] < hotel_obj.lowest_price:
                    Hotel.objects.filter(pk=hotel_obj.id).update(lowest_price = lowest_price[pos])
                    
        
        log.msg("end len name ...." + str(len(name)), level=log.INFO)

    def update_hotel(self, hotel_name, description):
        if description:
            log.msg("update description for hotel=="+ description)
            log.msg("hotel_name for hotel=="+ hotel_name)
            obj = Hotel.objects.filter(name=hotel_name).update(description = description)
    
    
        
    def create_location(self, location):
        short_name = re.sub(' ', '', location)
        object, create = Location.objects.get_or_create(name=location,
                                                        short_name=short_name)
        return object


    def after_search(self, response):

        ran = randint(2, 10)  #Inclusive
        filename = response.url.split("/")[-2] + str(ran)
        open(filename + '.html', 'wb').write(response.body)
        
        log.msg("After Search ...."+ filename, level=log.INFO)
        sel = Selector(response)
        info = sel.xpath(hotel_info_path['hotel_info_tag'])
        name = info.xpath('.//a[@class="hot_name"]/text()').extract()
        urls = info.xpath('.//a[@class="hot_name"]').xpath(
            '@href').extract()
        href = filter(None, map(lambda x: x.split('?')[0], urls))

        currency = info.xpath('.//div/span[@class="fontxlargeb purple"]/span/text()').extract()

        lowest_price = []
        list_price = info.xpath('.//div/span[@class="fontxlargeb purple"]/text()').extract()
        for price in list_price:
            try:
                lowest_price.append(int(price))
            except:
                pass

                #        Get location of hotel like hochiminh, singapore
        location = sel.xpath('//*[@id="ctl00_head1"]/title/text()').extract()
        if location:
            location = location[0]
            location = re.sub('[\r\n\t]', '', location)
            location = location[:-7] #delete ' Hotels' at the end of the string location
        else:
            location = ''
        location_obj = self.create_location(location)

        #        Get the rating of hotel, some hotel dont have user rating. So boring
        users_rating = []
        for pos in range(1, len(name) + 1):
            startIDofA = "ctl00_ContentMain_CitySearchResult_v2_rptSearchResults_ctl"
            lastIDofA = "_lnkReviewScore"
            if pos < 10:
                IDofA = startIDofA + "0" + str(pos) + lastIDofA
            else:
                IDofA = startIDofA + str(pos) + lastIDofA
            xpathquery = './/a[@id="' + IDofA + '"]/text()'

            user_rating = info.xpath(xpathquery).extract()
            if user_rating:
                users_rating.append(user_rating[0].encode('ascii', 'ignore')[-3:])
            else:
                users_rating.append(0)

        address = info.xpath('.//span[@class="fontsmalli"]/text()').extract()
        area = info.xpath('.//p/span[@class="black fontsmallb"]/text()').extract()
        type = info.xpath('.//p/span[2][@class="fontsmallb black"]/text()').extract()
        star_rating = info.xpath('.//input[starts-with(@class,"ssrstars")]/@class').extract()

        self.create_hotel(name, href, location_obj, star_rating, users_rating, currency, lowest_price, address, area)
        for url in urls:
            yield Request(url='http://www.agoda.com' + url, callback=self.hotel_detail)
        log.msg("-------------NEXT PAGE-----------", level=log.INFO)
        print '\n------------NEXT PAGE--------------'
        VIEWSTATE = sel.xpath('//input[@id="__VIEWSTATE"]/@value').extract()
        next_page_data['__VIEWSTATE'] = VIEWSTATE
        next_page_datax = urllib.urlencode(next_page_data)

        yield Request(url=response.url, method='POST',
                      body=next_page_datax, callback=self.after_search,
                      headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                               "Accept-Encoding": "gzip,deflate,sdch",
                               "Accept-Language": "vi,en-US;q=0.8,en;q=0.6",
                               "Cache-Control": "max-age=0",
                               "Connection": "keep-alive",
                               "Content-Type": "application/x-www-form-urlencoded"})