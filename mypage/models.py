from django.db import models
from accounts.models import User

# Create your models here.

class MyPage(models.Model):
    user = models.ForeignKey("accounts.User", null=True, on_delete=models.CASCADE)