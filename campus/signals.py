from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Attendance, StudentProfile
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings


@receiver(post_save, sender=Attendance)
def update_attendance(sender, instance, created, **kwargs):
    if created:
        student = instance.student
        profile, _ = StudentProfile.objects.get_or_create(user=student)
        profile.attended_days += 1 if instance.present else 0
        profile.save()
        if profile.total_days > 0 and (profile.attended_days / profile.total_days * 100 < 80):
             # Simplified email usage for robustness
             try:
                send_mail(
                    'Low Attendance Alert',
                    f'Your attendance is below 80%. Contact your faculty.',
                    settings.EMAIL_HOST_USER,
                    [student.email],
                    fail_silently=True,
                )
             except Exception:
                 pass
            # Twilio commented out to avoid crashes if not configured
            # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            # client.messages.create(to=student.phone_number, from_=settings.TWILIO_PHONE_NUMBER, body='Low attendance alert!')

from django.contrib.auth import get_user_model
User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'student':
            StudentProfile.objects.get_or_create(user=instance)
        elif instance.role == 'teacher':
            from .models import TeacherProfile # lazy import
            TeacherProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == 'student':
        if hasattr(instance, 'studentprofile'):
             instance.studentprofile.save()
    elif instance.role == 'teacher':
        if hasattr(instance, 'teacherprofile'):
             instance.teacherprofile.save()