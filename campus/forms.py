from django import forms
from .models import Assignment, Course, ExamRoutine, Event, FeeDue, CustomUser

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('title', 'description', 'subject', 'due_date', 'semester')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        # fields = ('name', 'faculty', 'available_seats')
        fields = ['name', 'description', 'duration', 'location', 'available_seats']
        
class ExamRoutineForm(forms.ModelForm):
    class Meta:
        model = ExamRoutine
        fields = ('subject', 'date', 'details')

class NotificationForm(forms.Form):
    subject = forms.CharField(max_length=200)
    message = forms.TimeField()
    recipients = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.filter(role='student'),
                                  widget=forms.CheckboxSelectMultiple)

class UpdateSeatsForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    available_seats = forms.IntegerField(min_value=0)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'date', 'type')

class FeeDueForm(forms.ModelForm):
    class Meta:
        model = FeeDue
        fields = ('student', 'amount', 'due_date')