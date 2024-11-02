from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from inventory.models import InventoryItem
from accounts.models import CustomUser
from datetime import timedelta
from django.db.models import JSONField
from django.contrib.auth import get_user_model

class StandardOperatingProcedure(models.Model):
    title = models.CharField(max_length=255)
    document = models.FileField(upload_to='sops/', help_text="Standard Operating Procedure (SOP) document")
    description = models.TextField(blank=True, null=True, help_text="SOP description")

    def __str__(self):
        return self.title

class CalibrationStandard(models.Model):
    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=100, unique=True)
    last_calibration_date = models.DateField(help_text="Last calibration date of the standard")
    certification_body = models.CharField(max_length=255, help_text="Certification organization")
    acceptable_error_margin = models.DecimalField(
        max_digits=10, 
        decimal_places=5, 
        help_text="Acceptable error margin for the equipment"
    )

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

class Maintenance(models.Model):
    item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name='maintenance_records',
        help_text="Item to be maintained"
    )
    technician = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='maintenance_tasks',
        help_text="Technician responsible for maintenance"
    )
    frequency_months = models.PositiveIntegerField(help_text="Maintenance interval in months")
    last_maintenance_date = models.DateField(null=True, blank=True, help_text="Last maintenance date")
    description = models.TextField(blank=True, null=True, help_text="Description of maintenance work")
    sop = models.ForeignKey(
        StandardOperatingProcedure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="SOP followed during maintenance"
    )
    report = models.FileField(
        upload_to='maintenance_reports/', 
        blank=True, 
        null=True, 
        help_text="Maintenance report"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Maintenance"
        verbose_name_plural = "Maintenances"
        permissions = [
            ("can_view_maintenance", "Can view maintenances"),
            ("can_add_maintenance", "Can add maintenances"),
            ("can_change_maintenance", "Can change maintenances"),
            ("can_delete_maintenance", "Can delete maintenances"),
        ]

    def __str__(self):
        next_maintenance = self.next_maintenance_date()
        return f"Maintenance of {self.item.name} (Next: {next_maintenance.strftime('%d/%m/%Y') if next_maintenance else 'Undefined date'})"

    def next_maintenance_date(self):
        if self.last_maintenance_date:
            return self.last_maintenance_date + timedelta(days=self.frequency_months * 30)
        return None

class Calibration(models.Model):
    item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name='calibration_records',
        help_text="Item to be calibrated"
    )
    technician = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='calibration_tasks',
        help_text="Technician responsible for calibration"
    )
    frequency_months = models.PositiveIntegerField(help_text="Calibration interval in months")
    last_calibration_date = models.DateField(null=True, blank=True, help_text="Last calibration date")
    measurement_uncertainty = models.DecimalField(
        max_digits=10, 
        decimal_places=5, 
        null=True, 
        blank=True, 
        help_text="Associated measurement uncertainty"
    )
    description = models.TextField(blank=True, null=True, help_text="Description of calibration work")
    sop = models.ForeignKey(
        StandardOperatingProcedure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="SOP followed during calibration"
    )
    standard = models.ForeignKey(
        CalibrationStandard,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Calibration standard used for traceability"
    )
    report = models.FileField(
        upload_to='calibration_reports/', 
        blank=True, 
        null=True, 
        help_text="Calibration report"
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Calibration"
        verbose_name_plural = "Calibrations"
        permissions = [
            ("can_view_calibration", "Can view calibrations"),
            ("can_add_calibration", "Can add calibrations"),
            ("can_change_calibration", "Can change calibrations"),
            ("can_delete_calibration", "Can delete calibrations"),
        ]

    def __str__(self):
        next_calibration = self.next_calibration_date()
        return f"Calibration of {self.item.name} (Next: {next_calibration.strftime('%d/%m/%Y') if next_calibration else 'Undefined date'})"

    def next_calibration_date(self):
        if self.last_calibration_date:
            return self.last_calibration_date + timedelta(days=self.frequency_months * 30)
        return None

class Training(models.Model):
    contact = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='trainings',
        help_text="Technician who received the training"
    )
    training_name = models.CharField(max_length=255, help_text="Training name")
    date_completed = models.DateField(help_text="Training completion date")
    certification_document = models.FileField(upload_to='certifications/', blank=True, null=True, help_text="Certification document")
    description = models.TextField(blank=True, null=True, help_text="Description of the training or acquired skills")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Training"
        verbose_name_plural = "Trainings"
        permissions = [
            ("can_view_training", "Can view trainings"),
            ("can_add_training", "Can add trainings"),
            ("can_change_training", "Can change trainings"),
            ("can_delete_training", "Can delete trainings"),
        ]

    def __str__(self):
        return f"{self.training_name} for {self.contact.get_full_name()} on {self.date_completed.strftime('%d/%m/%Y')}"

class DailyVerification(models.Model):
    user = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        related_name='daily_verifications',
        help_text="User who performed the verification"
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Verification date and time")
    measurements = JSONField(help_text="Measurements taken by the user")

    class Meta:
        verbose_name = "Daily Verification"
        verbose_name_plural = "Daily Verifications"
        permissions = [
            ("can_view_dailyverification", "Can view daily verifications"),
            ("can_add_dailyverification", "Can add daily verifications"),
            ("can_change_dailyverification", "Can change daily verifications"),
            ("can_delete_dailyverification", "Can delete daily verifications"),
        ]

    def __str__(self):
        return f"Daily verification by {self.user.get_full_name()} on {self.created_at.strftime('%d/%m/%Y %H:%M')}"
