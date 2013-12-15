from django.db import models

# Create your models here.

rating = (
           (1,1),
           (2,2),
           (3,3),
           (4,4),
           (5,5),
           )

#Save request from users
class Users_Request(models.Model):
    location = models.CharField(max_length=200)
    price_from = models.FloatField(null=True, blank=True)
    price_to  = models.FloatField(null=True, blank=True)
    star_rating = models.SmallIntegerField(max_length=1, choices=rating, null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    currency = models.CharField(max_length=4, null=True, blank=True)

#Save domain to search hotel and their priority compare with other domain
class Hotel_Domain(models.Model):
    name = models.CharField(max_length=100)
    priority = models.SmallIntegerField()
    def __unicode__(self):
        return self.name

#Save info about hotel
class Hotel(models.Model):
    
    user_request = models.ForeignKey(Users_Request, null=True, blank=True)
    hotel_domain = models.ForeignKey(Hotel_Domain, null=True, blank=True)
    order_in_page = models.SmallIntegerField(null=True, blank=True)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
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
    price = models.FloatField()
    room_info = models.TextField()
    number_of_people  = models.SmallIntegerField(null=True, blank=True)
    promotion = models.FloatField(null=True, blank=True)
    currency = models.CharField(max_length=4)
    def __unicode__(self):
        return self.name

class Image_Hotel(models.Model):
    hotel = models.ForeignKey(Hotel, null=True, blank=True)
    room = models.ForeignKey(Room, null=True, blank=True)
    src = models.URLField(max_length=200)
    
    
    
    
    
    
    
    
    
    