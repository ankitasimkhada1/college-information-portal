

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Attendance  # Adjust import based on model location
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

def teacher_required(function):
    return user_passes_test(lambda u: u.role == 'teacher' and u.is_authenticated)(function)

@login_required
@teacher_required
def mark_attendance(request):
    if request.method == 'POST':
        students = request.POST.getlist('students')
        for student_id in students:
            student = User.objects.get(id=student_id)
            present = student_id in request.POST.getlist('present_students', [])
            Attendance.objects.update_or_create(
                student=student,
                teacher=request.user,
                date=date.today(),
                defaults={'present': present}
            )
            # Update StudentProfile if it exists (adjust logic as needed)
        messages.success(request, 'Attendance marked successfully.')
        return redirect('attendance:teacher_dashboard')  # Adjust redirect
    students = User.objects.filter(role='student')
    return render(request, 'attendance/mark_attendance.html', {'students': students})

@login_required
@teacher_required
def mark_teacher_attendance(request):
    if request.method == 'POST':
        present = request.POST.get('present') == 'on'
        # Assuming TeacherAttendance model exists
        from .models import TeacherAttendance
        TeacherAttendance.objects.update_or_create(
            teacher=request.user,
            date=date.today(),
            defaults={'present': present}
        )
        messages.success(request, 'Attendance marked.')
        return redirect('attendance:teacher_dashboard')  # Adjust redirect
    return render(request, 'attendance/mark_teacher_attendance.html')

@login_required
def view_attendance(request, role=None):
    if role:
        attendees = User.objects.filter(role=role)
    else:
        attendees = User.objects.filter(role='student')
    attendance_records = Attendance.objects.filter(
        student__in=attendees, date__gte=date.today().replace(day=1)
    ).order_by('date')
    return render(request, 'attendance/view_attendance.html', {'attendance_records': attendance_records})