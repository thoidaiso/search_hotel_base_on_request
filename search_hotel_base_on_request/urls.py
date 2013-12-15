from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'search_hotel_base_on_request.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
#    url(r'^s', include('hotel.urls', namespace="hotel")),
    url(r'^admin/', include(admin.site.urls)),
)
