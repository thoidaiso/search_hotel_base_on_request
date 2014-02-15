from django.db import models
from django.forms import ModelForm
from django import template
# Create your models here.

rating = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)

#Save request from users
#class Users_Request(models.Model):
#    session_id = models.CharField(max_length=200)#Session id of web browser
#    location = models.CharField(max_length=200)
#    price_from = models.FloatField(null=True, blank=True)
#    price_to = models.FloatField(null=True, blank=True)
#    star_rating = models.SmallIntegerField(max_length=1, choices=rating, null=True, blank=True)
#    create_time = models.DateTimeField(null=True, blank=True)
#    currency = models.CharField(max_length=4, null=True, blank=True)
#
#    date_start = models.DateField(null=True, blank=True)
#    date_end = models.DateField(null=True, blank=True)
#    room_count = models.SmallIntegerField(max_length=1, choices=rating, null=True, blank=True)
#    guess_count = models.SmallIntegerField(max_length=1, choices=rating, null=True, blank=True)
#    
#
#class Users_Request_Form(ModelForm):
#    class Meta:
#        model = Users_Request

class Location(models.Model):
    name = models.CharField(max_length=200) #full name of location
    short_name = models.CharField(max_length=100) #short name, use to check location of hotel ex: hochiminh, hanoi
    def __unicode__(self):
        return self.name
    
    
#Save domain to search hotel and their priority compare with other domain
class Hotel_Domain(models.Model):
    name = models.CharField(max_length=100)
    priority = models.SmallIntegerField()

    def __unicode__(self):
        return self.name

#Save info about hotel
class Hotel(models.Model):
#    user_request = models.ForeignKey(Users_Request, null=True, blank=True)
    hotel_domain = models.ForeignKey(Hotel_Domain, null=True, blank=True)
    order_in_page = models.SmallIntegerField(null=True, blank=True)
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, null=True, blank=True) #location of hotel like hochiminh---this field link to location
    address = models.CharField(max_length=200) #full address, number of house, street, city
    area = models.CharField(max_length=200) #like district 1- Ben thanh market
    type = models.CharField(max_length=100)
    star_rating = models.SmallIntegerField(max_length=1, choices=rating, null=True, blank=True)
    user_rating = models.FloatField(null=True, blank=True)
    lowest_price = models.SmallIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    src = models.URLField(max_length=200)
    service = models.TextField(blank=True)
    currency = models.CharField(max_length=4, null=True, blank=True)

    def __unicode__(self):
        return self.name


    
#Save info about room
class Room(models.Model):
    hotel = models.ForeignKey(Hotel)
    name = models.CharField(max_length=100)
    price = models.FloatField(null=True, blank=True)
    room_info = models.TextField(null=True, blank=True)
    number_of_people = models.CharField(max_length=100, null=True, blank=True)
#    promotion = models.FloatField(null=True, blank=True)
    currency = models.CharField(max_length=4)

    def __unicode__(self):
        return self.name
    

class Price_Book(models.Model):
    hotel = models.ForeignKey(Hotel, null=True, blank=True)
    room = models.ForeignKey(Room)
    hotel_domain = models.ForeignKey(Hotel_Domain, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)

class Image_Hotel(models.Model):
    hotel = models.ForeignKey(Hotel, null=True, blank=True)
    room = models.ForeignKey(Room, null=True, blank=True)
    src = models.URLField(max_length=200)
    

    
    
    
    
