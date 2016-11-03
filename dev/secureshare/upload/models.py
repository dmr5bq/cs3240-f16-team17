from django.db import models
from datetime import *


# Create your models here.

class FileUpload(models.Model):
    upload_id = models.AutoField(primary_key=True)
    title = models.TextField(default='title')
    file = models.FileField(default=None)
    timestamp = models.DateTimeField(default=datetime.now())


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    title = models.TextField(default="None")
    encrypted = models.BooleanField(default=False)
    file = models.BinaryField(default=bin(0))
    timestamp = models.DateTimeField(default=datetime.now())
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)