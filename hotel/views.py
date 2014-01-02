from django.http import HttpResponse, HttpResponseRedirect
#from polls.models import Poll, Choice
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone


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


def get_result(request):
    search_name = request.POST['search_name']
    check_in = request.POST['check_in']
    check_out = request.POST['check_out']
    room_count = request.POST['room_count']
    guest_count = request.POST['guest_count']
    vals = {"search_name": search_name,
            "check_in": check_in,
            "check_out": check_out,
            "room_count": room_count,
            'guest_count': guest_count,
             }
    print "\n vals==",vals
    
#    p = get_object_or_404(Poll, pk=poll_id)
#    try:
#        selected_choice = p.choice_set.get(pk=request.POST['choice'])
#    except(KeyError, Choice.DoesNotExist):
#    return render(request, 'hotel/result.html', {
#                    'poll':p, 'error_message':"You didn't select a choice."})
#    else:
#        print "\n\nprepare vote===",selected_choice
#        selected_choice.votes +=1
#        print "\nafter vote"
#        selected_choice.save()
#        print "\n\save",p
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return render(request, 'hotel/result.html')#, {
#                    'poll':p, 'error_message':"You didn't select a choice."})
    return HttpResponseRedirect(reverse('results'))



