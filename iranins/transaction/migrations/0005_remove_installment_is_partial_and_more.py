# Generated by Django 4.2 on 2025-04-03 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_installment_is_partial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='installment',
            name='is_partial',
        ),
        migrations.AddField(
            model_name='installment',
            name='is_complete',
            field=models.BooleanField(default=False, verbose_name='is complete'),
        ),
    ]
