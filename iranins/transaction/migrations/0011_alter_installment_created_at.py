# Generated by Django 4.2 on 2025-04-06 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0010_installment_created_at_installment_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installment',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='created at'),
        ),
    ]
