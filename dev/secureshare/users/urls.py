from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from .views import register

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^register/$', register, name='register'),
    # url(r'^profile/$', ProfileView.as_view(), name='profile'),
]
