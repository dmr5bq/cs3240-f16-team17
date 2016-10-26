from django.shortcuts import render, redirect

from .forms import RegisterUserForm
from .models import User


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
    form_action = '/users/register/'
    return render(request, 'users/general_form.html', {'form': form, 'form_title':form_title, 'form_action':form_action})
