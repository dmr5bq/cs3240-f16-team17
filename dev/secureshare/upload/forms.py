from django import forms
from django.forms import ModelForm
from .models import Report


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50, min_length=3)
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'encrypted', 'file']



"""
class Report(models.Model):
    report_id = models.AutoField(primary_key=True, default=0)
    title = models.TextField(default="None")
    encrypted = models.BooleanField(default=False)
    file = models.BinaryField(default=bin(0))
    timestamp = models.DateTimeField(default=datetime.now())
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
"""


