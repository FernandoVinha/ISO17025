import django_filters
from .models import Maintenance, Calibration, Training, StandardOperatingProcedure, CalibrationStandard, DailyVerification

class MaintenanceFilter(django_filters.FilterSet):
    class Meta:
        model = Maintenance
        fields = {
            'item': ['exact'],
            'technician': ['exact'],
            'frequency_months': ['exact', 'gt', 'lt'],
            'last_maintenance_date': ['exact', 'year__gte', 'year__lte'],
        }

class CalibrationFilter(django_filters.FilterSet):
    class Meta:
        model = Calibration
        fields = {
            'item': ['exact'],
            'technician': ['exact'],
            'frequency_months': ['exact', 'gt', 'lt'],
            'last_calibration_date': ['exact', 'year__gte', 'year__lte'],
            'measurement_uncertainty': ['exact', 'gt', 'lt'],
        }

class TrainingFilter(django_filters.FilterSet):
    class Meta:
        model = Training
        fields = {
            'contact': ['exact'],
            'training_name': ['icontains'],
            'date_completed': ['exact', 'year__gte', 'year__lte'],
        }

class SOPFilter(django_filters.FilterSet):
    class Meta:
        model = StandardOperatingProcedure
        fields = {
            'title': ['icontains'],
        }

class CalibrationStandardFilter(django_filters.FilterSet):
    class Meta:
        model = CalibrationStandard
        fields = {
            'name': ['icontains'],
            'serial_number': ['exact'],
            'last_calibration_date': ['exact', 'year__gte', 'year__lte'],
            'certification_body': ['icontains'],
        }

class DailyVerificationFilter(django_filters.FilterSet):
    class Meta:
        model = DailyVerification
        fields = {
            'user': ['exact'],
            'created_at': ['exact', 'year__gte', 'year__lte'],
        }
