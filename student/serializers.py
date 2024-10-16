from rest_framework import serializers

from  .models import Student
from school_admin.serializer import *


class StudentSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Student
        exclude = ['admin_teacher']



class StudentMiniSerilizer(serializers.ModelSerializer):
    admin_teacher = AdminUpdateSerilizer()

    class Meta:
            model = Student
            fields = ['id', 'full_name', 'first_name', 'last_name', 'email', 'age', 'phone_number', 'standard', 'admin_teacher']
            