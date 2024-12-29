# maintenance/urls.py

from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.maintenance_list, name='maintenance_list'),
    path('add/', views.maintenance_create, name='maintenance_create'),
    path('edit/<int:pk>/', views.maintenance_edit, name='maintenance_edit'),
    path('delete/<int:pk>/', views.maintenance_delete, name='maintenance_delete'),

    path('calibration/', views.calibration_list, name='calibration_list'),
    path('calibration/add/', views.calibration_create, name='calibration_create'),
    path('calibration/edit/<int:pk>/', views.calibration_edit, name='calibration_edit'),
    path('calibration/delete/<int:pk>/', views.calibration_delete, name='calibration_delete'),

    path('training/', views.training_list, name='training_list'),
    path('training/add/', views.training_create, name='training_create'),
    path('training/edit/<int:pk>/', views.training_edit, name='training_edit'),
    path('training/delete/<int:pk>/', views.training_delete, name='training_delete'),

    path('sop/', views.sop_list, name='sop_list'),
    path('sop/add/', views.sop_create, name='sop_create'),
    path('sop/edit/<int:pk>/', views.sop_edit, name='sop_edit'),
    path('sop/delete/<int:pk>/', views.sop_delete, name='sop_delete'),

    path('calibration-standard/', views.calibration_standard_list, name='calibration_standard_list'),
    path('calibration-standard/add/', views.calibration_standard_create, name='calibration_standard_create'),
    path('calibration-standard/edit/<int:pk>/', views.calibration_standard_edit, name='calibration_standard_edit'),
    path('calibration-standard/delete/<int:pk>/', views.calibration_standard_delete, name='calibration_standard_delete'),

    path('daily-verification/', views.daily_verification_list, name='daily_verification_list'),
    path('daily-verification/add/', views.daily_verification_create, name='daily_verification_create'),
    path('daily-verification/edit/<int:pk>/', views.daily_verification_edit, name='daily_verification_edit'),
    path('daily-verification/delete/<int:pk>/', views.daily_verification_delete, name='daily_verification_delete'),
]
