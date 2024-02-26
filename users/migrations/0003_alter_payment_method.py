# Generated by Django 5.0.2 on 2024-02-26 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='method',
            field=models.CharField(choices=[('cash', 'Наличные'), ('card_pay', 'Банковская карта'), ('certificate', 'Сертификат')], max_length=30, verbose_name='Способ оплаты'),
        ),
    ]
