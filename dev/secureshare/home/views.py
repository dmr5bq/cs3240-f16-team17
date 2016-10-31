from django.shortcuts import render

# Create your views here.


def HomeView(request):
    template_name='home/home.html'
    return render(request, template_name)
