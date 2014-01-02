from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from hotel import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'search_hotel_base_on_request.views.home', name='home'),
#    url(r'^s', include('hotel.urls', namespace="hotel")),
    url(r'^admin/', include(admin.site.urls)),
#    url(r'^hotel/', include('hotel.urls', namespace="hotel")),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^search/', views.ResultView.as_view(), name='result'),
    url(r'^get_result/', views.get_result, name='get_result'),
)
