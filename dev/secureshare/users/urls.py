from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from .views import register, profile, change_password, create_group, join_group

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^change_password/$', change_password, name='change-password'),
    url(r'^create_group/$', create_group, name='create_group'),
    url(r'^join_group/$', join_group, name='join_group')

]
