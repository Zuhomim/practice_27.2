import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=30, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=30, verbose_name='страна', **NULLABLE)
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Payment(models.Model):

    PAYMENT_METHOD_CHOICE = [
        ('cash', 'Наличные'),
        ('card_pay', 'Банковская карта'),
        ('certificate', 'Сертификат'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    date = models.DateField(verbose_name='Дата платежа', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE , verbose_name='Оплачиваемый курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплачиваемый урок', **NULLABLE)
    amount = models.IntegerField(verbose_name='Сумма платежа')
    method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICE, verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.user.name} ({self.course if self.course else self.lesson})'
