from django.core.management import BaseCommand

from materials.models import Lesson
from users.models import Payment


class Command(BaseCommand):

    def handle(self, *args, **options):
        lesson_1 = Lesson(id=2)
        payment_list = [
            {'date': '2024-02-01', 'lesson': lesson_1, 'amount': 15000, 'method': 'cash'},
            {'date': '2024-02-02', 'lesson': lesson_1, 'amount': 25000, 'method': 'card_pay'},
            {'date': '2024-02-03', 'lesson': lesson_1, 'amount': 10000, 'method': 'certificate'},
        ]
        for payment in payment_list:
            Payment.objects.create(**payment)
