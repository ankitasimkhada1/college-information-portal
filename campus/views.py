from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Attendance, StudentProfile, TeacherProfile, ExamRoutine, FeeDue, Event, Assignment, TeacherAttendance, Subject, Faculty
from django.contrib.auth import get_user_model
from datetime import date
from django import forms
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

def student_required(function):
    return user_passes_test(lambda u: u.role == 'student' and u.is_authenticated)(function)

def teacher_required(function):
    return user_passes_test(lambda u: u.role == 'teacher' and u.is_authenticated)(function)

def admin_required(function):
    return user_passes_test(lambda u: u.role == 'admin' and u.is_authenticated)(function)

@login_required
@student_required
def student_dashboard(request):
    profile = StudentProfile.objects.get(user=request.user)
    attendance_percent = (profile.attended_days / profile.total_days * 100) if profile.total_days else 0
    if attendance_percent < 80:
        messages.warning(request, f"Low attendance: {attendance_percent:.1f}%. Contact your faculty.")
        send_mail(
            'Low Attendance Alert',
            f'Your attendance is {attendance_percent:.1f}%, below 80%. Contact your faculty.',
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=True,
        )
    exams = ExamRoutine.objects.all()
    fees = FeeDue.objects.filter(student=request.user)
    events = Event.objects.all()
    assignments = Assignment.objects.filter(semester=profile.semester)
    subjects = Subject.objects.filter(semester=profile.semester, faculty=profile.faculty)
    teachers_present = TeacherAttendance.objects.filter(date=date.today(), present=True)
    return render(request, 'campus/student_dashboard.html', {
        'attendance_percent': attendance_percent,
        'exams': exams,
        'fees': fees,
        'events': events,
        'assignments': assignments,
        'subjects': subjects,
        'teachers_present': teachers_present,
    })

@login_required
@teacher_required
def teacher_dashboard(request):
    subjects = request.user.teacherprofile.subjects.all()
    return render(request, 'campus/teacher_dashboard.html', {'subjects': subjects})

@login_required
@teacher_required
def mark_attendance(request):
    if request.method == 'POST':
        students = request.POST.getlist('students')
        for student_id in students:
            student = User.objects.get(id=student_id)
            Attendance.objects.update_or_create(
                student=student,
                date=date.today(),
                defaults={'present': True, 'teacher': request.user}
            )
            profile = StudentProfile.objects.get(user=student)
            profile.attended_days += 1
            profile.total_days += 1
            profile.save()
        messages.success(request, 'Attendance marked successfully.')
        return redirect('teacher_dashboard')
    students = User.objects.filter(role='student')
    return render(request, 'campus/mark_attendance.html', {'students': students})

@login_required
@teacher_required
def mark_teacher_attendance(request):
    if request.method == 'POST':
        present = request.POST.get('present') == 'on'
        TeacherAttendance.objects.update_or_create(
            teacher=request.user,
            date=date.today(),
            defaults={'present': present}
        )
        messages.success(request, 'Attendance marked.')
        return redirect('teacher_dashboard')
    return render(request, 'campus/mark_teacher_attendance.html')

@login_required
@teacher_required
def add_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = request.user
            assignment.save()
            messages.success(request, 'Assignment added successfully.')
            return redirect('teacher_dashboard')
    else:
        form = AssignmentForm()
    return render(request, 'campus/add_assignment.html', {'form': form})

@login_required
@admin_required
def admin_dashboard(request):
    return render(request, 'campus/admin_dashboard.html')

@login_required
@admin_required
def manage_courses(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course managed successfully.')
            return redirect('admin_dashboard')
    else:
        form = CourseForm()
    return render(request, 'campus/manage_courses.html', {'form': form})

@login_required
@admin_required
def set_exam_dates(request):
    if request.method == 'POST':
        form = ExamRoutineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam dates set successfully.')
            return redirect('admin_dashboard')
    else:
        form = ExamRoutineForm()
    return render(request, 'campus/set_exam_dates.html', {'form': form})

@login_required
@admin_required
def send_notifications(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipients = form.cleaned_data['recipients']
            for user in recipients:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=True,
                )
            messages.success(request, 'Notifications sent successfully.')
            return redirect('admin_dashboard')
    else:
        form = NotificationForm()
    return render(request, 'campus/send_notifications.html', {'form': form})

@login_required
@admin_required
def update_seats(request):
    if request.method == 'POST':
        form = UpdateSeatsForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            course.available_seats = form.cleaned_data['available_seats']
            course.save()
            messages.success(request, 'Seats updated successfully.')
            return redirect('admin_dashboard')
    else:
        form = UpdateSeatsForm()
    return render(request, 'campus/update_seats.html', {'form': form})

@login_required
@admin_required
def post_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event posted successfully.')
            return redirect('admin_dashboard')
    else:
        form = EventForm()
    return render(request, 'campus/post_event.html', {'form': form})

@login_required
@admin_required
def alert_fee_dues(request):
    if request.method == 'POST':
        form = FeeDueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee due alert sent successfully.')
            return redirect('admin_dashboard')
    else:
        form = FeeDueForm()
    return render(request, 'campus/alert_fee_dues.html', {'form': form})