# -*- coding: utf-8 -*-
__author__ = 'chanhle'
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import FormRequest, Request
from scrapy import log
from post_data import *
from datetime import datetime, timedelta
from hotel.models import Hotel, Hotel_Domain
import urllib

hotel_info_path = {
    'hotel_domain': './/*[@id="ctl00_ContentMain_CitySearchResult_v2_rptSearchResults_ctl00_lnkHotelName"]',
    'name': './/*[@id="ctl00_ContentMain_CitySearchResult_v2_rptSearchResults_ctl00_lnkHotelName"]',
    'hotel_info_tag': '//*[@id="hotel_result_item"]',
    'star': 'ssrstars'
}


class HotelSpider(BaseSpider):
    name = "hotel"
    allowed_domains = ["agoda.com"]
    start_urls = [
        "http://www.agoda.com/city/ho-chi-minh-city-vn.html",
    ]

    def __init__(self, args=[], from_date=datetime.now() + timedelta(days=1), to_date=datetime.now() + timedelta(days=3)):
        """
        Initial post data for search base on location
        """
        if args:
            from_date = args[0]
            to_date = args[1]
        elif not args and not from_date and not to_date:
            from_date=datetime.now() + timedelta(days=1)
            to_date=datetime.now() + timedelta(days=3)
            
        print "\n args==",args
        print "\n from date==",from_date
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

    def parse(self, response):
        log.msg("Start Scraping ....", level=log.INFO)
        return [FormRequest.from_response(response,
                                          formdata=post_data_search_base_on_location,
                                          dont_click=True,
                                          callback=self.after_search)]


    def next_page(self, response):
        print '\n------------NEXT PAGE--------------'
        next_page_datax = urllib.urlencode(next_page_data)

        return Request(url=response.url, method='POST',
                       body=next_page_datax, callback=self.after_search,
                       headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                                "Accept-Encoding": "gzip,deflate,sdch",
                                "Accept-Language": "vi,en-US;q=0.8,en;q=0.6",
                                "Cache-Control": "max-age=0",
                                "Connection": "keep-alive",
                                "Content-Type": "application/x-www-form-urlencoded"})

    def go_to_hotel(self, link):
        return Request(url=link, callback=self.hotel_detail)

    def hotel_detail(self, response):
        print 'HOTEL DETAL .....'


    def create_hotel(self, name, href, location, star_rating):
        for pos in range(0, len(name)):
            obj, created = Hotel_Domain.objects.get_or_create(name='agoda.com', priority=1)
            rating = star_rating[pos] and star_rating[pos].split(' ')[0].replace('ssrstars', '')[0] or 1
            Hotel.objects.get_or_create(hotel_domain=obj, src=href[pos], name=name[pos], location=location[pos],
                                        defaults={'star_rating': rating})


    def after_search(self, response):
        log.msg("After Search ....", level=log.INFO)
        from random import randint

        ran = randint(2, 10)  #Inclusive
        filename = response.url.split("/")[-2] + str(ran)
        open(filename + '.html', 'wb').write(response.body)

        sel = Selector(response)
        info = sel.xpath(hotel_info_path['hotel_info_tag'])
        name = info.xpath('.//a[@class="hot_name"]/text()').extract()
        urls = info.xpath('.//a[@class="hot_name"]').xpath(
            '@href').extract()
        href = filter(None, map(lambda x: x.split('?')[0], urls))
        location = info.xpath('.//p/span[@class="black fontsmallb"]/text()').extract()
        star_rating = info.xpath('.//input[starts-with(@class,"ssrstars")]/@class').extract()
        self.create_hotel(name, href, location, star_rating)
        for url in urls:
            yield Request(url='http://www.agoda.com' + url, callback=self.hotel_detail)

        yield self.next_page(response)