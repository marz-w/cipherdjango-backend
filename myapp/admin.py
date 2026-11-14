from django.contrib import admin
from .models import Contact, Employee

# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'created_at')
    search_fields = ('full_name', 'email', 'subject')
    list_filter = ('created_at',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'hire_date', 'job_title', 'salary')
    search_fields = ('first_name', 'last_name', 'email', 'job_title')
    list_filter = ('hire_date', 'job_title')
