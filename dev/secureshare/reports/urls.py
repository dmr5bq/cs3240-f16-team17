from django.conf.urls import include, url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^success/$', views.success, name='success'),
    url(r'^register/$', views.register_report, name='register_report'),

    url(r'^report/(?P<pk>[0-9]+)/$', views.ReportDetailView.as_view(), name='view_report'),
    url(r'^report/(?P<report_id>[0-9]+)/delete/$', views.delete_report, name='delete_report'),

    url(r'^all_reports/$', views.AllReportListView.as_view(), name='all_reports'),
]

