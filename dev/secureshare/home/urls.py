from django.conf.urls import include, url

from .views import HomeView

urlpatterns = [
    url(r'^$', HomeView, name='home'),
]
