from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'^$', views.show),
    url(r'^(?P<k>\d+)$', views.show),
 	url(r'^get_info/(?P<k>\d+)$', views.get_info),
]
