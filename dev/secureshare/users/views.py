from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash

from .forms import RegisterUserForm, ChangePasswordForm


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('login')
    else:
        form = RegisterUserForm()
    form_title = 'Create New User'
    form_back = '/users/login/'
    form_action = '/users/register/'
    return render(request, 'users/general_form.html', {'form': form, 'form_title':form_title, 'form_back':form_back, 'form_action':form_action})


def profile(request):
    template_name = 'users/profile.html'
    group_set = ''#request.user.group_set.all()
    return render(request, template_name, {'groups': group_set})


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = ChangePasswordForm(user=request.user, data=request.POST)
    form_title = 'Change password'
    form_back = '/users/profile/'
    form_action = '/users/change_password/'
    return render(request, 'users/general_form.html', {'form': form, 'form_title': form_title, 'form_back':form_back, 'form_action':form_action})
