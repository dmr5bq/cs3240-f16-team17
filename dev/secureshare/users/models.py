from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group
from django.utils.translation import gettext as _

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

    # GROUPS B O Y S
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )

    # Site Manager Fields
    is_site_manager = models.BooleanField(default=False)

    # Objects Manager Class
    objects = UserManager()

    USERNAME_FIELD = 'email'
