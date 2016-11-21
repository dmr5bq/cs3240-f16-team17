from django.db import models
from datetime import *
from users.models import *


# Create your models here.
class Folder(models.Model):

    name = models.CharField(max_length=50, default="")
    is_root = models.BooleanField(default=False)


class RootFolder(Folder):

    owner = models.OneToOneField(User, related_name="root_folder")


class SubFolder(Folder):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_folder = models.ForeignKey(Folder, related_name="sub_folder")


class Report(models.Model):

    title = models.TextField(default="None", max_length= 50)
    short_description = models.TextField(default="", max_length=200)
    detailed_description = models.TextField(default="", max_length=5000)
    timestamp = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    encrypted = models.BooleanField(default=False)

    parent_folder = models.ForeignKey(Folder, related_name="reports")
    # reports must be given a parent folder upon creation


class FileUpload(models.Model):

    title = models.TextField(default='title')
    file = models.FileField(default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    report = models.ForeignKey(Report)
    # uploads must be given reports upon creation

