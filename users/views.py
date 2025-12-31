from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login, get_user_model, authenticate
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

User = get_user_model()

@method_decorator(sensitive_post_parameters('password'), name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_form_class(self):
        from .forms import CustomAuthenticationForm  # Lazy import
        return CustomAuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['college_info'] = {
            'about_bim': 'Learn about our BIM program and campus facilities.',
            'location': 'Putalisadak, Kathmandu, Nepal'
        }
        from campus.models import Event, StudentProfile, Course  # Lazy import
        context['events'] = Event.objects.filter(date__gte=timezone.now().date()).order_by('date')[:3]
        
        # Student Counts per Semester
        from django.db.models import Count
        semester_counts = StudentProfile.objects.values('semester').annotate(count=Count('user')).order_by('semester')
        context['semester_counts'] = semester_counts
        
        # Available Seats
        context['courses'] = Course.objects.all().order_by('name')
        
        return context

    def form_valid(self, form):
        user = form.get_user()
        role = self.request.POST.get('role')
        if not role or role not in [choice[0] for choice in User.ROLE_CHOICES] or user.role != role:
            messages.error(self.request, "Selected role does not match your account or is invalid.")
            return self.form_invalid(form)
        
        # Log in the user (this clears the session)
        login(self.request, user)
        
        # Set session data AFTER login
        self.request.session['role'] = role
        messages.success(self.request, f"Logged in as {role.capitalize()}.")
        
        return redirect(self.get_success_url())

    def get_success_url(self):
        role = self.request.session.get('role')
        print(f"Role from session: {role}")
        if role == 'admin' and self.request.user.is_superuser:
            # Prevent admin login here if we want strict separation, but session role check handles redirect
            # We can enforce logout if admin tries to login here in form_valid, but plan says "Update login_view"
            # Since this is strictly "Student/Teacher Login" page now
            pass 
            
        if role == 'admin':
             messages.error(self.request, "Admins must use the Admin Login page.")
             return reverse_lazy('login')
             
        elif role == 'teacher':
            return reverse_lazy('teacher_dashboard')
        elif role == 'student':
            # return reverse_lazy('student_dashboard')
            return reverse_lazy('select_semester')
        messages.warning(self.request, "No valid role selected, redirecting to home.")
        return reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        if 'role' in request.session:
            del request.session['role']
        return super().get(request, *args, **kwargs)

def register_view(request):
    from .forms import CustomUserCreationForm  # Lazy import
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Registration successful! Please log in with your credentials.")
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Admin Login View
@method_decorator(sensitive_post_parameters('password'), name='dispatch')
class AdminLoginView(LoginView):
    template_name = 'users/admin_login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        if user.role != 'admin' and not user.is_superuser:
             messages.error(self.request, "Access Denied. Admins only.")
             return self.form_invalid(form)
             
        login(self.request, user)
        self.request.session['role'] = 'admin'
        messages.success(self.request, "Welcome, Admin.")
        return redirect('admin_dashboard')

# Student Login View
@method_decorator(sensitive_post_parameters('password'), name='dispatch')
class StudentLoginView(LoginView):
    template_name = 'users/student_login.html'
    
    def get_form_class(self):
        from .forms import CustomAuthenticationForm
        return CustomAuthenticationForm

    def get_initial(self):
        initial = super().get_initial()
        initial['role'] = 'student'
        return initial

    def form_valid(self, form):
        user = form.get_user()
        role = form.cleaned_data.get('role')
        if user.role != 'student':
             messages.error(self.request, "Access Denied. Students only.")
             return self.form_invalid(form)
             
        login(self.request, user)
        # Force session role to match user role (student)
        self.request.session['role'] = 'student' 
        messages.success(self.request, "Welcome, Student.")
        return redirect('select_semester') # Or student_dashboard

# Teacher Login View
@method_decorator(sensitive_post_parameters('password'), name='dispatch')
class TeacherLoginView(LoginView):
    template_name = 'users/teacher_login.html'

    def get_form_class(self):
        from .forms import CustomAuthenticationForm
        return CustomAuthenticationForm

    def get_initial(self):
        initial = super().get_initial()
        initial['role'] = 'teacher'
        return initial
    
    def form_valid(self, form):
        user = form.get_user()
        if user.role != 'teacher':
             messages.error(self.request, "Access Denied. Teachers only.")
             return self.form_invalid(form)
             
        login(self.request, user)
        self.request.session['role'] = 'teacher'
        messages.success(self.request, "Welcome, Teacher.")
        return redirect('teacher_dashboard')

def login_selection(request):
    return render(request, 'users/login_selection.html')

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login_selection')

# Admin-only Add User View
from campus.views import admin_required

@login_required
@admin_required
def add_user(request):
    from .forms import AddUserForm
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            
            # Send Email
            try:
                send_mail(
                    'Your ShankerDev Campus Credentials',
                    f'Hello {user.first_name},\n\nYour account has been created.\n\nRole: {user.role}\nEmail: {user.email}\nPassword: {password}\n\nPlease login and change your password.',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, f"User {user.email} created and credentials emailed.")
            except Exception as e:
                messages.warning(request, f"User created but failed to see email: {e}")
                
            return redirect('admin_dashboard')
    else:
        form = AddUserForm()
    return render(request, 'users/add_user.html', {'form': form})