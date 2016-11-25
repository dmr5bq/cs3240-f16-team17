from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.conf import settings
from django.contrib import messages

from wsgiref.util import FileWrapper

import os
import zipfile

import tarfile
from io import BytesIO, StringIO

from .forms import *
from .models import *


def handle_uploaded_file(f, report, count):
    f_upload = FileUpload(title=f.name, file=f, report=report)
    f_upload.save()
    new_name = str(f_upload.id)
    os.rename(f_upload.file.path, settings.MEDIA_ROOT + '/' + new_name)
    f_upload.file.name = new_name
    f_upload.save()


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # 10/30 DMR - This fails right now
        if form.is_valid():

            form.save()
            return HttpResponseRedirect('reports/all_reports') # this will redirect somewhere in the user profile
        else:
            return HttpResponse("Something went wrong with saving your file, please contact the administrator."
                                + " <a href=\"/reports/\">GO BACK</a>")
    # This means that the method == GET and it's before the file has been uploaded, shows form
    else:
        form = UploadFileForm()
        return render(request, 'reports/index.html', {'form': form})


'''
def register_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            for count, f in enumerate(request.FILES.getlist('file_field')):
                handle_uploaded_file(f, form.cleaned_data['title'] + str(count))
            messages.success(request, form.cleaned_data['title'])
            return HttpResponseRedirect('/reports:my_reports/')
    else:
        form = ReportForm()
    form_title = 'Create New Report'
    form_back = '/reports/my_reports/'
    form_action = '/reports/all_reports/'
    return render(request, 'users/general_form.html',
                  {'form': form, 'form_title': form_title, 'form_back': form_back, 'form_action': form_action})

'''


def register_report(request, folder_id):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            report = Report(title=form.cleaned_data['title'], short_description=form.cleaned_data['short_description'],
                            detailed_description=form.cleaned_data['detailed_description'],
                            is_private=form.cleaned_data['is_private'], encrypted=form.cleaned_data['encrypted'],
                            owner=request.user, parent_folder=get_object_or_404(Folder, pk=folder_id))
            report.save()
            for count, f in enumerate(request.FILES.getlist('file_field')):
                handle_uploaded_file(f, report, count)
            messages.success(request, form.cleaned_data['title'])
            return HttpResponseRedirect('/reports/my_reports/')
    else:
        form = UploadFileForm()
    return render(request, 'reports/report.html', {'form': form})


def all_reports(request, detail='short'):

    template_name = "reports/all_reports.html"

    context = {}
    if request.user.is_authenticated:
        if request.user.is_site_manager:
            context['reports_list'] = Report.objects.all()
        else:
            context['reports_list'] = Report.objects.filter(Q(owner=request.user) | Q(is_private=False))
    else:
        context['reports_list'] = Report.objects.filter(is_private=False)
    context['detail'] = '/detail/' in request.path

    return render(request, template_name, context)


class MyReportListView(ListView):

    template_name = "reports/my_reports.html"
    model = Report

    def get_context_data(self, **kwargs):
        context = super(MyReportListView, self).get_context_data(**kwargs)
        context['reports_list'] = Report.objects.filter(parent_folder=self.request.user.root_folder)
        context['folder_list'] = SubFolder.objects.filter(parent_folder=self.request.user.root_folder)
        return context


class ReportDetailView(DetailView):

    template_name = "reports/view_report.html"
    model = Report

    def get_context_data(self, **kwargs):
        context = super(ReportDetailView, self).get_context_data(**kwargs)
        context['file_list'] = FileUpload.objects.filter(report=get_object_or_404(Report, pk=self.kwargs['pk']))
        return context


def edit_report(request, report_id):

    report = get_object_or_404(Report, pk=report_id)
    if request.user.is_site_manager or request.user == report.owner:
        if request.method == "POST":
            report.title = request.POST['title']
            report.short_description = request.POST['sDesc']
            report.detailed_description = request.POST['dDesc']
            print(request.POST['privacy'])
            if request.POST['privacy'] == "p":
                report.is_private = True
            else:
                report.is_private = False
            report.save()
    return redirect(request.META['HTTP_REFERER'])


