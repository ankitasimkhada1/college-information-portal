# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required, user_passes_test
# from django.contrib import messages
# from .forms import AssignmentForm, CourseForm, EventForm, ExamRoutineForm, FeeDueForm, NotificationForm, UpdateSeatsForm
# from .models import Attendance, StudentProfile, TeacherProfile, ExamRoutine, FeeDue, Event, Assignment, TeacherAttendance, Subject, Faculty
# from django.contrib.auth import get_user_model
# from datetime import date
# from django.core.mail import send_mail
# from django.conf import settings

# User = get_user_model()

# def student_required(function):
#     return user_passes_test(lambda u: u.role == 'student' and u.is_authenticated)(function)

# def teacher_required(function):
#     return user_passes_test(lambda u: u.role == 'teacher' and u.is_authenticated)(function)

# def admin_required(function):
#     return user_passes_test(lambda u: u.role == 'admin' and u.is_authenticated)(function)

# @login_required
# @student_required
# def student_dashboard(request):
#     profile = StudentProfile.objects.get(user=request.user)
#     attendance_percent = (profile.attended_days / profile.total_days * 100) if profile.total_days else 0
#     if attendance_percent < 80:
#         messages.warning(request, f"Low attendance: {attendance_percent:.1f}%. Contact your faculty.")
#         send_mail(
#             'Low Attendance Alert',
#             f'Your attendance is {attendance_percent:.1f}%, below 80%. Contact your faculty.',
#             settings.EMAIL_HOST_USER,
#             [request.user.email],
#             fail_silently=True,
#         )
#     exams = ExamRoutine.objects.filter(date__gte=date.today())
#     fees = FeeDue.objects.filter(student=request.user, due_date__gte=date.today())
#     events = Event.objects.filter(date__gte=date.today())
#     assignments = Assignment.objects.filter(semester=profile.semester, due_date__gte=date.today())
#     subjects = Subject.objects.filter(semester=profile.semester, faculty=profile.faculty)
#     teachers_present = TeacherAttendance.objects.filter(date=date.today(), present=True)
#     return render(request, 'campus/student_dashboard.html', {
#         'attendance_percent': attendance_percent,
#         'exams': exams,
#         'fees': fees,
#         'events': events,
#         'assignments': assignments,
#         'subjects': subjects,
#         'teachers_present': teachers_present,
#     })

# @login_required
# @teacher_required
# def teacher_dashboard(request):
#     subjects = request.user.teacherprofile.subjects.all()
#     assignments = Assignment.objects.filter(teacher=request.user)
#     return render(request, 'campus/teacher_dashboard.html', {
#         'subjects': subjects,
#         'assignments': assignments,
#     })

# @login_required
# @teacher_required
# def mark_attendance(request):
#     if request.method == 'POST':
#         students = request.POST.getlist('students')
#         for student_id in students:
#             student = User.objects.get(id=student_id)
#             present = student_id in request.POST.getlist('present_students', [])  # Check if marked present
#             Attendance.objects.update_or_create(
#                 student=student,
#                 teacher=request.user,
#                 date=date.today(),
#                 defaults={'present': present}
#             )
#             profile = StudentProfile.objects.get(user=student)
#             if present:
#                 profile.attended_days += 1
#             profile.total_days += 1
#             profile.save()
#         messages.success(request, 'Attendance marked successfully.')
#         return redirect('teacher_dashboard')
#     students = User.objects.filter(role='student')
#     return render(request, 'campus/mark_attendance.html', {'students': students})

# @login_required
# @teacher_required
# def mark_teacher_attendance(request):
#     if request.method == 'POST':
#         present = request.POST.get('present') == 'on'
#         TeacherAttendance.objects.update_or_create(
#             teacher=request.user,
#             date=date.today(),
#             defaults={'present': present}
#         )
#         messages.success(request, 'Attendance marked.')
#         return redirect('teacher_dashboard')
#     return render(request, 'campus/mark_teacher_attendance.html')

# @login_required
# @teacher_required
# def add_assignment(request):
#     if request.method == 'POST':
#         form = AssignmentForm(request.POST)
#         if form.is_valid():
#             assignment = form.save(commit=False)
#             assignment.teacher = request.user
#             assignment.save()
#             messages.success(request, 'Assignment added successfully.')
#             return redirect('teacher_dashboard')
#         else:
#             for error in form.errors.values():
#                 messages.error(request, error)
#     else:
#         form = AssignmentForm()
#     return render(request, 'campus/add_assignment.html', {'form': form})

