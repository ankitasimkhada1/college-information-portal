
# from django.db import models
# from users.models import CustomUser

# class Faculty(models.Model):
#     name = models.CharField(max_length=100)

# class Subject(models.Model):
#     name = models.CharField(max_length=100)
#     faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
#     semester = models.IntegerField()

# class StudentProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
#     semester = models.IntegerField(default=1)
#     attended_days = models.IntegerField(default=0)
#     total_days = models.IntegerField(default=0)  # For attendance percentage

# class TeacherProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     subjects = models.ManyToManyField(Subject)

# class Attendance(models.Model):
#     student = models.ForeignKey(CustomUser, related_name='student_attendance', on_delete=models.CASCADE)
#     date = models.DateField(auto_now_add=True)
#     present = models.BooleanField(default=False)
#     teacher = models.ForeignKey(CustomUser, related_name='marked_by', on_delete=models.SET_NULL, null=True)

# # campus/models.py
# class TeacherAttendance(models.Model):
#     teacher = models.ForeignKey(
#         CustomUser,
#         on_delete=models.CASCADE,
#         limit_choices_to={'role': 'teacher'},
#         related_name='campus_teacher_records'
#     )
#     date = models.DateField(auto_now_add=True)
#     present = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.teacher.email} - {self.date}"
    
# class Assignment(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     due_date = models.DateField()
#     semester = models.IntegerField()

# class Submission(models.Model):
#     assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
#     student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     file = models.FileField(upload_to='submissions/')
#     submitted_at = models.DateTimeField(auto_now_add=True)

# class ExamRoutine(models.Model):
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     date = models.DateField()
#     details = models.TextField()

# class FeeDue(models.Model):
#     student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     due_date = models.DateField()

# class Event(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     date = models.DateField()
#     type = models.CharField(max_length=50)  # e.g., tournament

# class Project(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()

# class ContactMessage(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     message = models.TextField()
#     submitted_at = models.DateTimeField(auto_now_add=True)

# class Testimonial(models.Model):  # Optional bonus
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     content = models.TextField()
    
# class CollegeInfo(models.Model):
#     about_bim = models.TextField(default="ShankerDev Campus offers a Bachelor in Information Management (BIM) program.")
#     location = models.CharField(max_length=100, default="Kathmandu, Nepal")

from django.db import models
from users.models import CustomUser
from django.core.exceptions import ValidationError

class Faculty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    semester = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} (Sem {self.semester})"

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    semester = models.PositiveIntegerField(default=1)
    attended_days = models.PositiveIntegerField(default=0)
    total_days = models.PositiveIntegerField(default=0)  # For attendance percentage
    current_subjects = models.ManyToManyField(Subject, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.faculty}"

class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.user.username

class Attendance(models.Model):
    student = models.ForeignKey(CustomUser, related_name='student_attendance', on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    teacher = models.ForeignKey(CustomUser, related_name='teacher_attendance', on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    date = models.DateField(auto_now_add=True)
    present = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.email} - {self.date} ({'Present' if self.present else 'Absent'})"

class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        related_name='campus_teacher_records'
    )
    date = models.DateField()  # Allow manual date entry
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.teacher.email} - {self.date}"

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    due_date = models.DateField()
    semester = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"

class ExamRoutine(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    details = models.TextField()

    def __str__(self):
        return f"{self.subject.name} - {self.date}"

class FeeDue(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - NPR {self.amount}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    type = models.CharField(max_length=50, choices=[('event', 'Event'), ('tournament', 'Tournament'), ('program', 'Program')])

    def __str__(self):
        return self.title

class Course(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    available_seats = models.PositiveIntegerField(default=50)
    description = models.CharField(max_length=500)
    duration = models.CharField(max_length=50)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

class Testimonial(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()

class CollegeInfo(models.Model):
    about_bim = models.TextField(default="ShankerDev Campus offers a Bachelor in Information Management (BIM) program.")
    location = models.CharField(max_length=100, default="Kathmandu, Nepal")
    
    
