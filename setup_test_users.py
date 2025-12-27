import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth import get_user_model
from campus.models import StudentProfile, TeacherProfile, Faculty, Subject

User = get_user_model()

def create_users():
    print("Creating test users...")

    # Create Faculty
    faculty, _ = Faculty.objects.get_or_create(name='Management')
    
    # Create Subject
    subject, _ = Subject.objects.get_or_create(name='Principles of Management', faculty=faculty, semester=1)

    # Create Student
    student_email = 'garimanepal@gmail.com'
    if not User.objects.filter(email=student_email).exists():
        student = User.objects.create_user(
            email=student_email,
            password='garima123',
            role='student'
        )
        StudentProfile.objects.create(user=student, faculty=faculty, semester=1)
        print(f"Created Student: {student_email} / garima123")
    else:
        student = User.objects.get(email=student_email)
        student.set_password('garima123')
        student.save()
        print(f"Updated Student: {student_email} / garima123")

    # Create Teacher
    teacher_email = 'teacher@gmail.com'
    if not User.objects.filter(email=teacher_email).exists():
        teacher = User.objects.create_user(
            email=teacher_email,
            password='teacher123',
            role='teacher'
        )
        profile = TeacherProfile.objects.create(user=teacher)
        profile.subjects.add(subject)
        print(f"Created Teacher: {teacher_email} / teacher123")
    else:
        teacher = User.objects.get(email=teacher_email)
        teacher.set_password('teacher123')
        teacher.save()
        print(f"Updated Teacher: {teacher_email} / teacher123")

    # Create Admin
    admin_email = 'apekshyasimkhada@gmail.com'
    if not User.objects.filter(email=admin_email).exists():
        User.objects.create_superuser(
            email=admin_email,
            password='apekshya07',
            role='admin'
        )
        print(f"Created Admin: {admin_email} / apekshya07")
    else:
        admin = User.objects.get(email=admin_email)
        admin.set_password('apekshya07')
        admin.save()
        print(f"Updated Admin: {admin_email} / apekshya07")

if __name__ == '__main__':
    create_users()
