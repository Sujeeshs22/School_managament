from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student
from student.serializers import StudentSerilizer
# Create your views here.




@api_view(['GET', 'POST'])
def AddStudent(request):
    if request.method == 'POST':
        serializer = StudentSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    elif request.method == 'GET':
        students = Student.objects.filter(standard=7)
        serializer = StudentSerilizer(students, many=True)
        return Response(serializer.data)
    

@api_view(['GET','POST'])
def student_subjects_view(request):
    from school_admin.models import StudentSubjects,Subjects
    from school_admin.serializer import StudentSubjectInputSerializer,StudentSubjectSerializer
    if request.method == 'POST':
        data = StudentSubjectInputSerializer(data=request.data)

        if data.is_valid():
            student_name = data.validated_data['student_name']
            subjects = data.validated_data['subjects']
            
            try:
                # Check if the student exists in the student table
                student = Student.objects.get(full_name=student_name)
            except Student.DoesNotExist:
                return Response({'status': 'student with this name does not exist'}, status=400)

            responses = []
            created_subjects = []
            for subject_name in subjects:
                try:
                    # Search for the subject in the subject table
                    subject = Subjects.objects.get(sub_name__icontains=subject_name)
                except Subjects.DoesNotExist:
                    responses.append({'error': f'Subject "{subject_name}" not found'})
                    continue
                
                # Add a check if the subject is already added to the student
                if StudentSubjects.objects.filter(subject=subject, student=student).exists():
                    responses.append({'message': f'Subject "{subject_name}" already added for student'})
                else:
                    # Create the StudentSubjects entry
                    student_subject = StudentSubjects.objects.create(subject=subject, student=student)
                    created_subjects.append(student_subject)
                    print(created_subjects)
                    responses.append({'message': f'Subject "{subject_name}" added successfully'})

            # Serialize the created StudentSubjects entries
            serializer = StudentSubjectSerializer(created_subjects, many=True)
            print(serializer)
            return Response({'messages': responses, 'data': serializer.data}, status=200)
        else:
            return Response(data.errors, status=400)   
    else:
        if request.method == 'GET':
            stud_name = request.data.get('student_name',None)
            if stud_name:
                # get the student from the db and chech wether student exists
                stud_name = Student.objects.get(full_name__icontains = stud_name)
                if stud_name is not None: 
                #    get all the subjects  of that particular student
                    stud_subjects = StudentSubjects.objects.filter(student = stud_name)
                    added_subject = []
                    student_deatils = None
                    data = {}
                    for subject in stud_subjects:
                        from school_admin.serializer import SubjectUpdateSerilizer
                        print(subject.subject)
                        subject_data = SubjectUpdateSerilizer(subject.subject).data
                        subject_data.pop('is_active', None) 
                        added_subject.append(subject_data)
                        
                    # Add student details only once after the loop
                    data['subject_details']=added_subject if added_subject else []
                    data['student_details'] = StudentSerilizer(stud_name).data

                    return Response(data)
                else:
                    return Response({'message':'student with this name does not exist'},status=300)
            else:
                return Response({'message':'student name must be provided'},status=300)
        return None
            
            