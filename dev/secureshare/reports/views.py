from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


from .forms import *
from .models import *

"""
10/30 DMR - there is some problem with form validation, so the form is not being stored at the moment

Goals:
    -> handle multiple files
    -> display progress bars
    -> handle file storage (filesystem?)
    -> successful redirect <--- probably has to do with form validation
    -> handle file encryption mechanism
    -> add encryption option to the form (button or checkbox?)
    -> include user information from the session for storage, determining ownership

"""



def handle_uploaded_file(f, title):
    with open('media/' + str(title), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # 10/30 DMR - This fails right now
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('reports/success') # this will redirect somewhere in the user profile
        else:
            return HttpResponse("Something went wrong with saving your file, please contact the administrator."
                                + " <a href=\"/reports/\">GO BACK</a>")
    # This means that the method == GET and it's before the file has been uploaded, shows form
    else:
        form = UploadFileForm()
        return render(request, 'reports/index.html', {'form': form})


def success(request):
    return render(request, 'reports/success.html')


def register_report(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], form.cleaned_data['title'])
            return HttpResponseRedirect('../success/')
    else:
        form = UploadFileForm()
    return render(request, 'reports/report.html', {'form': form})





class AllReportListView(ListView):

    template_name = "reports/all_reports.html"
    model = Report

    def get_context_data(self, **kwargs):
        context = super(AllReportListView, self).get_context_data(**kwargs)
        return context


class MyReportListView(ListView):

    template_name = "reports/my_reports.html"
    model = Report

    def get_context_data(self, **kwargs):
        context = super(MyReportListView, self).get_context_data(**kwargs)
        # TODO: get reports that point to this folder
        context['reports_list'] = Report.objects.filter(owner=self.request.user)
        context['folder_list'] = SubFolder.objects.filter(parent_folder=self.request.user.root_folder)
        return context


class ReportDetailView(DetailView):

    template_name = "reports/view_report.html"
    model = Report

    def get_context_data(self, **kwargs):
        context = super(ReportDetailView, self).get_context_data(**kwargs)
        return context


def delete_report(request, report_id):

    report = get_object_or_404(Report, pk=report_id)
    if request.user.is_site_manager or request.user is report.owner:
        report.delete()
    return redirect('home:home')


def view_folder(request, folder_id):

    template_name = 'reports/view_folder.html'
    folder = get_object_or_404(SubFolder, pk=folder_id)

    context = {}
    if folder.parent_folder.is_root:
        context['parent_is_root'] = True
    context['this_folder'] = folder
    # TODO get reports that point to this folder
    # perhaps also implement breadcrumbs in the view_folder
    # context['reports_list'] = Report.objects.filter(parent_folder=folder)
    context['folder_list'] = folder.sub_folder.all()
    return render(request, template_name, context)



