from django.db import models
from accounts.models import User
from posts.models import Post, Emotion

# Create your models here.

class MyPage(models.Model):
    user = models.ForeignKey("accounts.User", null=True, on_delete=models.CASCADE)