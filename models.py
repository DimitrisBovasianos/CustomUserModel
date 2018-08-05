from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import (BaseUserManager,AbstractBaseUser)
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

class MyUserManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
           username=username,
           email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,email,password):
        user = self.create_user(
           username,
           email=email,
           password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    username = models.CharField(
      max_length = 250,
      unique = True,
    )
    email = models.EmailField(
    verbose_name = 'email address',
    max_length = 255,
    unique = True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)



    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


    def has_perm(self, perm, obj=None):
        "Does the user have a spesific permission?"
        #Simplest possible answer: Yes, always
        return True

    def has_module_perms(self,app_label):
        "Does the user have permission to view the app app_label ?"
        return True

    def get_full_name(self):
        """
        Returns email instead of the fullname for the user.
        """
        return str(self.username)

    def get_short_name(self):
        """
        Returns the short name for the user.
        This function works the same as `get_full_name` method.
        It's just included for django built-in user comparability.
        """
        return self.get_full_name()

    def get_email(self):
        return self.email



    @property
    def is_staff(self):
        'Is the user a member of staff?'
        return self.is_admin

    def email_user(self, *args, **kwargs):
        send_mail(
        '{}'.format(args[0]),
        '{}'.format(args[1]),
        "Searchsite",
        [args[2]],
       )
