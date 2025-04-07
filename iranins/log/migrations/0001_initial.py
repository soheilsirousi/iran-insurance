# Generated by Django 4.2 on 2025-04-07 06:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', models.PositiveSmallIntegerField(choices=[(1, 'ایجاد'), (2, 'ویرایش'), (3, 'حذف')], default=1)),
                ('description', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_logs', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_logs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
