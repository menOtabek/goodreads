from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(default='Screenshot_from_2024-09-03_08-20-28.png')