# @login_required
# @admin_required
# def admin_dashboard(request):
#     courses = CourseForm().fields['course'].queryset  # Assuming Course model exists
#     events = Event.objects.all()
#     return render(request, 'campus/admin_dashboard.html', {
#         'courses': courses,
#         'events': events,
#     })

# @login_required
# @admin_required
# def manage_courses(request):
#     if request.method == 'POST':
#         form = CourseForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Course managed successfully.')
#             return redirect('admin_dashboard')
#         else:
#             for error in form.errors.values():
#                 messages.error(request, error)
#     else:
#         form = CourseForm()
#     return render(request, 'campus/manage_courses.html', {'form': form})

# @login_required
# @admin_required
# def set_exam_dates(request):
#     if request.method == 'POST':
#         form = ExamRoutineForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Exam dates set successfully.')
#             return redirect('admin_dashboard')
#         else:
#             for error in form.errors.values():
#                 messages.error(request, error)
#     else:
#         form = ExamRoutineForm()
#     return render(request, 'campus/set_exam_dates.html', {'form': form})

# @login_required
# @admin_required
# def send_notifications(request):
#     if request.method == 'POST':
#         form = NotificationForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             message = form.cleaned_data['message']
#             recipients = form.cleaned_data['recipients']
#             for user in recipients:
#                 send_mail(
#                     subject,
#                     message,
#                     settings.EMAIL_HOST_USER,
#                     [user.email],
#                     fail_silently=True,
#                 )
#             messages.success(request, 'Notifications sent successfully.')
#             return redirect('admin_dashboard')
#         else:
#             for error in form.errors.values():
#                 messages.error(request, error)
#     else:
#         form = NotificationForm()
#     return render(request, 'campus/send_notifications.html', {'form': form})

# @login_required
# @admin_required
# def update_seats(request):
#     if request.method == 'POST':
#         form = UpdateSeatsForm(request.POST)
#         if form.is_valid():
#             course = form.cleaned_data['course']
#             course.available_seats = form.cleaned_data['available_seats']
#             course.save()
#             messages.success(request, 'Seats updated successfully.')
#             return redirect('admin_dashboard')
#         else:
#             for error in form.errors.values():
#                 messages.error(request, error)
#     else:
#         form = UpdateSeatsForm()
#     return render(request, 'campus/update_seats.html', {'form': form})

# @login_required
# @admin_required
# def post_event(request):
#     if request.method == 'POST':
#         form = EventForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Event posted successfully.')
#             return redirect('admin_dashboard')
#         else:
#             for error in form.errors.values():
#                 messages.error(request, error)
#     else:
#         form = EventForm()
#     return render(request, 'campus/post_event.html', {'form': form})

# @login_required
# @admin_required
# def alert_fee_dues(request):
#     if request.method == 'POST':
#         form = FeeDueForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Fee due alert sent successfully.')
#             return redirect('admin_dashboard')
#         else:
#             for error in form.errors.values():
#                 messages.error(request, error)
#     else:
#         form = FeeDueForm()
#     return render(request, 'campus/alert_fee_dues.html', {'form': form})

# # Add the missing bim_course_details view
# @login_required
# def bim_course_details(request):
#     # Assuming a Course model exists; fetch BIM course details
#     from .models import Course  # Lazy import
#     bim_course = Course.objects.filter(name__icontains='bim').first()  # Adjust query as needed
#     context = {
#         'course_info': {
#             'title': bim_course.name if bim_course else 'Bachelor in Information Management (BIM)',
#             'description': bim_course.description if bim_course else 'A 4-year program focusing on IT and management skills.',
#             'duration': bim_course.duration if bim_course else '4 years',
#             'location': bim_course.location if bim_course else 'Putalisadak, Kathmandu, Nepal'
#         }
#     }
#     return render(request, 'campus/bim_course_details.html', context)

