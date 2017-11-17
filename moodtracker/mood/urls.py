from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Front-end views
    url(r'^$', views.index, name='index'),
    url(r'profile/^$', views.profile, name='profile'),
    url(r'mood_history/^$', views.mood_history, name='mood_history'),

    # Auth views
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url('^password_change/$', auth_views.password_change, name='password_change'),
    url('^password_change/done/$', auth_views.password_change_done, name='password_change_done'),
    url('^password_reset/$', auth_views.password_reset, name='password_reset'),
    url('^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url('^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url('^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    # APIs
    url(r'^incoming_sms/$', views.incoming_sms, name='incoming_sms'),
]
