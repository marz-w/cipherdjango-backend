from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Contact, Employee

# Create your views here.

def home(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return redirect('home')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('home')

        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('home')

        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('home')

        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'User registered successfully.')
            return redirect('home')

    return render(request, 'home.html')

def contact(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not full_name or not email or not subject or not message:
            messages.error(request, 'All fields are required.')
            return redirect('contact')

        Contact.objects.create(
            full_name=full_name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')

    return render(request, 'contact.html')

def employee(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        hire_date = request.POST.get('hire_date', '').strip()
        job_title = request.POST.get('job_title', '').strip()
        salary = request.POST.get('salary', '').strip()

        if not first_name or not last_name or not email or not hire_date or not job_title or not salary:
            messages.error(request, 'All fields except phone number are required.')
            return redirect('employee')

        # Create the employee record
        Employee.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            hire_date=hire_date,
            job_title=job_title,
            salary=salary
        )
        messages.success(request, 'Employee added successfully!')
        return redirect('employee')

    return render(request, 'employee.html')
