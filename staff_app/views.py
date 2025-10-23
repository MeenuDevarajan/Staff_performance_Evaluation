from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
import pandas as pd
import os
from .forms import CSVUploadForm, PerformanceForm
from .ml_model import PerformancePredictor
from .models import Employee, PerformanceData
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .ml_model import PerformancePredictor

@login_required
def custom_logout(request):
    """Custom logout view"""
    logout(request)
    return render(request, 'staff_app/logout.html')

def is_admin(user):
    return user.is_staff

@login_required
def dashboard(request):
    return render(request, 'staff_app/dashboard.html', {
        'user': request.user,
        'is_admin': request.user.is_staff
    })

@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            try:
                # Read CSV file
                df = pd.read_csv(csv_file)
                
                # Process the data (simple example)
                result = f"File uploaded successfully! Found {len(df)} rows."
                return render(request, 'staff_app/upload_csv.html', {
                    'form': form,
                    'result': result,
                    'columns': df.columns.tolist()
                })
            except Exception as e:
                return render(request, 'staff_app/upload_csv.html', {
                    'form': form,
                    'error': f"Error processing file: {str(e)}"
                })
    else:
        form = CSVUploadForm()
    
    return render(request, 'staff_app/upload_csv.html', {'form': form})


@login_required
def evaluate_performance(request):
    predictor = PerformancePredictor()
    
    if request.method == 'POST':
        total_hours = request.POST.get('total_hours')
        activity_percentage = request.POST.get('activity_percentage')
        
        if total_hours and activity_percentage:
            try:
                total_hours = float(total_hours)
                activity_percentage = float(activity_percentage)
                
                # Validate input ranges
                if not (0 <= total_hours <= 24):
                    return render(request, 'staff_app/evaluate_performance.html', {
                        'error': 'Hours must be between 0-24'
                    })
                
                if not (0 <= activity_percentage <= 100):
                    return render(request, 'staff_app/evaluate_performance.html', {
                        'error': 'Activity must be between 0-100%'
                    })
                
                # Get ML prediction
                score = predictor.predict(total_hours, activity_percentage)
                
                # Get performance data from database
                performance_data = PerformanceData.objects.all().order_by('-performance_score')[:8]
                
                return render(request, 'staff_app/evaluate_performance.html', {
                    'score': score,
                    'total_hours': total_hours,
                    'activity_percentage': activity_percentage,
                    'performance_data': performance_data,
                    'ml_used': True  # Flag to show ML was used
                })
                
            except ValueError:
                return render(request, 'staff_app/evaluate_performance.html', {
                    'error': 'Please enter valid numbers'
                })
        else:
            return render(request, 'staff_app/evaluate_performance.html', {
                'error': 'Please fill in all fields'
            })
    
    # For GET request
    performance_data = PerformanceData.objects.all().order_by('-performance_score')[:8]
    return render(request, 'staff_app/evaluate_performance.html', {
        'performance_data': performance_data
    })

@login_required
@user_passes_test(is_admin)
def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_staff = request.POST.get('is_staff') == 'on'
        
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                is_staff=is_staff
            )
            return render(request, 'staff_app/create_user.html', {
                'message': f'User {username} created successfully!'
            })
        except Exception as e:
            return render(request, 'staff_app/create_user.html', {
                'error': f'Error creating user: {str(e)}'
            })
    
    return render(request, 'staff_app/create_user.html')

@login_required
def view_data(request):
    # Admin sees everything, regular users see only their data
    if request.user.is_staff:
        performance_data = PerformanceData.objects.all()
        employees = Employee.objects.all()
        message = "Administrator View - All Employee Data"
    else:
        # Regular users see only data where employee name matches their username
        performance_data = PerformanceData.objects.filter(employee__name=request.user.username)
        employees = Employee.objects.filter(name=request.user.username)
        message = f"Your Performance Data - {request.user.username}"
    
    return render(request, 'staff_app/view_data.html', {
        'employees': employees,
        'performance_data': performance_data,
        'message': message
    })