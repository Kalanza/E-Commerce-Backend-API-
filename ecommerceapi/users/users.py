from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, ** extra_fields):
        """
        Create and Save a  User with the given email and password.
        """
        if not email:
            raise ValueError(('The email must be set'))
        
        # 1. Normalize the email (Standard BaseUserManager Method)
        email = self.normalize_email(email)

        # 2. Create the model instance (but don't save to DB yet)
        user = self.model(email=email , **extra_fields)

        # 3. Hash the password(CRITICAL STEP)
        user.set_password(password)

        # 4.Save to the database
        user.Save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and  save a SuperUser with the given email and password
        """
        #Set default permissions for a superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('SuperUser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('SuperUser must have is_superuser=True'))
        
        return self.create_user(email, password, **extra_fields)

    







