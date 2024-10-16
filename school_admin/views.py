from rest_framework.decorators import api_view
from rest_framework.response import Response

from student.models import Student
from .models import HallTicketForStudent, StudentSubjects, Teacher_admin,Examination
from school_admin.serializer import AdminUpdateSerilizer,SubjectUpdateSerilizer,HallTicketForStudentSerilizer,ExaminationSerilizer
from rest_framework import status
from rest_framework import viewsets

@api_view(['GET', 'POST'])
def AddTeacher(request):
    if request.method == 'POST':
        serializer = AdminUpdateSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    elif request.method == 'GET':
        teachers = Teacher_admin.objects.all()
        serializer = AdminUpdateSerilizer(teachers, many=True)
        return Response(serializer.data)
    

    
@api_view(['GET'])
def GetStudentForteacher(request):
    if request.method =='GET':
        teacher_name = request.POST.get('teacher_name',None)
        print(teacher_name)
        if teacher_name:
            get_teacher = Teacher_admin.objects.filter(first_name__icontains=teacher_name).first()
            if get_teacher:
                from student.models import Student
                from student.serializers import StudentSerilizer
                students = Student.objects.filter(admin_teacher= get_teacher.pk)
                print(students)
                details ={}
                teacher_details = AdminUpdateSerilizer(get_teacher).data if get_teacher else None
                if students:
                    serializer =  StudentSerilizer(students,many = True)
                    details['teacher'] = teacher_details
                    details['student_deatils'] = serializer.data
                    return Response(details,status=status.HTTP_200_OK)
                else:
                    return Response({'message':'No students exist under this teacher'},status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message':'teacher with name does noit exsit'},status=status.HTTP_400_BAD_REQUEST)
        else:
            Response({'message':"teacher name must be provided"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def GetStudentDetails(request):

    if request.method == 'GET':
        student_name = request.POST.get('student_name',None)
        if student_name:
            from student.models import Student
            from student.serializers import StudentMiniSerilizer
            student_student = Student.objects.filter(first_name__icontains = student_name).first()
            if student_student:
               serializer = StudentMiniSerilizer(student_student)
               return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({'message':'no student under that name exist'},status= status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'student name is not provided'},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET','POST'])
def AddSubjects(request):
    if request.method == "POST":
        serializer = SubjectUpdateSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'subject added successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        if request.method == 'GET':
            from school_admin.models import Subjects
            subjects = Subjects.objects.all()
            serializer = SubjectUpdateSerilizer(subjects,many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        


class SubjectForStudents(viewsets.ModelViewSet):
    from .serializer import StudentSerializer
    from student.models import Student
    from .models import StudentSubjects
    serializer_class = StudentSerializer
    # queryset = StudentSubjects.objects.filter(student== 'ronaldo')



    def get_queryset(self):
        subject_sub = self.request.data.get('subject_name',None)
        subjects = None
        if subject_sub:
            subjects = StudentSubjects.objects.filter(subject = subject_sub).values('student')
        
        return self.serializer_class(subjects).data if subjects else []
    


class StudentHallTicketViewset(viewsets.ModelViewSet):
    # queryset = Student.objects.all()
    serializer_class = HallTicketForStudentSerilizer

    def create(self, request, *args, **kwargs):
        # Extract the data from the request
        data = request.data
        student_id = data.get('student', None)
        
        # Check if student_id is provided
        if student_id:
            # Check if a hall ticket for this student already exists
            student_hall_tck_exists = HallTicketForStudent.objects.filter(student_id=student_id).exists()
            
            # If hall ticket already exists, return a response and don't save
            if student_hall_tck_exists:
                return Response(
                    {"detail": "Hall ticket already exists for this student."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Proceed to create the hall ticket if it does not exist
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        # Save the student instance to trigger the hall ticket generation logic in the model
        hall_ticket_for_student = serializer.save()

        # Call the `save` method explicitly to ensure the hall ticket is generated
        hall_ticket_for_student.save()
        
        # Return the response with the student data including the hall ticket (if issued)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    



class YearExamminationViewSet(viewsets.ModelViewSet):
   serializer_class = ExaminationSerilizer
   queryset = Examination.objects.all()

   def get_queryset(self):
       return super().get_queryset()
   

   def create(self, request, *args, **kwargs):
        # Extract student and subject from request data
        student_id = request.data.get('student', None)
        subject_id = request.data.get('subject', None)
        print(subject_id)

        # Check if an Examination entry already exists for the student and subject
        if Examination.objects.filter(student_id=student_id, subject_id=subject_id).exists():
            return Response(
                {"detail": "Examination entry already exists for this student and subject."},
                status=400
            )

        # Proceed with the creation if no duplicate entry is found
        response = super().create(request, *args, **kwargs)
        print(response)
        # Check if the student has a hall ticket
        if Student.objects.filter(pk=student_id).exists():
            student_obj = Student.objects.get(pk=student_id)
            hall_tkt = HallTicketForStudent.objects.filter(student=student_obj).first()
            
            # If a hall ticket exists, update the Examination record
            if hall_tkt:
                exam_entry = Examination.objects.get(pk=response.data['id'])
                exam_entry.hall_ticket = hall_tkt
                exam_entry.save()

        return response

