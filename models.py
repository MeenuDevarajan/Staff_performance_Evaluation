from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    emp_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} ({self.emp_id})"

class PerformanceData(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project_id = models.CharField(max_length=50)
    date = models.DateField()
    time_spent = models.IntegerField()  # in minutes
    activity_level = models.FloatField()  # 0.0 to 1.0
    performance_score = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.employee.name} - {self.project_id}"