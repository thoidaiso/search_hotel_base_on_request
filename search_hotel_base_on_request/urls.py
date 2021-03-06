from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()
from hotel import views

urlpatterns = patterns('',
                       url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       url(r'^search/$', views.ResultView.as_view(), name='result'),
                       url(r'^get_result/$', views.get_result, name='get_result'),
                       url(r'^get_filter_result/', views.get_filter_result, name='get_filter_result'),
                       url(r'^get_result/(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
                       url(r'^get_result/statistic/$', views.statistic, name='statistic'),
                       url(r'^search.json/$', views.autocompleteLocation, name='autocompleteLocation'),
                       url(r'^get_result/help/$', views.get_help, name='help'),
                       url(r'^help/$', views.get_help, name='help'),
)
