from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from hotel.models import  Hotel, Location
from multiprocessing.queues import Queue
from scraper.scraper.spiders.hotel_spider import HotelSpider
from ConnectorToScrapy import ConnectorToScrapy
from datetime import datetime
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
#        return Poll.objects.filter(
#            pub_date__lte=timezone.now()
#        ).order_by('-pub_date')[:5]
#        return Poll.objects.order_by('-pub_date')[:5]

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
        print "\n\n get====",args
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        print "\n\n posst----"
        return render(request, self.template_name)

class DetailView(generic.DetailView):
    template_name = 'hotel/detail.html'
    model = Hotel
    
    
#get search data from index page
def get_result(request):
    print "\n request Post==",request.POST
    now = timezone.now()
    location = request.GET.get('search_name')
#    location = re.sub('[-., ]+', '', location)
    #TODO:
#        Get real location like hochiminh if input 'ho chi minh city'
    
    check_in    = request.GET.get('check_in') 
    check_in    = check_in and datetime.strptime(check_in, "%d-%m-%Y")
    
    check_out   = request.GET.get('check_out')
    check_out   = check_out and  datetime.strptime(check_out, "%d-%m-%Y")
    
    room_count  = request.GET.get('room_count') or 0
    guest_count = request.GET.get('guest_count') or 0
    
    vals = {"location": location,
            "check_in": check_in and check_in.date(),
            "check_out": check_out and check_out.date(),
            "room_count": int( room_count),
            'guest_count': int( guest_count),
            'create_time': now,
             }
    print "\n vals==",vals
    
    
    
#    Rule to input at index page
#        must input location and check_in date
#        check_in date must greater or equal now 
#        check_out date must greater than check_in date
    if not location  or not check_in or now.date() > check_in.date() or (check_out and check_out <= check_in):
        return HttpResponseRedirect(reverse('index', args=()))
    
    hotel_data = [] 
    
    if Location.objects.filter(name = location).exists():
        location_obj = Location.objects.filter(name = location)[0]
        print "\n location==",location_obj.name
#        for hotel in Hotel.objects.filter(location = location_obj):
#            hotel_data.append(hotel)
        hotel_data = Hotel.objects.filter(location = location_obj)
        
    else:
        print "\n\n\n Show page to choose correct location"
        #TODO: Need to show page to choose correct location
        
        call_spider(HotelSpider, location, check_in, check_out)
    
#    TODO: Remove this block
#    Get user_request id
#    created = True
#    try:
#        object = Users_Request.objects.get(location = location)
#        print "\n exist location"
#    except Users_Request.DoesNotExist:
#        print "\n create new user request"
#        return_dict = create_user_request(vals)
#        if return_dict.get('object', False) and return_dict.get('created', False):
#            object = return_dict['object']
#            created = False
#    
#    print "\n object id==",object.id,';location', location
#    END_TODO:     
    
#    try to call spider
#    if show_location_page:
#        call_spider(HotelSpider, location, check_in, check_out)
    
    
    #    FILTER OR SORT RESULT HOTELS
    filter = False
    sort_type = request.POST.get('sort_type')
    if sort_type:
        filter = True
        hotel_data = hotel_data.order_by(sort_type)
    else:
        hotel_data = hotel_data.order_by('-user_rating')
        
        
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
    if page_number or filter:
        print "\n return grid hotels detail"
        return render(request, 'hotel/hotel_grid_detail.html', {'data': hotels, 'count_hotel': count_hotel})
        
    
    return render(request, 'hotel/result.html', {'vals': vals, 'hotel_data': hotels, 'count_hotel': count_hotel})
#    return HttpResponseRedirect(reverse('result', args=(vals)))
    
def get_filter_result(request):
    print "\n== get_result_with_extra_info"
    return HttpResponseRedirect(reverse('index', args=()))

#def create_user_request(vals):
#    var_dict = {}
#    if vals.get('check_out', False):
#        var_dict = { 'date_end': vals['check_out'] }
#    object, created = Users_Request.objects.get_or_create(location = vals.get('location',''),
#                                        create_time = vals.get('create_time', False) ,
#                                        date_start  = vals.get('check_in', False) , 
#                                        room_count  = vals.get('room_count', 0),
#                                        guess_count = vals.get('guess_count', 0),
#                                        defaults    = var_dict
#                                        )
#    return {'object': object, 'created': created}
    

def call_spider(Spider, location, check_in, check_out):
    print "\n try to call spider"
    dict = {'spider': Spider, 'args': {'location': location, 'from_date': check_in } }
    if check_out:
        dict.update({'to_date': check_out})
    try:
        conector = ConnectorToScrapy()
        conector.run_spider(dict)
        conector.stop_reactor()
    except ValueError:
        print "\n Error when call spider---",ValueError
        pass
    print "\n end call spider"
        

