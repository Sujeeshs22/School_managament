from django.db import models

class Teacher_admin(models.Model):
    full_name = models.TextField(blank=True, null=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.full_name

class Subjects(models.Model):
    sub_name = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False, help_text='Is subject active')

    def __str__(self):
        return self.sub_name

class StudentSubjects(models.Model):
    student = models.ForeignKey('student.Student', related_name='student_admin', on_delete=models.CASCADE)
    subject = models.ForeignKey('school_admin.Subjects', related_name='student_sub', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.admin_teacher} - {self.student} - {self.subject}"



class HallTicketForStudent(models.Model):
    student = models.ForeignKey('student.Student', related_name='student_hall_tickt', on_delete=models.CASCADE)
    is_issued = models.BooleanField(default=False)
    hallticket_for_stud = models.CharField(max_length=5,null=True, blank= True)
    is_active = models.BooleanField(default= True)

    def generate_hallticket(self):
        """
        This method generates a new hall ticket ID if 'is_issued' is True.
        Format is 'XR' followed by a 3-digit number starting from 100.
        """
        if self.is_issued:
            # Get the latest hall ticket number (if any) and increment it
            last_hallticket = HallTicketForStudent.objects.filter(hallticket_for_stud__startswith="XR").order_by('hallticket_for_stud').last()
            if last_hallticket:
                last_ticket_number = int(last_hallticket.hallticket_for_stud[2:])  # Extract the numeric part
                new_ticket_number = last_ticket_number + 1
            else:
                new_ticket_number = 100  # Start from 100 if there are no previous tickets
            return f"XR{new_ticket_number}"
        else:
            return None

    def save(self, *args, **kwargs):
        """
        Overrides the save method to compute the hall ticket when the student is issued one.
        """
        if self.is_issued and not self.hallticket_for_stud:
            self.hallticket_for_stud = self.generate_hallticket()
        elif not self.is_issued:
            self.hallticket_for_stud = None
        
        super(HallTicketForStudent, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.hallticket_for_stud}"
    

class Examination(models.Model):
    student = models.ForeignKey('student.Student', related_name='student_attended', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects,related_name='student_attended_sub', on_delete=models.CASCADE)
    hall_ticket = models.ForeignKey(HallTicketForStudent,related_name='hall_ticket_student',null= True,blank=True,on_delete=models.CASCADE)
    has_attended = models.BooleanField(default= False)
    date_attended = models.DateField(auto_now_add=True)
    # active = models.TextField(null=True,blank=True)
    active_status = models.TextField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.has_attended:
            self.active_status = 'active'
        else:
            self.active_status = 'inactive'

        return super().save(*args, **kwargs)
    
    