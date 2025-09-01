from django.urls import path
from .views import student_dashboard, teacher_dashboard, mark_attendance, mark_teacher_attendance, add_assignment, admin_dashboard, manage_courses, set_exam_dates, send_notifications, update_seats, post_event, alert_fee_dues

urlpatterns = [
    path('student/', student_dashboard, name='student_dashboard'),
    path('teacher/', teacher_dashboard, name='teacher_dashboard'),
    path('teacher/attendance/', mark_attendance, name='mark_attendance'),
    path('teacher/teacher_attendance/', mark_teacher_attendance, name='mark_teacher_attendance'),
    path('teacher/add_assignment/', add_assignment, name='add_assignment'),
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('admin/manage_courses/', manage_courses, name='manage_courses'),
    path('admin/set_exam_dates/', set_exam_dates, name='set_exam_dates'),
    path('admin/send_notifications/', send_notifications, name='send_notifications'),
    path('admin/update_seats/', update_seats, name='update_seats'),
    path('admin/post_event/', post_event, name='post_event'),
    path('admin/alert_fee_dues/', alert_fee_dues, name='alert_fee_dues'),
]