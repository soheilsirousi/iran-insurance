# Generated by Django 4.2 on 2025-03-25 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='payment_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'کارتخوان'), (2, 'کارت به کارت')], verbose_name='payment type'),
        ),
    ]
