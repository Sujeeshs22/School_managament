from rest_framework import serializers

from school_admin.models import Teacher_admin,Subjects,StudentSubjects,HallTicketForStudent,Examination
from student.models import *


class AdminUpdateSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Teacher_admin
        fields = '__all__'


# for displaying student subectjs
class StudentSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubjects
        fields = '__all__'


# for adding subejcts for eeach student
class StudentSubjectInputSerializer(serializers.Serializer):
    student_name = serializers.CharField()
    subjects = serializers.ListField(
        child=serializers.CharField()
    )


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['full_name']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = ['sub_name']



class StudentSubjectSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = StudentSubjects
        fields = ['id', 'student', 'subject']



class SubjectUpdateSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Subjects
        fields = '__all__'


class HallTicketForStudentSerilizer(serializers.ModelSerializer):

    class Meta:
        model = HallTicketForStudent
        fields = '__all__'


class ExaminationSerilizer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Examination
        # fields = ['student', 'hall_ticket', 'has_attended', 'date_attended', 'status']
        fields = '__all__'

    def get_status(self, obj):
        print(obj)
        # print(self.active_status)
        return obj.active_status
        