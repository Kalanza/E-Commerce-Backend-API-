from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _ 
from django.utils import timezone

# Import the manager we defined in the previous step
from .users import CustomUserManager
# Import TimestampedModel for soft delete functionality
from core.models import TimestampedModel

class CustomUser(TimestampedModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email instead of using username.
    """
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True)
    is_verified = models.BooleanField(_('email verified'), default=False)

    #Required fields for admin management
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    #Connect the Custom Manager
    objects = CustomUserManager()

    #Configuration
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] #Email & Password are required by default

    def __str__(self):
        return self.email