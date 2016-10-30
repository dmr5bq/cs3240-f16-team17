from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, loader
from .models import FileUpload
from .forms import UploadFileForm


def index(request):

    if request.method == 'POST':

        form = UploadFileForm(request.POST)

        if form.is_valid():

            # file is saved
            file = request.POST['file']
            title = request.POST['title']

            return HttpResponseRedirect('upload/success') # this will redirect somewhere in the user profile

    # This means that the method == GET and it's before the file has been uploaded
    else:
        form = UploadFileForm()

        return render(request, 'upload/index.html', {'form': form})


def success(request):

    template = loader.get_template('upload/success.html')
    return render(template.render(request))