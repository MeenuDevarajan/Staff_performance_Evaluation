from django.urls import path
from staff_app.views import custom_logout

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('evaluate-performance/', views.evaluate_performance, name='evaluate_performance'),
    path('create-user/', views.create_user, name='create_user'),
    path('view-data/', views.view_data, name='view_data'),
    path('logout/', custom_logout, name='logout'),
]