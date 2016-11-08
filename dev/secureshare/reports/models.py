from django.db import models
from datetime import *


# Create your models here.

class FileUpload(models.Model):

    upload_id = models.AutoField(primary_key=True, default=0)
    title = models.TextField(default='title')
    file = models.FileField(default=None)
    timestamp = models.DateTimeField(auto_now_add=True)


class Report(models.Model):

    report_id = models.AutoField(primary_key=True, default=0)
    title = models.TextField(default="None", max_length= 50)
    short_description = models.TextField(default="", max_length=200)
    detailed_description = models.TextField(default="", max_length=5000)
    timestamp = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    encrypted = models.BooleanField(default=False)

    file = models.FileField(default=bin(0))