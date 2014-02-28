from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from hotel.models import Hotel, Location
#from ConnectorToScrapy import ConnectorToScrapy
from django.utils import timezone
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class IndexView(generic.ListView):
    template_name = 'hotel/index.html'
    #    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """
        Return the last five published polls (not including those set to be
        published in the future).
        """
        return


class ResultView(generic.ListView):
    template_name = 'hotel/result.html'
    #    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """
        Return the last five published polls (not including those set to be
        published in the future).
        """
        return

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)


class DetailView(generic.DetailView):
    template_name = 'hotel/detail.html'
    model = Hotel


#get search data from index page
def get_result(request):
    Hotel.objects.filter(name='New World Saigon Hotel').update(description='description')
    now = timezone.now()
    location = request.GET.get('search_name')
    #    if location:
    #        request.session['filter'] = {}
    #    location = re.sub('[-., ]+', '', location)
    #TODO:
    #        Get real location like hochiminh if input 'ho chi minh city'

    check_in = request.GET.get('check_in')
    check_in = check_in and datetime.strptime(check_in, "%d-%m-%Y")

    check_out = request.GET.get('check_out')
    check_out = check_out and datetime.strptime(check_out, "%d-%m-%Y")

    room_count = request.GET.get('room_count') or 0
    guest_count = request.GET.get('guest_count') or 0

    vals = {"location": location,
            "check_in": request.GET.get('check_in'),
            "check_out": request.GET.get('check_out'),
            "room_count": int(room_count),
            'guest_count': int(guest_count),
            'create_time': now,
            'search_hotelname': request.GET.get('search_hotelname') or '',
            'search_star_rating_5': request.GET.get('search_star_rating_5'),
            'search_star_rating_4': request.GET.get('search_star_rating_4'),
            'search_star_rating_3': request.GET.get('search_star_rating_3'),
            'search_star_rating_2': request.GET.get('search_star_rating_2'),
            'search_star_rating_1': request.GET.get('search_star_rating_1'),

            'search_facility_internet': request.GET.get('search_facility_internet'),
            'search_facility_air_trans': request.GET.get('search_facility_air_trans'),
            'search_facility_bar': request.GET.get('search_facility_bar'),
            'search_facility_business': request.GET.get('search_facility_business'),
            'search_facility_restaurant': request.GET.get('search_facility_restaurant'),
            'search_facility_spa': request.GET.get('search_facility_spa'),
            'search_facility_car_park': request.GET.get('search_facility_car_park'),
            'search_facility_gym': request.GET.get('search_facility_gym'),
            'search_facility_smoke_area': request.GET.get('search_facility_smoke_area'),
            'search_facility_child': request.GET.get('search_facility_child'),
    }
    #    Rule to input at index page
    #        must input location and check_in date
    #        check_in date must greater or equal now
    #        check_out date must greater than check_in date
    if not location or not check_in or now.date() > check_in.date() or (check_out and check_out <= check_in):
        return HttpResponseRedirect(reverse('index', args=()))

    hotel_data = []

    if Location.objects.filter(name=location).exists():
        location_obj = Location.objects.filter(name=location)[0]
        #        for hotel in Hotel.objects.filter(location = location_obj):
        #            hotel_data.append(hotel)
        hotel_data = Hotel.objects.filter(location=location_obj)

    else:
        #################TRY
#        from celery_app.tasks import crawl_spider
#        args = {'from_date': check_in}
#        crawl_spider(0,args)
#    
        ###############ENDTRY
#        from django.db import connection
#        connection.close()
        
        location = re.sub('[-.,_/\| ]+', '', location)
        location = location.lower()
        location = location.replace('city', '')
        location_obj = Location.objects.filter(short_name__icontains=location)
        if not location_obj:
            location_obj = Location.objects.all()
        return render(request, 'hotel/location_list.html',
                      {'locations': location_obj, 'name': request.GET.get('search_name')})

        #TODO: Need to show page to choose correct location
    #   SORT RESULT HOTELS
    sort_result = False
    sort_type = request.POST.get('sort_type')
    if sort_type:
        sort_result = True
        hotel_data = hotel_data.order_by(sort_type)
    else:
        hotel_data = hotel_data.order_by('-user_rating')

    # FILTER RESULT PAGE
    hotel_data = filter_result_page(request, hotel_data)

    #FILTER TO GET BEST HOTEL INFO IF HAVE 2 RECORD FOR SAME HOTEL BY 2 DOMAIN
    hotel_data = filter_duplicate_hotel(hotel_data, check_in)

    ####Pagination
    count_hotel = len(hotel_data)
    page_number = request.POST.get('page')
    page_number = page_number and int(page_number)
    paginator = Paginator(hotel_data, 20) # Show 20 hotels per page

    try:
        hotels = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        hotels = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        hotels = paginator.page(paginator.num_pages)



    #    render grid hotel result, if change page
    if page_number or sort_result:
        print "\n return grid hotels detail"
        return render(request, 'hotel/hotel_grid_detail.html', {'data': hotels, 'count_hotel': count_hotel, 'location': location_obj, 'date_start':request.GET.get('check_in') })
        
    
    return render(request, 'hotel/result.html', {'vals': vals, 'hotel_data': hotels, 'count_hotel': count_hotel, 'location': location_obj})
#    return HttpResponseRedirect(reverse('result', args=(vals)))

def get_filter_result(request):
    return HttpResponseRedirect(reverse('index', args=()))


def call_spider(Spider, location, check_in, check_out):
    dict = {'spider': Spider, 'args': {'location': location, 'from_date': check_in}}
    if check_out:
        dict.update({'to_date': check_out})
    try:
        conector = ConnectorToScrapy()
        conector.run_spider(dict)
        conector.stop_reactor()
    except ValueError:
        pass


#FILTER TO GET BEST HOTEL INFO IF HAVE 2 RECORD FOR SAME HOTEL BY 2 DOMAIN
#AT THE MOMENT ONLY CHOOSE HOTEL WHICH HAVE LOWER PRICE THAN
def filter_duplicate_hotel(hotel_data, check_in):
    print "\n filter duplicate hotel======="
    remove_index_hotel_data = []
    for i in range(0, len(hotel_data)-1):
        for j in range(i+1, len(hotel_data)):
            if hotel_data[i].name ==hotel_data[j].name and hotel_data[i].location == hotel_data[j].location and two_hotel_address_is_nearly_similar(hotel_data[i].address, hotel_data[j].address):
                
                #Start to validate to choose best hotel
                if hotel_data[i].lowest_price > hotel_data[j].lowest_price:
                    remove_index_hotel_data.append(j)
                else:
                    remove_index_hotel_data.append(i)

    return_hotel_data = []
    if remove_index_hotel_data:
        for i in range(0, len(hotel_data)):
            if i not in remove_index_hotel_data:
                return_hotel_data.append(hotel_data[i])
    else:
        return_hotel_data = hotel_data
    return return_hotel_data

#Compare if two hotel address is nearly similar 
def two_hotel_address_is_nearly_similar(add1, add2):
    
    add1_arr = add1.split(',')
    add2_arr = add2.split(',')
    
    print "=a1",add1_arr
    print "=a2",add2_arr
    
    count = 0
    for add in add1_arr:
        if add in add2_arr:
            count += 1
    
    if count >= (len(add1_arr) + len(add2_arr) ) /4:
        return True
    return False
    

#FILTER RESULT PAGE BASE ON FILTER AND OLD FILTER IN SESSION
def filter_result_page(request, hotel_data):
    filter_sort = False

    if request.GET.get('search_hotelname'):
        hotel_data = filter_hotel('name', request.GET.get('search_hotelname'), hotel_data)

    star_rating = []
    if request.GET.get('search_star_rating_1'):
        star_rating.append(int(request.GET.get('search_star_rating_1')))

    if request.GET.get('search_star_rating_2'):
        star_rating.append(int(request.GET.get('search_star_rating_2')))

    if request.GET.get('search_star_rating_3'):
        star_rating.append(int(request.GET.get('search_star_rating_3')))

    if request.GET.get('search_star_rating_4'):
        star_rating.append(int(request.GET.get('search_star_rating_4')))

    if request.GET.get('search_star_rating_5'):
        star_rating.append(int(request.GET.get('search_star_rating_5')))

    if star_rating:
        hotel_data = filter_hotel('star_rating', star_rating, hotel_data)

    #Filter service
    if request.GET.get('search_facility_internet'):
        hotel_data = filter_hotel('service', request.GET.get('search_facility_internet'), hotel_data)

    if request.GET.get('search_facility_air_trans'):
        hotel_data = filter_hotel('service', request.GET.get('search_facility_air_trans'), hotel_data)

    if request.GET.get('search_facility_bar'):
        hotel_data = filter_hotel('service', request.GET.get('search_facility_bar'), hotel_data)

    if request.GET.get('search_facility_business'):
        hotel_data = filter_hotel('service', request.GET.get('search_facility_business'), hotel_data)

    if request.GET.get('search_facility_spa'):
        hotel_data = filter_hotel('service', request.GET.get('search_facility_spa'), hotel_data)

    if request.GET.get('search_facility_car_park'):
        hotel_data = filter_hotel('service', request.GET.get('search_facility_car_park'), hotel_data)

    if request.GET.get('search_facility_gym'):
        hotel_data = filter_hotel('service', request.GET.get('search_facility_gym'), hotel_data)

    if request.GET.get('search_facility_smoke_area'):
        hotel_data = filter_hotel('service', request.GET.get('search_facility_smoke_area'), hotel_data)

    if request.GET.get('search_facility_child'):
        hotel_data = filter_hotel('service', request.GET.get('search_facility_child'), hotel_data)

    return hotel_data


def filter_hotel(type_filter, filter_content, hotel_data):
    if type_filter and filter_content:

        if type_filter == 'name':
            hotel_data = hotel_data.filter(name__icontains=filter_content)

        elif type_filter == 'lowest_price':
            hotel_data = hotel_data.filter(lowest_price=filter_content)

        elif type_filter == 'star_rating':
            hotel_data = hotel_data.filter(star_rating__in=filter_content)

        elif type_filter == 'user_rating':
            hotel_data = hotel_data.filter(user_rating=filter_content)

        elif type_filter == 'area':
            hotel_data = hotel_data.filter(area=filter_content)

        elif type_filter == 'service':
            hotel_data = hotel_data.filter(service__icontains=filter_content)

    return hotel_data


from django.utils import simplejson
def autocompleteLocation(request):
    search_qs = Location.objects.filter(name__icontains=request.REQUEST['search'])
    results = []
    for r in search_qs:
        results.append(r.name)
    resp = request.REQUEST['callback'] + '(' + simplejson.dumps(results) + ');'
    print "\n autocomplete----",resp
    return HttpResponse(resp, content_type='application/json')

