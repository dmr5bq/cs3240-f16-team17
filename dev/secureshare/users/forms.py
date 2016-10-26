from django import forms

from .models import User


class RegisterUserForm(forms.Form):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    password1 = forms.CharField()
    password2 = forms.CharField()

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