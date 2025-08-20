from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from events.models import Event
from django.utils import timezone

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # BIM subjects by semester
        bim_subjects = {
            1: ["Principles of Management", "English Composition", "Basic Mathematics", "Computer Information System", "Digital Logic Design"],
            2: ["Business Communications", "Digital Logic", "Discrete Structure", "Object Oriented Programming with Java", "Organizational Behavior & Human Resource Management"],
            3: ["Business Statistics", "Data Structure and Algorithms", "Financial Accounting", "Microprocessor and Computer Architecture", "Web Technology I"],
            4: ["Business Data Communication and Networking", "Cost and Management Accounting", "Database Management System", "Economics for Business", "Operating System", "Web Technology II"],
            5: ["Artificial Intelligence", "Fundamentals of Marketing", "Information Security", "Programming with Python", "Software Design and Development"],
            6: ["Business Environment", "Business Information Systems", "Business Research Methods", "Fundamentals of Corporate Finance", "IT Ethics and Cybersecurity", "Project"],
            7: ["E-Commerce and Internet Marketing", "Elective I", "Operations Management", "Sociology for Business Management", "Strategic Management"],
            8: ["Business Intelligence", "Digital Economy", "Economics of Information and Communication", "Elective II", "Internship"],
        }

        # Fee structure
        fee_structure = {
            2079: 475000,
            2080: 500000,
            2081: 525000,
            2082: 550000,
        }

        # Fetch latest events
        events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]  # Next 3 events

        context.update({
            'bim_subjects': bim_subjects,
            'fee_structure': fee_structure,
            'events': events,
        })
        return context

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})