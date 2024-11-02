from django.urls import path
from . import views

urlpatterns = [
    # Maintenance URLs
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/create/', views.maintenance_create, name='maintenance_create'),
    path('maintenance/edit/<int:pk>/', views.maintenance_edit, name='maintenance_edit'),
    path('maintenance/delete/<int:pk>/', views.maintenance_delete, name='maintenance_delete'),
    path('maintenance/calendar/', views.maintenance_calendar, name='maintenance_calendar'),
    path('maintenance/day/<int:year>/<int:month>/<int:day>/', views.maintenance_list_by_day, name='maintenance_list_by_day'),
    path('maintenance/', views.maintenance_list, name='maintenance_list'),

    # Calibration URLs
    path('calibration/', views.calibration_list, name='calibration_list'),
    path('calibration/create/', views.calibration_create, name='calibration_create'),
    path('calibration/edit/<int:pk>/', views.calibration_edit, name='calibration_edit'),
    path('calibration/delete/<int:pk>/', views.calibration_delete, name='calibration_delete'),

    # Training URLs
    path('training/', views.training_list, name='training_list'),
    path('training/create/', views.training_create, name='training_create'),
    path('training/edit/<int:pk>/', views.training_edit, name='training_edit'),
    path('training/delete/<int:pk>/', views.training_delete, name='training_delete'),

    # Standard Operating Procedure (SOP) URLs
    path('sop/', views.sop_list, name='sop_list'),
    path('sop/create/', views.sop_create, name='sop_create'),
    path('sop/edit/<int:pk>/', views.sop_edit, name='sop_edit'),
    path('sop/delete/<int:pk>/', views.sop_delete, name='sop_delete'),

    # Calibration Standard URLs
    path('calibration-standard/', views.calibration_standard_list, name='calibration_standard_list'),
    path('calibration-standard/create/', views.calibration_standard_create, name='calibration_standard_create'),
    path('calibration-standard/edit/<int:pk>/', views.calibration_standard_edit, name='calibration_standard_edit'),
    path('calibration-standard/delete/<int:pk>/', views.calibration_standard_delete, name='calibration_standard_delete'),

    path('calibrationstandard/', views.calibration_standard_list, name='calibrationstandard_list'),
]
