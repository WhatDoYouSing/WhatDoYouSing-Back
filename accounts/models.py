from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    nickname=models.CharField(max_length=10, null=True, blank=True)
    
    profile_choices=[
        (1,1),
        (2,2),
        (3,3),
        (4,4)
    ]
    profile=models.IntegerField(choices=profile_choices, null=True, blank=True)

    def __str__(self):
        return self.username
