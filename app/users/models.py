from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import random
import string

import pyotp

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(
            phone_number=phone_number,
        )
        
        user.set_unusable_password()  # No password, because OTP will be used
        
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, password=None):
        user = self.create_user(
            phone_number=phone_number,
        )
        user.is_staff = True
        user.is_superuser = True
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=13, unique=True)  # '+998' bilan
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='user_phone_set',  # Yangi nom
        related_query_name='user',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='user_phone_permissions_set',  # Yangi nom
        related_query_name='user',
    )
    objects = UserManager()
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

class Session(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secret = models.CharField(max_length=100, default=pyotp.random_base32, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.phone_number}'