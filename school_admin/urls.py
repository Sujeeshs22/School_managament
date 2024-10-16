from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
 path('add_teacher/', views.AddTeacher, name='add_teacher'),
 path('get-student-teacher/',views.GetStudentForteacher, name='getsdtudentsunderteacher'),
 path('student-details/',views.GetStudentDetails, name='student_deatils'),
 path('add-subject/', views.AddSubjects, name='add-subject'),
 path('subjectforstudent', views.SubjectForStudents.as_view({'get': 'list'}),
             name='subject_passed_get_stduents'),
 path('hallticket/', views.StudentHallTicketViewset.as_view({'post': 'create'}), name='hallticket'),
 path('exam_exam/',views.YearExamminationViewSet.as_view({'get': 'list','post': 'create'}))
            
]