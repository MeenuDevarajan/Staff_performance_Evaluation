from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from staff_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='staff_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='staff_app/logout.html', next_page='login'), name='logout'),
    
    # App URLs
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('evaluate-performance/', views.evaluate_performance, name='evaluate_performance'),
    path('create-user/', views.create_user, name='create_user'),
    path('view-data/', views.view_data, name='view_data'),
]