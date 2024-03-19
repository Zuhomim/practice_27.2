from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from materials.models import Subscription


@shared_task
def send_mail_for_updates(course_id):

    subscriptions = Subscription.objects.filter(pk=course_id, is_active=True)

    for subscription in subscriptions:
        if subscription.user.email:
            send_mail(
                subject="Курс обновлен!",
                message=f"Курс {subscription.course.name} обновлен. Ознакомьтесь с материалами!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscription.user.email],
                fail_silently=False
            )
