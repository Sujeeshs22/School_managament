from django.urls import include, path
from . import views

urlpatterns = [
    path('student/',views.AddStudent,name='add_student'),
    path('student-subjects/', views.student_subjects_view, name='student-subjects'),
]