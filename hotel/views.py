from django.http import HttpResponse, HttpResponseRedirect
#from polls.models import Poll, Choice
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from hotel.models import Users_Request_Form, Hotel
from multiprocessing.queues import Queue
from scraper.scraper.spiders.hotel_spider import HotelSpider
from ConnectorToScrapy import ConnectorToScrapy

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
    vals = {"search_name": request.POST['search_name'],
            "check_in": request.POST['check_in'],
            "check_out": request.POST['check_out'],
            "room_count": request.POST['room_count'],
            'guest_count': request.POST['guest_count'],
             }
    print "\n vals==",vals
#    if request.method == 'POST': 
#         print "\n method POST=="
#         form = Users_Request_Form(request.POST) 
#         print "\n form ==",form
#         if form.is_valid(): 
             
    search_name = vals['search_name']
    if not search_name:
        return HttpResponseRedirect(reverse('index', args=()))
    
    #########
    ###get hotel data in here for first request
    hotel_data = []
    for i in range(0,6):
        hotel = {'name': 'Amancando',
                 'location': '123, Le dinh chinh, quan 3',
                 'lowest_price': 123,
                 'currency': '$',
                 'user_rating': '7.6',
                 'id': '1',
                 'star_rating': '3',
                 }
        
        hotel_data.append(hotel)
    
#    try to call spider
    print "\n try to call spider"
    dict = {'spider': HotelSpider, 'args': [] }
    conector = ConnectorToScrapy()
    conector.run_spider(dict)
    print "\n end call spider"
    
    return render(request, 'hotel/result.html', {'vals': vals, 'hotel_data': hotel_data})
#    return HttpResponseRedirect(reverse('result', args=(vals)))
    
def get_filter_result(request):
    print "\n== get_result_with_extra_info"
    return HttpResponseRedirect(reverse('index', args=()))


        
        

