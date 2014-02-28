from datetime import datetime

from hotel.models import Price_Book, Image_Hotel
from django import template


register = template.Library()


@register.filter
def get_room_price(room_obj, from_date):
    from_date = datetime.strptime(from_date, "%d-%m-%Y").date()

    #    get price from price_book where date_start <= from_date <= date_end
    price_books = Price_Book.objects.filter(room=room_obj).filter(date_start__lt=from_date, date_end__gt=from_date)

    #    room.price_set.all.filter(date_start>= from_date, date_end <= from_date)
    #    If dont have info about from_date, get the latest price_book
    if not price_books:
        price_books = Price_Book.objects.filter(room=room_obj).order_by('-date_start')

    return price_books[0].price


@register.filter
def get_hotel_lowest_price(hotel_obj, from_date):
    from_date = datetime.strptime(from_date, "%d-%m-%Y").date()

    price_books = Price_Book.objects.filter(hotel=hotel_obj).filter(date_start__lt=from_date,
                                                                    date_end__gt=from_date).order_by('price')
    if not price_books:
        price_books = Price_Book.objects.filter(hotel=hotel_obj).order_by('-date_start').order_by('price')

    if not price_books:
        return hotel_obj.lowest_price
    return price_books[0].price

@register.filter
def get_hotel_user_rating(hotel_obj, user_rating):
    if user_rating >0:
        return user_rating
    return 'N/A'

@register.filter
def separate_hotel_service(service):
    service_arr = service.split('\r\n')
    service_arr = [x for x in service_arr if x]
    return service_arr


@register.filter
def get_hotel_main_image(hotel_obj):
    image = Image_Hotel.objects.filter(hotel=hotel_obj, main=True)
    if not image:
        images = Image_Hotel.objects.filter(hotel=hotel_obj)
        if images:
            for image in images:
                if 'icon_wifi' not in image.src:
                    return image.src
        else:
            return ''

    return image[0].src


@register.filter
def get_book_link(hotel_obj):
    if 'http' in hotel_obj.src:
        return hotel_obj.src
    return "http://agoda.com" + hotel_obj.src
