from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash

from .forms import RegisterUserForm, ChangePasswordForm, CreateGroupForm, JoinGroupForm
from .models import *


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('users:login')
    else:
        form = RegisterUserForm()
    form_title = 'Create New User'
    form_back = '/users/login/'
    form_action = '/users/register/'
    return render(request, 'users/general_form.html', {'form': form, 'form_title':form_title, 'form_back':form_back, 'form_action':form_action})


def profile(request):
    template_name = 'users/profile.html'
    group_set = 'request.user.groups.all()'
    return render(request, template_name, {'groups': group_set})


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('users:profile')
    else:
        form = ChangePasswordForm(user=request.user, data=request.POST)
    form_title = 'Change password'
    form_back = '/users/profile/'
    form_action = '/users/change_password/'
    return render(request, 'users/general_form.html', {'form': form, 'form_title': form_title, 'form_back':form_back, 'form_action':form_action})


def join_group(request):
    if request.method == 'POST':
        form = JoinGroupForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('users:profile')
    else:
        form = JoinGroupForm(user=request.user, data=request.POST)
    form_title = 'Join New Group'
    form_back = '/users/profile/'
    form_action = '/users/join_group/'
    return render(request, 'users/general_form.html',
                  {'form': form, 'form_title': form_title, 'form_back': form_back, 'form_action': form_action})


def create_group(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            return redirect('users:profile')
    else:
        form = CreateGroupForm()
    form_title = 'Create New Group'
    form_back = '/users/profile/'
    form_action = '/users/create_group/'
    return render(request, 'users/general_form.html', {'form':form, 'form_title':form_title, 'form_back':form_back,'form_action':form_action})


def view_group(request, group_id):
    template_name = 'users/view_group.html'
    group = get_object_or_404(Group, pk=group_id)

    context = {}
    context['group'] = group
    users = []
    for user in User.objects.all():
        if group in user.groups.all():
            users.append(user)
    context['users'] = users

    return render(request, template_name, context)


def view_user(request, user_id):
    template_name = 'users/view_user.html'
    user = get_object_or_404(User, pk=user_id)

    context = {}
    context['viewed_user'] = user
    context['groups'] = user.groups.all()

    return render(request, template_name, context)


def suspend_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.user.is_site_manager:
        user.is_suspended = not user.is_suspended
        user.save()
    return redirect('users:user', user_id=user.id)


def promote_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.user.is_site_manager:
        user.is_site_manager = not user.is_site_manager
        user.save()
    return redirect('users:user', user_id=user.id)


def all_groups(request):
    template_name = 'users/all_groups.html'

    context = {}
    context['groups'] = Group.objects.all()

    return render(request, template_name, context)


def all_users(request):
    template_name = 'users/all_users.html'

    context = {}
    context['users'] = User.objects.all()

    return render(request, template_name, context)