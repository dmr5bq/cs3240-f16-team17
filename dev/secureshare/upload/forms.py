from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50, min_length=3)
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))





