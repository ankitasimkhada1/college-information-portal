"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, home_view, register_view, student_dashboard, teacher_dashboard, admin_dashboard, bim_course_details
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    path('', RedirectView.as_view(url='/login/'), name='home'),  # Redirect root to login
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),  # Removed duplicate
    path('register/', register_view, name='register'),
    path('student-dashboard/', student_dashboard, name='student_dashboard'),
    path('teacher-dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('bim-course-details/', bim_course_details, name='bim_course_details'),
    path('campus/', include('campus.urls')),
    path('', home_view, name='home'),
]