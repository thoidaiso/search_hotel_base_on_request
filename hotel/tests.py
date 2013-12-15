from django.test import TestCase
from hotel.models import Users_Request, Hotel, Hotel_Domain, Room, Image_Hotel
import datetime
from django.utils import timezone
# Create your tests here.

def create_user_request(location, price_from, price_to, currency, star_rating, create_time):
    return Users_Request.objects.create(location=location,
            create_time=create_time, price_from =price_from, price_to=price_to, currency=currency, star_rating=star_rating)

def create_hotel_domain(name, priority):
    return Hotel_Domain.objects.create(name=name, priority=priority)

class Users_RequestTest(TestCase):
    
    def basic_create(self):
        """
        Creates a user request with basic info
        """
        Users_Request.objects.create(location="Ho Chi Minh",
            create_time=datetime.datetime.now())
#        self.assertEqual(Users_Request.object.filter, "Ho Chi Minh")
        
    def extra_create(self):
        """
        Creates a user request with extra info
        """
        request= create_user_request("Ho Chi Minh", 21,132.5,'USD', 4,datetime.datetime.now())
#        self.assertEqual(request.location, "Ho Chi Minh")
        
class Hotel_DomainTest(TestCase):
    def create(self):
        """
        Create a hotel domain
        """
        domain= create_hotel_domain("agoda.com",1)
#        self.assertEqual(request.location, "agoda.com")
    
#class HotelTest(TestCase):
#    def basic_create(self):
#        """
#        Create basic hotel
#        """
#        
    
    
    
        