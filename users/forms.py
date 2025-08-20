from os import login_tty
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from users.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'phone', 'role')  # Adjust fields based on your model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = "Email"
        self.fields['phone'].required = False
        self.fields['role'].required = False

# Update register_view to use this form
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login_tty(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})