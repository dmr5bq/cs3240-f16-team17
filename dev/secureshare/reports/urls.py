from django.conf.urls import include, url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^success/$', views.success, name='success'),
    url(r'^report/$', views.register_report, name='report'),

    url(r'^all_reports/$', views.AllReportListView.as_view(), name='all_reports'),
]

