
from django.urls import path
from django.urls import path
from .views import CustomLoginView, AdminLoginView, StudentLoginView, TeacherLoginView, add_user, login_selection

urlpatterns = [
    # path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'), # Fallback/Legacy
    path('admin-login/', AdminLoginView.as_view(), name='admin_login'),
    path('student-login/', StudentLoginView.as_view(), name='student_login'),
    path('teacher-login/', TeacherLoginView.as_view(), name='teacher_login'),
    path('login-selection/', login_selection, name='login_selection'),
    path('add-user/', add_user, name='add_user'),
]