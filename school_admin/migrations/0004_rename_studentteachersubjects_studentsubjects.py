# Generated by Django 3.2.25 on 2024-08-01 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_auto_20240724_0953'),
        ('school_admin', '0003_remove_studentteachersubjects_teacher'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StudentTeacherSubjects',
            new_name='StudentSubjects',
        ),
    ]
