from django import forms
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
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user