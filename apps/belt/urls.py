from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^main$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^quotes$', views.quotes, name='quotes'),
    url(r'^users/(?P<id>\d+)$', views.userinfo, name='userinfo'),
    url(r'^addtolist/(?P<id>\d+)$', views.addtolist, name='addtolist'),
    url(r'^removefromlist/(?P<id>\d+)$', views.removefromlist, name='removefromlist'),
    url(r'^quotes/addquote$', views.addquote, name='addquote'),
    url(r'^logout$', views.logout, name='logout')
]