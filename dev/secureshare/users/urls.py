from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'users:login'}, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^change_password/$', change_password, name='change-password'),



    url(r'^create_group/$', create_group, name='create_group'),
    url(r'^join_group/$', join_group, name='join_group'),
    url(r'^leave_group/$', leave_group, name='leave_group'),
    #url(r'^invite/$', invite_user, name='invite_user'),


    url(r'^all_users/$', all_users, name='all_users'),
    url(r'^all_groups/$', all_groups, name='all_groups'),
    url(r'^my_groups/$', my_groups, name='my_groups'),

    url(r'^user/(?P<user_id>[0-9]+)/$', view_user, name='user'),
    url(r'^group/(?P<group_id>[0-9]+)/$', view_group, name='group'),

    url(r'^group/(?P<group_id>[0-9]+)/leave/(?P<user_id>[0-9]+)/$', leave_group_by_id, name='leave_group_by_id'),

    url(r'^user/(?P<user_id>[0-9]+)/suspend/$', suspend_user, name='suspend_user'),
    url(r'^user/(?P<user_id>[0-9]+)/promote/$', promote_user, name='promote_user'),
    url(r'^user/(?P<user_id>[0-9]+)/(?P<group_id>[0-9]+)/remove_from_group/$', remove_user_from_group, name='remove_user_from_group'),
    url(r'^user/(?P<group_id>[0-9]+)/add_user_to_group/$', add_user_to_group, name='add_user_to_group'),

]

'''
url(r'^inbox/$', inbox, name='inbox'),
url(r'^outbox/$', outbox, name='outbox'),
url(r'^send_message/$', send_message, name='send_message'),
'''