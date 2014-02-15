from django.contrib import admin
from hotel.models import  Hotel_Domain, Hotel, Room, Image_Hotel
# Register your models here.


#admin.StackedInline
class HotelInline(admin.TabularInline):
    model = Hotel
    extra = 5
    
#admin.StackedInline
class RoomInline(admin.TabularInline):
    model = Room
    extra = 5

#admin.StackedInline
class ImageInline(admin.TabularInline):
    model = Image_Hotel
    extra = 5
#class Users_Request_Admin(admin.ModelAdmin):
#    #    Design form
#    fieldsets  = [
#                  (None, {'fields': ['location']}),
#                  ('Other Info', {'fields': ['price_from', 'price_to', 'currency', 'star_rating', 'create_time'], 'classes': ['collapse'] } )
#                  ]
#    
#    #    Design many2one
#    inlines = [HotelInline]
#    
#    #    Design form
#    list_display = ['location', 'price_from', 'price_to', 'currency', 'star_rating', 'create_time']
#    
#    #    add filter
#    list_filter = ['create_time']
#    
#admin.site.register(Users_Request, Users_Request_Admin)

class Hotel_Domain_Admin(admin.ModelAdmin):
     #    Design form
    list_display = ['name', 'priority']
    
     #    Design many2one
    inlines = [HotelInline]

admin.site.register(Hotel_Domain, Hotel_Domain_Admin)


class Hotel_Admin(admin.ModelAdmin):
        #    Design form
    fieldsets  = [
                  (None, {'fields': ['name', 'order_in_page', 'src',  'hotel_domain']}),
                  ('Price', {'fields': ['lowest_price','currency'], 'classes': ['collapse'] } ),
                  ('Location', {'fields': ['location']}),
                  ('Rating', {'fields': ['star_rating', 'user_rating'], 'classes': ['collapse']}),
                  ('Description', {'fields': ['description'], 'classes': ['collapse']}),
                  ('Service', {'fields': ['service'], 'classes': ['collapse']}),
                  
                  ]
    
    #    Design form
    list_display = ['name', 'lowest_price', 'currency', 'star_rating', 'user_rating', 'description', 'src']
    
    #    add filter
    list_filter = ['star_rating', 'location']
    
    #    Design many2one
    inlines = [RoomInline, ImageInline]
    
admin.site.register(Hotel, Hotel_Admin)

class Room_Admin(admin.ModelAdmin):
        #    Design form
    fieldsets  = [
                  (None, {'fields': ['name', 'hotel']}),
                  ('Price', {'fields': ['price','currency'], 'classes': ['collapse'] } ),
                  ('People', {'fields': ['number_of_people']}),
                  ('Description', {'fields': ['room_info'], 'classes': ['collapse']}),
                  
                  ]
    
    #    Design form
    list_display = ['name', 'hotel', 'price', 'currency', 'number_of_people', 'room_info']
    
    #    add filter
    list_filter = ['hotel', 'number_of_people']
    
    #    Design many2one
    inlines = [ImageInline]
    
admin.site.register(Room, Room_Admin)

class Image_Hotel_Admin(admin.ModelAdmin):
    #    Design form
    list_display = [ 'hotel', 'room', 'src']
    
    #    add filter
    list_filter = ['hotel', 'room']

admin.site.register(Image_Hotel, Image_Hotel_Admin)
    
    