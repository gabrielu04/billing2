from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import AuthUserManager


# Create your models here.
class AuthUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, verbose_name='email', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AuthUserManager()

    def __str__(self):
        return self.email

    def __repr__(self):
        return self.__str__()
