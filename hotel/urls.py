from django.conf.urls import patterns, url
from hotel import views

urlpatterns = patterns('', 
#                   ex: /polls/
#                url(r'^$', views.index, name='index'),
##               ex: /polls/5/
#                url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
#                # ex: /polls/5/results/
#                url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
#                # ex: /polls/5/vote/
#                url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
                
#                url(r'^$', views.IndexView.as_view(), name='index'),
#                url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
#                url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
#                url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),

#                url(r'^$', views.IndexView.as_view(), name='index'),

#                url(r'^$', views.IndexView.as_view(), name='index'), 
#                url(r'^search/', views.ResultView.as_view(), name='result'),
#                url(r'^get_result/$', views.get_result, name='get_result'),
#                url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
                       )