# @login_required
# @admin_required
# def view_attendance(request, role=None):
#     if role:
#         attendees = User.objects.filter(role=role)
#     else:
#         attendees = User.objects.filter(role='student')  # Default to students
#     attendance_records = Attendance.objects.filter(
#         student__in=attendees, date__gte=date.today().replace(day=1)  # Last 30 days
#     ).order_by('date')
#     return render(request, 'campus/view_attendance.html', {'attendance_records': attendance_records})




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import AssignmentForm, CourseForm, EventForm, ExamRoutineForm, FeeDueForm, NotificationForm, UpdateSeatsForm
from .models import Attendance, Course, StudentProfile, TeacherProfile, ExamRoutine, FeeDue, Event, Assignment, TeacherAttendance, Subject, Faculty
from django.contrib.auth import get_user_model
from datetime import date
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
    try:
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
    except StudentProfile.DoesNotExist:
        messages.error(request, "Your student profile is not set up. Contact an admin.")
        attendance_percent = 0
    exams = ExamRoutine.objects.filter(date__gte=date.today()).order_by('date')
    fees = FeeDue.objects.filter(student=request.user, due_date__gte=date.today()).order_by('due_date')
    events = Event.objects.filter(date__gte=date.today()).order_by('date')
    assignments = Assignment.objects.filter(semester=profile.semester, due_date__gte=date.today()).order_by('due_date')
    subjects = Subject.objects.filter(semester=profile.semester, faculty=profile.faculty).order_by('name')
    teachers_present = TeacherAttendance.objects.filter(date=date.today(), present=True).order_by('teacher__email')
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
    try:
        subjects = request.user.teacherprofile.subjects.all().order_by('name')
        assignments = Assignment.objects.filter(teacher=request.user).order_by('due_date')
    except TeacherProfile.DoesNotExist:
        messages.error(request, "Your teacher profile is not set up. Contact an admin.")
        subjects = []
        assignments = []
    return render(request, 'campus/teacher_dashboard.html', {
        'subjects': subjects,
        'assignments': assignments,
    })
@login_required
@teacher_required
def mark_attendance(request):
    if request.method == 'POST':
        students = request.POST.getlist('students')
        if not students:
            messages.error(request, "No students selected.")
            return redirect('mark_attendance')
        try:
            for student_id in students:
                student = User.objects.get(id=student_id)
                present = student_id in request.POST.getlist('present_students', [])
                Attendance.objects.update_or_create(
                    student=student,
                    teacher=request.user,
                    date=date.today(),
                    defaults={'present': present}
                )
                profile = StudentProfile.objects.get(user=student)
                if present:
                    profile.attended_days += 1
                profile.total_days += 1
                profile.save()
            messages.success(request, 'Attendance marked successfully.')
        except (User.DoesNotExist, StudentProfile.DoesNotExist) as e:
            messages.error(request, f"Error marking attendance: {str(e)}")
        return redirect('teacher_dashboard')
    students = User.objects.filter(role='student').order_by('email')
 
    return render(request, 'campus/mark_attendance.html', {'students': students})
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'teacher_dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'campus/login.html', {'next': request.GET.get('next')})
# @login_required
# @teacher_required
# def mark_attendance(request):
#     if request.method == 'POST':
#         students = request.POST.getlist('students')
#         if not students:
#             messages.error(request, "No students selected.")
#             return redirect('mark_attendance')
#         try:
#             for student_id in students:
#                 student = User.objects.get(id=student_id)
#                 present = student_id in request.POST.getlist('present_students', [])
#                 Attendance.objects.update_or_create(
#                     student=student,
#                     teacher=request.user,
#                     date=date.today(),
#                     defaults={'present': present}
#                 )
#                 profile = StudentProfile.objects.get(user=student)
#                 if present:
#                     profile.attended_days += 1
#                 profile.total_days += 1
#                 profile.save()
#             messages.success(request, 'Attendance marked successfully.')
#         except (User.DoesNotExist, StudentProfile.DoesNotExist) as e:
#             messages.error(request, f"Error marking attendance: {str(e)}")
#         return redirect('teacher_dashboard')
#     students = User.objects.filter(role='student').order_by('email')
#     return render(request, 'campus/mark_attendance.html', {'students': students})

