from django.shortcuts import render
from events.models import Event
from django.utils import timezone

def home_view(request):
    # Hardcoded BIM subjects by semester
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

    # Fee structure (hardcoded for simplicity, can be dynamic later)
    fee_structure = {
        2079: 475000,
        2080: 500000,
        2081: 525000,
        2082: 550000,
    }

    # Fetch latest events (admin-added)
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]  # Show next 3 events

    context = {
        'bim_subjects': bim_subjects,
        'fee_structure': fee_structure,
        'events': events,
    }
    return render(request, 'home.html', context)
