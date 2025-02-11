# Generated by Django 3.2.25 on 2024-09-24 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_auto_20240724_0953'),
        ('school_admin', '0004_rename_studentteachersubjects_studentsubjects'),
    ]

    operations = [
        migrations.CreateModel(
            name='HallTicketForStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_issued', models.BooleanField(default=False)),
                ('hallticket_for_stud', models.CharField(max_length=5)),
                ('is_active', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_hall_tickt', to='student.student')),
            ],
        ),
    ]