@login_required
@teacher_required
def mark_teacher_attendance(request):
    if request.method == 'POST':
        try:
            present = request.POST.get('present') == 'on'
            TeacherAttendance.objects.update_or_create(
                teacher=request.user,
                date=date.today(),
                defaults={'present': present}
            )
            messages.success(request, 'Attendance marked.')
        except Exception as e:
            messages.error(request, f"Error marking attendance: {str(e)}")
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
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = AssignmentForm()
    return render(request, 'campus/add_assignment.html', {'form': form})

@login_required
@admin_required
def admin_dashboard(request):
    try:
        courses = Course.objects.all().order_by('name')  # Use model directly for consistency
    except Exception:
        courses = []
        messages.error(request, "Could not load courses. Check database.")
    events = Event.objects.all().order_by('date')
    return render(request, 'campus/admin_dashboard.html', {
        'courses': courses,
        'events': events,
    })

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
            for error in form.errors.values():
                messages.error(request, error)
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
            for error in form.errors.values():
                messages.error(request, error)
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
            for error in form.errors.values():
                messages.error(request, error)
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
            for error in form.errors.values():
                messages.error(request, error)
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
            for error in form.errors.values():
                messages.error(request, error)
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
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = FeeDueForm()
    return render(request, 'campus/alert_fee_dues.html', {'form': form})

# @login_required
# def bim_course_details(request):
#     try:
#         from .models import Course  # Lazy import to avoid circular issues
#         bim_course = Course.objects.filter(name__icontains='bim').first()
#         context = {
#             'course_info': {
#                 'title': bim_course.name if bim_course else 'Bachelor in Information Management (BIM)',
#                 'description': bim_course.description if bim_course else 'A 4-year program focusing on IT and management skills.',
#                 'duration': bim_course.duration if bim_course else '4 years',
#                 'location': bim_course.location if bim_course else 'Putalisadak, Kathmandu, Nepal'
#             }
#         }
#     except Exception as e:
#         messages.error(request, f"Error loading course details: {str(e)}")
#         context = {
#             'course_info': {
#                 'title': 'Bachelor in Information Management (BIM)',
#                 'description': 'A 4-year program focusing on IT and management skills.',
#                 'duration': '4 years',
#                 'location': 'Putalisadak, Kathmandu, Nepal'
#             }
#         }
#     return render(request, 'campus/bim_course_details.html', context)
@login_required
def bim_course_details(request):
    try:
        # Use exact match for BIM course or case-insensitive search
        bim_course = Course.objects.filter(name__iexact='BIM').first()
        if not bim_course:
            bim_course = Course.objects.filter(name__icontains='bim').first()
        context = {
            'course_info': {
                'title': bim_course.name if bim_course else 'Bachelor in Information Management (BIM)',
                'description': bim_course.description if bim_course else 'A 4-year program focusing on IT and management skills.',
                'duration': bim_course.duration if bim_course else '4 years',
                'location': bim_course.location if bim_course else 'Putalisadak, Kathmandu, Nepal',
                'additional_info': getattr(bim_course, 'additional_info', ''),  # Add more fields if available
            }
        }
    except Course.DoesNotExist:
        messages.warning(request, "BIM course not found in the database.")
        context = {
            'course_info': {
                'title': 'Bachelor in Information Management (BIM)',
                'description': 'A 4-year program focusing on IT and management skills.',
                'duration': '4 years',
                'location': 'Putalisadak, Kathmandu, Nepal',
                'additional_info': '',
            }
        }
    except Exception as e:
        messages.error(request, f"Error loading course details: {str(e)}")
        context = {
            'course_info': {
                'title': 'Bachelor in Information Management (BIM)',
                'description': 'A 4-year program focusing on IT and management skills.',
                'duration': '4 years',
                'location': 'Putalisadak, Kathmandu, Nepal',
                'additional_info': '',
            }
        }
    return render(request, 'campus/bim_course_details.html', context)

@login_required
@admin_required
def view_attendance(request, role=None):
    try:
        if role:
            attendees = User.objects.filter(role=role)
        else:
            attendees = User.objects.filter(role='student')
        attendance_records = Attendance.objects.filter(
            student__in=attendees, date__gte=date.today().replace(day=1)
        ).order_by('date')
    except Exception as e:
        messages.error(request, f"Error loading attendance: {str(e)}")
        attendance_records = []
    return render(request, 'campus/view_attendance.html', {'attendance_records': attendance_records})