from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^incoming_sms/$', views.incoming_sms, name='incoming_sms'),
]
