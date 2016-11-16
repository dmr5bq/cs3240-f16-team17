from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


from .forms import *
from .models import *
from reports.models import RootFolder


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            rf = RootFolder(name=user.email, owner=user, is_root=True)
            rf.save()
            messages.success(request, user.email)
            return redirect('users:login')
    else:
        form = RegisterUserForm()
    form_title = 'Create New User'
    form_back = '/users/login/'
    form_action = '/users/register/'
    return render(request, 'users/general_form.html', {'form': form, 'form_title':form_title, 'form_back':form_back, 'form_action':form_action})


def profile(request):
    template_name = 'users/profile.html'
    return render(request, template_name, {})


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
    return render(request, 'users/general_form.html', {'form': form, 'form_title': form_title, 'form_back': form_back, 'form_action': form_action})


def leave_group(request):
    if request.method == 'POST':
        form = LeaveGroupForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('users:profile')
    else:
        form = LeaveGroupForm(user=request.user, data=request.POST)
    form_title = 'Join New Group'
    form_back = '/users/profile/'
    form_action = '/users/leave_group/'
    return render(request, 'users/general_form.html', {'form': form, 'form_title': form_title, 'form_back': form_back, 'form_action': form_action})


def leave_group_by_id(request, group_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    group = get_object_or_404(Group, pk=group_id)
    if user == request.user or request.user.is_site_manager:
        if group in user.groups.all():
            user.groups.remove(group)
    return redirect('users:group', group_id=group_id)


def add_user_to_group(request, group_id):
    if request.method == 'POST':
        form = AddUserToGroupForm(data=request.POST)
        if form.is_valid():
            form.save(group_id=group_id)
            return redirect('users:all_groups')
    else:
        form = AddUserToGroupForm(data=request.POST)
    form_title = 'Add User To Group'
    form_back = '/users/all_groups/'
    form_action = '/users/user/' + str(group_id) + '/add_user_to_group/'
    return render(request, 'users/general_form.html',
                  {'form': form, 'form_title': form_title, 'form_back': form_back, 'form_action': form_action})


def create_group(request):
    if request.method == 'POST':
        form = CreateGroupForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('users:profile')
    else:
        form = CreateGroupForm(user=request.user, data=request.POST)
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
    context['viewed_users'] = users
    context['user'] = request.user
    context['user_in_group'] = group in request.user.groups.all()

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


def remove_user_from_group(request, user_id, group_id):
    user = get_object_or_404(User, pk=user_id)
    if request.user.is_site_manager:
        g = Group.objects.get(id=group_id)
        user.groups.remove(g)
    if '/user/' in request.META['HTTP_REFERER']:
        return redirect('users:user', user_id=user_id)
    elif '/group/' in request.META['HTTP_REFERER']:
        return redirect('users:group', group_id=group_id)
    else:
        return redirect('home:home')


def my_groups(request):
    template_name = 'users/my_groups.html'

    context = {}
    context['groups'] = request.user.groups.all()

    return render(request, template_name, context)


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



'''
def inbox(request):
    template_name = 'users/inbox.html'
    message_set = Message.objects.inbox(request.user)
    return render(request, template_name, {'message_set': message_set},)


def outbox(request):
    template_name = 'users/outbox.html'

    context = {}
    context['users'] = User.objects.all()

    return render(request, template_name, context)



def send_message(request):
    if request.method == 'POST':
        form = SendMessageForm()
        if form.is_valid():
            form.save(sender=request.user)
            return redirect('users:profile')

    else:
        form = SendMessageForm()
    form_title = 'Send New Message'
    form_back = '/users/outbox/'
    form_action = '/users/outbox/'
    return render(request, 'users/general_form.html',
                  {'form': form, 'form_title': form_title, 'form_back': form_back, 'form_action': form_action})
'''
