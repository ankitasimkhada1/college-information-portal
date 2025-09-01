from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, get_user_model
from django.contrib import messages

User = get_user_model()

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        user = form.get_user()
        role = self.request.POST.get('role')
        if role and role in [choice[0] for choice in User.ROLE_CHOICES]:
            self.request.session['role'] = role
            messages.success(self.request, f"Logged in as {role.capitalize()}.")
        else:
            messages.error(self.request, "Please select a valid role.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        role = self.request.session.get('role')
        print(f"Role from session: {role}")
        if role == 'student':
            return reverse_lazy('student_dashboard')
        elif role == 'teacher':
            return reverse_lazy('teacher_dashboard')
        elif role == 'admin':
            return reverse_lazy('admin_dashboard')
        messages.warning(self.request, "No valid role selected, redirecting to home.")
        return reverse_lazy('home')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Registration successful! Please log in with your credentials.")
            return redirect('login')  # Redirect to login page
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})