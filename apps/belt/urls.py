from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^main$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^travels$', views.travels, name='travels'),
    url(r'^travels/destination/(?P<id>\d+)$', views.travelinfo, name='travelinfo'),
    url(r'^travels/join/(?P<id>\d+)$', views.jointrip, name='jointrip'),
    # # url(r'^dashboard/remove/(?P<id>\d+)$', views.removefromlist, name='removefromlist'),
    # # url(r'^dashboard/destroy/(?P<id>\d+)$', views.destroy, name='destroy'),
    url(r'^travels/add$', views.addtrip, name='addtrip'),
    url(r'^travels/createtrip$', views.createtrip, name='createtrip'),
    url(r'^logout$', views.logout, name='logout')
]