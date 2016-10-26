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
    return render(request, 'users/register.html', {'form': form})
