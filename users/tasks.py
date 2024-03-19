from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

import logging
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)


@shared_task
def check_last_date():
    """Проверка активности пользователя за последний месяц"""

    User = get_user_model()
    month_ago = timezone.now() - relativedelta(months=1)
    # deadline_data = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(
        last_login__lt=month_ago, is_active=True
    )
    inactive_users_count = inactive_users.update(is_active=False)

    logger.info('Deactivated %d users', inactive_users_count)
