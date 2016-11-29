from django.conf.urls import include, url

from . import views


urlpatterns = [
    url(r'^register/(?P<folder_id>[0-9]+)/$', views.register_report, name='register_report'),

    url(r'^file/download/(?P<file_id>[0-9]+)/$', views.download_file, name='download_file'),
    url(r'^file/delete/(?P<file_id>[0-9]+)/$', views.delete_file, name='delete_file'),
    url(r'^file/all_documents/$', views.all_documents, name='all_documents'),

    url(r'^report/(?P<pk>[0-9]+)/$', views.ReportDetailView.as_view(), name='view_report'),
    url(r'^report/(?P<report_id>[0-9]+)/edit/$', views.edit_report, name='edit_report'),
    url(r'^report/(?P<report_id>[0-9]+)/delete/$', views.delete_report, name='delete_report'),
    url(r'^report/(?P<report_id>[0-9]+)/download/$', views.download_report, name='download_report'),
    url(r'^report/(?P<report_id>[0-9]+)/upload_file/$', views.upload_file_to_report, name='upload_file_to_report'),
    url(r'^report/(?P<report_id>[0-9]+)/favorite/$', views.favorite_report, name='favorite_report'),

    url(r'^folder/(?P<folder_id>[0-9]+)/$', views.view_folder, name='view_folder'),
    url(r'^folder/(?P<folder_id>[0-9]+)/new/$', views.new_folder, name='new_folder'),
    url(r'^folder/(?P<folder_id>[0-9]+)/delete/$', views.delete_folder, name='delete_folder'),

    url(r'^all_reports/$', views.all_reports, name='all_reports'),
    url(r'^all_reports/detail/$', views.all_reports, name='all_reports_detail'),
    url(r'^my_reports/$', views.MyReportListView.as_view(), name='my_reports'),
    url(r'^favorites/$', views.view_favorites, name='view_favorites'),
]

