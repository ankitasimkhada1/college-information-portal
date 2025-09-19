from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.utils import timezone

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    email_or_phone = forms.CharField(
        label="Email or Phone Number",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email or phone number'})
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )
    role = forms.ChoiceField(
        label="Select Role",
        choices=[('', 'Choose your role')] + list(User.ROLE_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)

    def clean(self):
        cleaned_data = super().clean()
        email_or_phone = cleaned_data.get('email_or_phone')
        password = cleaned_data.get('password')
        role = cleaned_data.get('role')

        if email_or_phone and password and role:
            user = authenticate(self.request, username=email_or_phone, password=password)
            if user is None:
                # Try phone number if email fails
                user = authenticate(self.request, username=User.objects.filter(phone_number=email_or_phone).first().email if User.objects.filter(phone_number=email_or_phone).exists() else email_or_phone, password=password)
            if user is None:
                raise ValidationError("Invalid email, phone number, or password.")
            elif user.role != role:
                raise ValidationError("The selected role does not match your account.")
            self.user_cache = user
        elif not role:
            raise ValidationError("Please select a role.")
        return cleaned_data

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'role', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
        self.fields['phone_number'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number (optional)'})
        self.fields['role'].widget = forms.Select(choices=[('', 'Choose your role')] + list(User.ROLE_CHOICES), attrs={'class': 'form-control'})
        self.fields['role'].required = True
        self.fields['phone_number'].required = False
        self.fields['email'].required = True
        # Remove username field since it's generated
        self.fields.pop('username', None)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        # Generate username similar to CustomUserManager
        base_username = user.email.split('@')[0].replace('.', '_')
        username = f"{base_username}_{timezone.now().strftime('%Y%m%d%H%M%S')}"
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{timezone.now().strftime('%Y%m%d%H%M%S')}"
        user.username = username
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user