from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from .views import RegistrationView

urlpatterns = [
	url(r'^login/$', auth_views.login, {'template_name':'users/login.html', 'next_page':'home:home'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page':'login'}, name='logout'),
    url(r'^register/$', RegistrationView.as_view(), name='register'),
]