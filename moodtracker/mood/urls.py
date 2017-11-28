from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Front-end views
    url(r'^$', views.index, name='index'),
    url(r'^profile/(?P<username>[0-9A-Z-a-z]+)/$', views.profile, name='profile'),
    url(r'^settings/(?P<username>[0-9A-Z-a-z]+)/$', views.settings, name='settings'),
    url(r'^mood/(?P<username>[0-9A-Z-a-z]+)/$', views.mood, name='mood'),

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
    url(r'^get_user_data/$', views.get_user_data, name='get_user_data'),
    url(r'^get_user_profile/$', views.get_user_profile, name='get_user_profile'),
    url(r'^update_user_profile/$', views.update_user_profile, name='update_user_profile'),
]