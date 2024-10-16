from django.db import models

class Student(models.Model):
    STANDARD_CHOICES = [
        (1, 'I'),
        (2, 'II'),
        (3, 'III'),
        (4, 'IV'),
        (5, 'V'),
        (6, 'VI'),
        (7, 'VII'),
        (8, 'VIII'),
        (9, 'IX'),
        (10, 'X'),
        (11, 'XI'),
        (12, 'XII'),
    ]

    full_name = models.TextField(blank=True, null=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=20)
    standard = models.CharField(max_length=250, choices=STANDARD_CHOICES)
    admin_teacher = models.ForeignKey('school_admin.Teacher_admin', related_name='teacher_student', on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name
