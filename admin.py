from django.contrib import admin
from .models import Employee, PerformanceData

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['emp_id', 'name', 'department', 'position']
    search_fields = ['emp_id', 'name']

@admin.register(PerformanceData)
class PerformanceDataAdmin(admin.ModelAdmin):
    list_display = ['employee', 'project_id', 'date', 'performance_score']
    list_filter = ['date', 'employee__department']