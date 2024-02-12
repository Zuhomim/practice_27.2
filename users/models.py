import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=30, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=30, verbose_name='страна', **NULLABLE)
    uuid = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
