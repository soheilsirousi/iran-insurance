# Generated by Django 4.2 on 2025-04-06 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0012_remove_installment_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='balance',
            old_name='type',
            new_name='balance_type',
        ),
    ]
