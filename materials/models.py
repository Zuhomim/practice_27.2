from django.db import models

from config import settings

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')
    preview = models.ImageField(upload_to='materials/courses/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.name} ({self.description[:30]})'


class Lesson(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')
    description = models.CharField(max_length=100, verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(upload_to='materials/lessons/', verbose_name='Превью', **NULLABLE)
    video_link = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.name} ({self.course.name})'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    is_active = models.BooleanField(default=True, verbose_name="Активность подписки")

    def __str__(self):
        return f'{self.user} ({self.course.name})'
