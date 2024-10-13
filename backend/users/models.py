from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserModel(AbstractUser):
    username = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'user'
