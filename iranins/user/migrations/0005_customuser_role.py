# Generated by Django 4.2 on 2025-03-28 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_customuser_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'مدیر'), (2, 'پشتیبان'), (3, 'مشتری')], default=3, verbose_name='role'),
        ),
    ]
