# from django import views
# from django.urls import path
# from .views import student_dashboard, teacher_dashboard, mark_attendance, mark_teacher_attendance, add_assignment, admin_dashboard, manage_courses, set_exam_dates, send_notifications, update_seats, post_event, alert_fee_dues

# urlpatterns = [
#     #student and teacher dashboard
#     path('student/', student_dashboard, name='student_dashboard'),
#     path('teacher/', teacher_dashboard, name='teacher_dashboard'),
    
#     #attendance-related
#     path('teacher/attendance/', mark_attendance, name='mark_attendance'),
#     path('teacher/teacher_attendance/', mark_teacher_attendance, name='mark_teacher_attendance'),
#     path('teacher/add_assignment/', add_assignment, name='add_assignment'),
 
#   #admin dashboard and management
#     path('admin/', admin_dashboard, name='admin_dashboard'),
#     path('admin/manage_courses/', manage_courses, name='manage_courses'),
#     path('admin/set_exam_dates/', set_exam_dates, name='set_exam_dates'),
#     path('admin/send_notifications/', send_notifications, name='send_notifications'),
#     path('admin/update_seats/', update_seats, name='update_seats'),
#     path('admin/post_event/', post_event, name='post_event'),
#     path('admin/alert_fee_dues/', alert_fee_dues, name='alert_fee_dues'),
   
#     # Attendance-related paths
#     path('mark/', views.mark_attendance, name='mark_attendance'),
#     path('teacher/mark/', views.mark_teacher_attendance, name='mark_teacher_attendance'),
#     path('view/', views.view_attendance, name='view_attendance', kwargs={'role': 'student'}),
#     path('view/<str:role>/', views.view_attendance, name='view_attendance_by_role'),
   
#     # Existing campus paths
#     path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
#     path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
#     path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
#     path('bim-course-details/', views.bim_course_details, name='bim_course_details'),
#     # Add other paths as needed (e.g., manage_courses, set_exam_dates)
#     path('manage-courses/', views.manage_courses, name='manage_courses'),
#     path('set-exam-dates/', views.set_exam_dates, name='set_exam_dates'),
#     path('send-notifications/', views.send_notifications, name='send_notifications'),
#     path('update-seats/', views.update_seats, name='update_seats'),
#     path('post-event/', views.post_event, name='post_event'),
#     path('alert-fee-dues/', views.alert_fee_dues, name='alert_fee_dues'),
#     path('add-assignment/', views.add_assignment, name='add_assignment'),


# ]



from django.urls import path
from .views import login_view, student_dashboard, teacher_dashboard, mark_attendance, mark_teacher_attendance, add_assignment, admin_dashboard, manage_courses, set_exam_dates, send_notifications, update_seats, post_event, alert_fee_dues, view_attendance, bim_course_details

urlpatterns = [
    # Student and Teacher Dashboards
    path('student/', student_dashboard, name='student_dashboard'),
    path('teacher/', teacher_dashboard, name='teacher_dashboard'),
    
    # Attendance-related paths
    path('teacher/attendance/', mark_attendance, name='mark_attendance'),
    path('teacher/teacher_attendance/', mark_teacher_attendance, name='mark_teacher_attendance'),
    path('view/', view_attendance, name='view_attendance', kwargs={'role': 'student'}),
    path('view/<str:role>/', view_attendance, name='view_attendance_by_role'),
    
    # Teacher-specific
    path('teacher/add_assignment/', add_assignment, name='add_assignment'),
    
    # Admin Dashboards and Management
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('admin/manage_courses/', manage_courses, name='manage_courses'),
    path('admin/set_exam_dates/', set_exam_dates, name='set_exam_dates'),
    path('admin/send_notifications/', send_notifications, name='send_notifications'),
    path('admin/update_seats/', update_seats, name='update_seats'),
    path('admin/post_event/', post_event, name='post_event'),
    path('admin/alert_fee_dues/', alert_fee_dues, name='alert_fee_dues'),
    path('login/', login_view, name='login'),
    # Additional Paths
    path('bim-course-details/', bim_course_details, name='bim_course_details'),
]