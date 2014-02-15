# -*- coding: utf-8 -*-
__author__ = 'chanhle'
from scrapy.spider import BaseSpider
from scrapy import log
from datetime import datetime, timedelta
from hotel.models import Hotel, Hotel_Domain, Location


class HotelSpider(BaseSpider):
    def __init__(self, args={}, from_date=datetime.now() + timedelta(days=1),
                 to_date=datetime.now() + timedelta(days=3)):
        """

        @param args:
        @param from_date:
        @param to_date:
        """
        if args:
            from_date = args.get('from_date', datetime.now() + timedelta(days=1))
            to_date = args.get('to_date', datetime.now() + timedelta(days=3))
        else:
            from_date = datetime.now() + timedelta(days=1)
            to_date = datetime.now() + timedelta(days=3)

        self.from_date = from_date
        self.to_date = to_date

    def create_hotel(self, spider_name, name, href, location_obj, star_rating, users_rating, currency, lowest_price,
                     address, area):
        """

        @param spider_name:
        @param name:
        @param href:
        @param location_obj:
        @param star_rating:
        @param users_rating:
        @param currency:
        @param lowest_price:
        @param address:
        @param area:
        """
        log.msg("len name ...." + str(len(name)), level=log.INFO)
        print star_rating
        for pos in range(0, len(name)):
            log.msg("name ...." + str(pos), level=log.INFO)
            obj, created = Hotel_Domain.objects.get_or_create(name=spider_name, priority=1)
            Hotel.objects.get_or_create(hotel_domain=obj,
                                        src=href[pos],
                                        name=name[pos],
                                        location=location_obj,
                                        currency=currency[pos],
                                        lowest_price=lowest_price[pos],
                                        user_rating=float(users_rating[pos]),
                                        address=address[pos],
                                        area=area[pos],
                                        defaults={'star_rating': star_rating[pos]})

    def create_location(self, location):
        """

        @param location:
        @return:
        """
        object, create = Location.objects.get_or_create(name=location)
        return object