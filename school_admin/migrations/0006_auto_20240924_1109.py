# Generated by Django 3.2.25 on 2024-09-24 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_admin', '0005_hallticketforstudent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hallticketforstudent',
            name='hallticket_for_stud',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='hallticketforstudent',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
