from django import forms
from .models import Assignment, Course, ExamRoutine, Event, FeeDue, CustomUser

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('title', 'description', 'subject', 'due_date', 'semester')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'faculty', 'available_seats')

class ExamRoutineForm(forms.ModelForm):
    class Meta:
        model = ExamRoutine
        fields = ('subject', 'date', 'details')

class NotificationForm(forms.Form):
    subject = forms.CharField(max_length=200)
    message = forms.TextField()
    recipients = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.filter(role='student'))

class UpdateSeatsForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    available_seats = forms.PositiveIntegerField()

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'date', 'type')

class FeeDueForm(forms.ModelForm):
    class Meta:
        model = FeeDue
        fields = ('student', 'amount', 'due_date')