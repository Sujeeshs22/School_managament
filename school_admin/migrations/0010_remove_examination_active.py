# Generated by Django 3.2.25 on 2024-09-25 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school_admin', '0009_examination_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examination',
            name='active',
        ),
    ]
