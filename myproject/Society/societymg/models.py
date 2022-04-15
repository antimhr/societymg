from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    flat = models.IntegerField(unique=True, default=0)
    tower = models.IntegerField(unique=True, default=0)
    phone = models.IntegerField(unique=True, default=0)
    password = models.CharField(max_length=25, default=0)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
