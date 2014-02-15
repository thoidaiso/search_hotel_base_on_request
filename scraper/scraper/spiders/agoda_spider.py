# -*- coding: utf-8 -*-
__author__ = 'sepdau'

from scrapy.selector import Selector
from scrapy.http import FormRequest, Request
from scrapy import log
import urllib
from random import randint
import re
from hotel_spider import HotelSpider
from post_data import *

hotel_info_path = {
    'hotel_domain': './/*[@id="ctl00_ContentMain_CitySearchResult_v2_rptSearchResults_ctl00_lnkHotelName"]',
    'name': './/*[@id="ctl00_ContentMain_CitySearchResult_v2_rptSearchResults_ctl00_lnkHotelName"]',
    'hotel_info_tag': '//*[@id="hotel_result_item"]',
    'star': 'ssrstars',
    'start_price': '//span[starts-with(@id,"ctl00_ContentMain_CitySearchResult_v2_rptSearchResults_ctl")][ends-with(@id,"_clblPrice")]',
    'score': '//a[starts-with(@id,"ctl00_ContentMain_CitySearchResult_v2_rptSearchResults_ctl")][ends-with(@id,"_lnkReviewScore")]/text()',

}


class AgodaSpider(HotelSpider):
    name = 'agoda'
    allowed_domains = ["agoda.com"]
    start_urls = [
        "http://www.agoda.com/city/ho-chi-minh-city-vn.html",
    ]

    def parse(self, response):
        # initial post
        """

        @param response:
        @return:
        """
        post_data_search_base_on_location[
            'ctl00$ctl00$MainContent$area_promo$CitySearchBox1$arrivaldate'] = self.from_date.strftime("%m/%d/%Y")
        post_data_search_base_on_location[
            'ctl00$ctl00$MainContent$area_promo$CitySearchBox1$departdate'] = self.to_date.strftime("%m/%d/%Y")

        post_data_search_base_on_location['ddlCheckInDay'] = self.from_date.strftime("%d")
        post_data_search_base_on_location['ddlCheckInMonthYear'] = self.from_date.strftime("%m,%Y")
        post_data_search_base_on_location['ddlCheckOutDay'] = self.to_date.strftime("%d")
        post_data_search_base_on_location['ddlCheckOutMonthYear'] = self.to_date.strftime("%m,%Y")
        post_data_search_base_on_location[
            'ctl00$ctl00$MainContent$area_promo$CitySearchBox1$ddlNights'] = str((self.to_date - self.from_date).days)
        sel = Selector(response)
        view_state = sel.xpath('//input[@id="__VIEWSTATE"]/@value').extract()
        post_data_search_base_on_location['__VIEWSTATE'] = view_state

        next_page_data['ctl00$ContentMain$DestinationSearchBox1$arrivaldate'] = self.from_date.strftime("%m/%d/%Y")
        next_page_data['ctl00$ContentMain$DestinationSearchBox1$ddlNights'] = str((self.to_date - self.from_date).days)
        next_page_data['ctl00$ContentMain$DestinationSearchBox1$departdate'] = self.to_date.strftime("%m/%d/%Y")
        next_page_data['ddlCheckInDay'] = self.from_date.strftime("%d")
        next_page_data['ddlCheckInMonthYear'] = self.from_date.strftime("%m,%Y")
        next_page_data['ddlCheckOutDay'] = self.to_date.strftime("%d")
        next_page_data['ddlCheckInMonthYear'] = self.to_date.strftime("%m,%Y")

        log.msg("Start Scraping ....", level=log.INFO)
        return [FormRequest.from_response(response,
                                          formdata=post_data_search_base_on_location,
                                          dont_click=True,
                                          callback=self.after_search)]

    def hotel_detail(self, response):
        """

        @param response:
        """
        log.msg("HOTEL DETAIL ....", level=log.INFO)
        sel = Selector(response)

        location = sel.xpath('//td[@id="ctl00_ctl00_MainContent_ContentMain_ThumbPhotos_rLocation"]/text()').extract()
        number_of_rooms = sel.xpath(
            '//td[@id="ctl00_ctl00_MainContent_ContentMain_ThumbPhotos_rRooms"]/text()').extract()
        description = sel.xpath(
            '//div[@id="ctl00_ctl00_MainContent_ContentMain_HotelInformation1_pnlDescription"]/div/text()').extract()
        room = sel.xpath('//tr[@class="tr553"]')
        room_name = room.xpath('.//td[@class="room_name"]/div/a/span/text()').extract()
        number_of_people = room.xpath(
            './/div[starts-with(@id, "ctl00_ctl00_MainContent_ContentMain_RoomTypesListGrid_AB1771_rptRateContent_ct")][contains(@id, "_pnlOccupancy")][@class="dek"]/text()').extract()
        number_of_people = filter(None, map(lambda x: re.sub('[\r\n\t]', '', x.split(',')[0]), number_of_people))
        price = room.xpath(
            './/td[contains(@class,"tex_center gray_r sgrayu row_padding_")]/div/span[2]/text()').extract()
        print '=============', room_name
        print '=============', number_of_people
        print '=============', price


    def after_search(self, response):
        """

        @param response:
        """
        log.msg("After Search ....", level=log.INFO)
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
        rating = []
        for el in star_rating:
            rating.append(el and el.split(' ')[0].replace('ssrstars', '')[0] or 1)
        log.msg("Create Hotel", level=log.INFO)
        self.create_hotel('agoda.com', name, href, location_obj, rating, users_rating, currency, lowest_price, address,
                          area)
        for url in urls:
            yield Request(url='http://www.agoda.com' + url, callback=self.hotel_detail)

        log.msg("NEXT PAGE", level=log.INFO)
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