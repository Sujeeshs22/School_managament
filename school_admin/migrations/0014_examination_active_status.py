# Generated by Django 3.2.25 on 2024-09-25 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_admin', '0013_auto_20240925_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='examination',
            name='active_status',
            field=models.TextField(blank=True, null=True),
        ),
    ]
