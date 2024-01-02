from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    nickname=models.CharField(max_length=10)
    report=models.IntegerField(null=True, blank=True)
    count=models.IntegerField(null=True, blank=True)