def delete_report(request, report_id):

    report = get_object_or_404(Report, pk=report_id)
    if request.user.is_site_manager or request.user == report.owner:
        parent_folder_id = report.parent_folder.id
        report.delete()
        return redirect('reports:view_folder', folder_id=parent_folder_id)
    # add success message
    return redirect('home:home')


def view_folder(request, folder_id):

    if int(request.user.root_folder.id) == int(folder_id):
        return redirect('reports:my_reports')

    template_name = 'reports/view_folder.html'
    folder = get_object_or_404(Folder, pk=folder_id)

    context = {}
    if not folder.is_root:
        folder = get_object_or_404(SubFolder, pk=folder_id)
        context['parent_folder'] = folder.parent_folder
        # context['came_from_reports'] = "/my_reports/" in request.META['HTTP_REFERER']

    context['this_folder'] = folder
    # TODO get reports that point to this folder
    # perhaps also implement breadcrumbs in the view_folder
    # folder deletion
    # folder creation by form
    context['reports_list'] = Report.objects.filter(parent_folder=folder)
    context['folder_list'] = folder.sub_folder.all()
    return render(request, template_name, context)


def new_folder(request, folder_id):

    if request.POST:
        if request.user.is_authenticated:
            current_folder = get_object_or_404(Folder, pk=folder_id)
            if current_folder.is_root:
                if request.user.is_site_manager or int(request.user.root_folder.id) == int(folder_id):
                    current_folder = get_object_or_404(RootFolder, pk=folder_id)
                    name = request.POST['name']
                    sub = SubFolder(name=name, owner=request.user, parent_folder=current_folder)
                    sub.save()
            else :
                current_folder = get_object_or_404(SubFolder, pk=folder_id)
                if current_folder.owner == request.user:
                    name = request.POST['name']
                    sub = SubFolder(name=name, owner=request.user, parent_folder=current_folder)
                    sub.save()
            return redirect(request.META['HTTP_REFERER'])
    return redirect('home:home')


def delete_folder(request, folder_id):

    folder = get_object_or_404(SubFolder, pk=folder_id)
    if request.user.is_site_manager or request.user == folder.owner:
        parent_folder_id = folder.parent_folder.id
        folder.delete()
        # add success message
        return redirect('reports:view_folder', folder_id=parent_folder_id)
    return redirect('home:home')


def download_file(request, file_id):
    upload = get_object_or_404(FileUpload, pk=file_id)
    if request.user.is_authenticated and not upload.report.is_private or upload.report.owner == request.user or request.user.is_site_manager:
        file = upload.file
        response = HttpResponse(FileWrapper(file), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="' + str(upload.title) + '"'
        return response
    return redirect('home:home')


def delete_file(request, file_id):
    upload = get_object_or_404(FileUpload, pk=file_id)
    if request.user.is_authenticated and upload.report.owner == request.user or request.user.is_site_manager:
        upload.delete()
    return redirect(request.META['HTTP_REFERER'])


def download_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    # check permissions
    if request.user.is_authenticated and not report.is_private or report.owner == request.user or request.user.is_site_manager:
        uploads = FileUpload.objects.filter(report=report)
        out = BytesIO()
        tar = tarfile.open(report.title+'.tar.gz', mode="w:gz", fileobj = out)
        for upload in uploads:
            info = tarfile.TarInfo(name=upload.title)
            tar.addfile(tarinfo=info, fileobj=FileWrapper(upload.file))
        print(tar.getmembers())
        tar.close()

        response = HttpResponse(out.getvalue(), content_type='application/tgz')
        response['Content-Length'] = os.path.getsize(report.title+'.tar.gz')
        response['Content-Disposition'] = 'attachment; filename='+report.title+'.tar.gz'
        return response
    return redirect('reports:view_report', pk=report_id)


def all_documents(request):
    if request.user.is_authenticated and request.user.is_site_manager:
        template_name='reports/all_documents.html'
        context = {}
        context['documents_list'] = FileUpload.objects.all()
        return render(request, template_name, context)
    return redirect('home:home')

