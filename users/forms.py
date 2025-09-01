from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    email_or_phone = forms.CharField(
        label="Email or Phone Number",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email or phone number'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)

    def clean(self):
        email_or_phone = self.cleaned_data.get('email_or_phone')
        password = self.cleaned_data.get('password')

        if email_or_phone and password:
            try:
                user = User.objects.filter(email=email_or_phone).first()
                if not user:
                    user = User.objects.filter(phone_number=email_or_phone).first()
                if user and user.check_password(password):
                    self.user_cache = user
                else:
                    raise ValidationError("Invalid email, phone number, or password.")
            except User.DoesNotExist:
                raise ValidationError("Invalid email, phone number, or password.")
        return self.cleaned_data

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'role', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'})
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
        self.fields['phone_number'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number (optional)'})
        self.fields['role'].widget = forms.Select(choices=User.ROLE_CHOICES, attrs={'class': 'form-control'})
        self.fields['role'].required = True
        self.fields['phone_number'].required = False
        self.fields['email'].required = True
        self.fields['username'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.role = self.cleaned_data['role']
        user.save()
        return user