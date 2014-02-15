from hotel.models import Price_Book, Hotel
from datetime import datetime
from django import template
register = template.Library()

@register.filter
def get_room_price(room_obj, from_date):
    from_date = datetime.strptime(from_date, "%d-%m-%Y").date()
    
#    get price from price_book where date_start <= from_date <= date_end
    price_books = Price_Book.objects.filter(room=room_obj).filter(date_start__lt=from_date,date_end__gt=from_date)
    
#    room.price_set.all.filter(date_start>= from_date, date_end <= from_date)
#    If dont have info about from_date, get the latest price_book
    if not price_books:
        print "1111"
        price_books = Price_Book.objects.filter(room=room_obj).order_by('-date_start')
   
    print "\price = ",price_books[0].price
    return price_books[0].price

@register.filter
def get_hotel_lowest_price(hotel_obj, from_date):
    from_date = datetime.strptime(from_date, "%d-%m-%Y").date()
    
    price_books = Price_Book.objects.filter(hotel=hotel_obj).filter(date_start__lt=from_date,date_end__gt=from_date).order_by('price')
    print "\n\n"
    if not price_books:
        print "get again",hotel_obj.id
        price_books = Price_Book.objects.filter(hotel=hotel_obj).order_by('-date_start').order_by('price')
    
    print "price_books",price_books
    return price_books[0].price



