from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _

from .models import User


class RegisterUserForm(forms.Form):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password (again)"), widget=forms.PasswordInput)

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
            raise forms.ValidationError("User with this email already exists")
        except User.DoesNotExist:
            pass
        return self.cleaned_data['email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = User.objects.create_normal_user(
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(label=_("Current Password"), widget=forms.PasswordInput)
    new_password1 = forms.CharField(label=_("New Password"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New Password (again)"), widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        try:
            user = authenticate(email=self.user.email, password=self.cleaned_data['current_password'])
            if user is None:
                raise forms.ValidationError(_("Incorrect Password."))
        except PermissionDenied:
            raise forms.ValidationError(_("Incorrect Password."))

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return new_password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])

        if commit:
            self.user.save()

        return self.user


