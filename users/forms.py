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
    role = forms.ChoiceField(
        label="Select Role",
        choices=[('', 'Choose your role')] + [choice for choice in User.ROLE_CHOICES],
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
            user = User.objects.filter(email=email_or_phone).first()
            if not user:
                user = User.objects.filter(phone_number=email_or_phone).first()
            if user and user.check_password(password):
                self.user_cache = user
                if user.role != role:
                    raise ValidationError("The selected role does not match your account.")
            else:
                raise ValidationError("Invalid email, phone number, or password.")
        elif not role:
            raise ValidationError("Please select a role.")
        return cleaned_data

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'role', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'})
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
        self.fields['phone_number'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number (optional)'})
        self.fields['role'].widget = forms.Select(choices=[('', 'Choose your role')] + list(User.ROLE_CHOICES), attrs={'class': 'form-control'})
        self.fields['role'].required = True
        self.fields['phone_number'].required = False
        self.fields['email'].required = True
        self.fields['username'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user