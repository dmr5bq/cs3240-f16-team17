from django.db import models
from datetime import *


# Create your models here.

class FileUpload(models.Model):
    title = models.TextField(default='title')
    file = models.FileField(default=None)
    timestamp = models.DateTimeField(default=datetime.now())


