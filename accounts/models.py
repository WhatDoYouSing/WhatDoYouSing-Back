from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    nickname=models.CharField(max_length=10, null=True, blank=True)
    #report=models.IntegerField(null=True, blank=True)
    
    profile_choices=[
        (1,'chicken'),
        (2,'cat'),
        (3,'dog'),
        (4,'horse')
    ]
    profile=models.IntegerField(choices=profile_choices, null=True, blank=True)

    def __str__(self):
        return self.username

    #비밀번호 확인을 위한 필드 모델 / 시리얼라이저 <- 아마 시리얼라이저일듯
    #confirm_password=models.CharField(max_length=128, default='')
