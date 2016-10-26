from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None):
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        return user

    def create_normal_user(self, email=None, first_name=None, last_name=None, password=None):
        user = self.create_user(email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user

    def create_site_manager(self, email=None, first_name=None, last_name=None, password=None):
        user = self.create_user(email=email, password=password)
        user.is_site_manager = True
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, blank=False)
    is_active = models.BooleanField(default=True)

    # User Fields
    first_name = models.CharField(max_length=40, null=True)
    last_name = models.CharField(max_length=40, null=True)

    # Site Manager Fields
    is_site_manager = models.BooleanField(default=False)

    # Objects Manager Class
    objects = UserManager()

    USERNAME_FIELD = 'email'




