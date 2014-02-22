# -*- coding: utf-8 -*-
__author__ = 'chanhle'
from datetime import datetime, timedelta

from scrapy.spider import BaseSpider
from scrapy import log
from hotel.models import Hotel, Hotel_Domain, Location, Room, Price_Book, Image_Hotel
import re


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

    def create_image(self, hotel_name, image, main=False):
        if image and hotel_name:
            hotel_obj = Hotel.objects.filter(name=hotel_name)[0]
            Image_Hotel.objects.get_or_create(hotel=hotel_obj,
                                              src=image,
                                              main=main
                                              )

    def get_hotel_service(self, service_data):
        dict = {'wi': False,
                'airport': False,
                'bar': False,
                'business': False,
                'restaurant': False,
                'spa': False,
                'sauna': False,
                'park': False,
                'fitness': False,
                'smok': False,
                'baby': False
        }

        name_dict = {'wi': 'Internet',
                     'airport': 'Airport Transfer',
                     'bar': 'Bar',
                     'business': 'Business Center',
                     'restaurant': 'Restaurant',
                     'spa': 'Spa',
                     'sauna': 'Spa',
                     'park': "Parking",
                     'fitness': 'Fitness Center',
                     'smok': 'Smoke Area',
                     'baby': 'Babysitting'
        }
        service = ""

        for data in service_data:
            for key in dict.keys():
                if key in data.lower():
                    dict[key] = True

        for key in dict.keys():
            if dict[key]:
                service += "\r\n" + name_dict[key]

        return service


    def create_room(self, spider_name, hotel_name, room_name, number_of_people, price):
        log.msg("create room for" + hotel_name, level=log.INFO)
        hotel_domain_obj, created = Hotel_Domain.objects.get_or_create(name=spider_name, priority=1)
        hotel_obj = Hotel.objects.filter(name=hotel_name)[0]
        #        log.msg("hotel_obj room"+str(hotel_obj.name), level=log.INFO)
        for pos in range(0, len(room_name)):
            room_obj, created = Room.objects.get_or_create(hotel=hotel_obj,
                                                           name=room_name[pos],
                                                           number_of_people=number_of_people[pos])
            if not price:
                price = 0
            log.msg("price:" + (price and pos <= len(price) and price[pos] or ''), level=log.INFO)
            self.create_price_book_period(hotel_obj, room_obj, price and price[pos] or 0)


    def create_price_book_period(self, hotel_obj, room_obj, price):
        hotel_domain_obj, created = Hotel_Domain.objects.get_or_create(name='agoda.com', priority=1)
        obj, created = Price_Book.objects.get_or_create(hotel=hotel_obj,
                                                        room=room_obj,
                                                        hotel_domain=hotel_domain_obj,
                                                        date_start=self.from_date,
                                                        date_end=self.to_date,
                                                        defaults={'price': float(price)}
                                                        )
        if not created and obj.price > float(price):
            Price_Book.objects.filter(pk=obj.id).update(price=float(price))

    def create_hotel(self, spider_name, name, href, location_obj, star_rating, users_rating, currency, lowest_price,
                     address, area, priority):
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
        if len(name) == len(href) == len(address) == len(area) == len(currency) == len(star_rating) == len(
                users_rating) == len(lowest_price):
            for pos in range(0, len(name)):
                log.msg("name ...." + name[pos], level=log.INFO)
                obj, created = Hotel_Domain.objects.get_or_create(name=spider_name, priority=priority)
                obj, created = Hotel.objects.get_or_create(hotel_domain=obj,
                                                           src=href[pos],
                                                           name=name[pos].strip(),
                                                           location=location_obj,
                                                           address=address[pos],
                                                           area=area[pos],
                                                           defaults={'star_rating': int(float(star_rating[pos])),
                                                                     'user_rating': float(users_rating[pos]),
                                                                     'lowest_price': lowest_price[pos],
                                                                     'currency': currency[pos],
                                                           })

    def update_hotel(self, hotel_name, description, service):
        """

        @param hotel_name:
        @param description:
        @param service:
        """
        if description and service:
            log.msg("hotel_name for hotel " + hotel_name)
            hotel_obj = Hotel.objects.filter(name=hotel_name)[0]
            if hotel_obj:
                if (hotel_obj.description and len(description) > len(
                        hotel_obj.description)) or not hotel_obj.description:
                    Hotel.objects.filter(pk=hotel_obj.id).update(description=description)

                Hotel.objects.filter(pk=hotel_obj.id).update(service=service)

    def create_location(self, location):
        """

        @param location:
        @return:
        """
        short_name = re.sub(' ', '', location)
        location_object = Location.objects.filter(name__icontains=location)
        if not location_object:
            object, create = Location.objects.get_or_create(name=location,
                                                            short_name=short_name)
            return object
        else:
            return location_object[0]
       


