from django.contrib import admin
from .models import Maintenance, Calibration, Training, StandardOperatingProcedure, CalibrationStandard
from simple_history.admin import SimpleHistoryAdmin

# ====== Maintenance Admin ======

@admin.register(Maintenance)
class MaintenanceAdmin(SimpleHistoryAdmin):
    list_display = ('item', 'technician', 'last_maintenance_date', 'frequency_months', 'description')
    list_filter = ('item', 'technician', 'frequency_months')
    search_fields = ('item__name', 'technician__name', 'description')
    ordering = ('-last_maintenance_date',)
    history_list_display = ["changed_by"]

# ====== Calibration Admin ======

@admin.register(Calibration)
class CalibrationAdmin(SimpleHistoryAdmin):
    list_display = ('item', 'technician', 'last_calibration_date', 'frequency_months', 'measurement_uncertainty')
    list_filter = ('item', 'technician', 'frequency_months')
    search_fields = ('item__name', 'technician__name', 'description')
    ordering = ('-last_calibration_date',)
    history_list_display = ["changed_by"]

# ====== Training Admin ======

@admin.register(Training)
class TrainingAdmin(SimpleHistoryAdmin):
    list_display = ('contact', 'training_name', 'date_completed', 'description')
    list_filter = ('training_name', 'contact')
    search_fields = ('training_name', 'contact__name', 'description')
    ordering = ('-date_completed',)
    history_list_display = ["changed_by"]

# ====== Standard Operating Procedure Admin ======

@admin.register(StandardOperatingProcedure)
class StandardOperatingProcedureAdmin(SimpleHistoryAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')
    ordering = ('title',)
    history_list_display = ["changed_by"]

# ====== Calibration Standard Admin ======

@admin.register(CalibrationStandard)
class CalibrationStandardAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'serial_number', 'last_calibration_date', 'certification_body')
    list_filter = ('name', 'certification_body')
    search_fields = ('name', 'serial_number', 'certification_body')
    ordering = ('-last_calibration_date',)
    history_list_display = ["changed_by"]
