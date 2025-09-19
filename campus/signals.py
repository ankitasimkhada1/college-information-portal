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
        profile = StudentProfile.objects.get(user=student)
        profile.attended_days += 1 if instance.present else 0
        profile.save()
        if profile.attended_days / profile.total_days * 100 < 80:
            send_mail(
                'Low Attendance Alert',
                f'Your attendance is below 80%. Contact your faculty.',
                settings.EMAIL_HOST_USER,
                [student.email],
                fail_silently=True,
            )
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(to=student.phone_number, from_=settings.TWILIO_PHONE_NUMBER, body='Low attendance alert!')