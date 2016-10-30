from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, loader
from .models import FileUpload


def index(request):
    template = loader.get_template('upload/index.html')
    return HttpResponse(template.render(request))


def upload_file(request):
    if request.method == 'POST':
        form = FileUpload(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('')

    else:
        form = FileUpload()

    return render(request, 'upload.html', {'form': form})