

# from urllib import request
# from django.shortcuts import render, redirect
# from django.contrib.auth.views import LoginView
# from django.urls import reverse_lazy
# from django.contrib.auth import login, get_user_model
# from django.contrib import messages
# from django.utils import timezone

# User = get_user_model()

# class CustomLoginView(LoginView):
#     template_name = 'registration/login.html'

#     def get_form_class(self):
#         from .forms import CustomAuthenticationForm  # Lazy import
#         return CustomAuthenticationForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['college_info'] = {
#             'about_bim': 'Learn about our BIM program and campus facilities.',
#             'location': 'Putalisadak, Kathmandu, Nepal'
#         }
#         from campus.models import Event  # Lazy import
#         context['events'] = Event.objects.filter(date__gte=timezone.now().date())[:3]
#         return context

#     def form_valid(self, form):
#         user = form.get_user()
#         role = self.request.POST.get('role')
#         if role and role in [choice[0] for choice in User.ROLE_CHOICES] and user.role == role:
#             self.request.session['role'] = role
#             messages.success(request, f"Logged in as {role.capitalize()}.")
#         else:
#             messages.error(request, "Selected role does not match your account or is invalid.")
#             return self.form_invalid(form)
#         return super().form_valid(form)

#     def get_success_url(self):
#         role = self.request.session.get('role')
#         print(f"Role from session: {role}")
#         if role == 'admin' and self.request.user.is_superuser:
#             return reverse_lazy('admin_dashboard')
#         elif role == 'teacher':
#             return reverse_lazy('teacher_dashboard')
#         elif role == 'student':
#             return reverse_lazy('student_dashboard')
#         messages.warning(request, "No valid role selected, redirecting to home.")
#         return reverse_lazy('home')

#     def get(self, request, *args, **kwargs):
#         if 'role' in request.session:
#             del request.session['role']
#         return super().get(request, *args, **kwargs)

# def register_view(request):
#     from .forms import CustomUserCreationForm  # Lazy import
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             messages.success(request, f"Registration successful! Please log in with your credentials.")
#             return redirect('login')
#         else:
#             for error in form.errors.values():
#                 messages.error(request, error)
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from django.utils import timezone

User = get_user_model()

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
        from campus.models import Event  # Lazy import
        context['events'] = Event.objects.filter(date__gte=timezone.now().date())[:3]
        return context

    def form_valid(self, form):
        user = form.get_user()
        role = self.request.POST.get('role')
        if role and role in [choice[0] for choice in User.ROLE_CHOICES] and user.role == role:
            self.request.session['role'] = role
            messages.success(self.request, f"Logged in as {role.capitalize()}.")
        else:
            messages.error(self.request, "Selected role does not match your account or is invalid.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        role = self.request.session.get('role')
        print(f"Role from session: {role}")
        if role == 'admin' and self.request.user.is_superuser:
            return reverse_lazy('admin_dashboard')
        elif role == 'teacher':
            return reverse_lazy('teacher_dashboard')
        elif role == 'student':
            return reverse_lazy('student_dashboard')
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