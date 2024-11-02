from django.db import models, transaction
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError, PermissionDenied
from accounts.models import CustomUser
from methodology.models import Methodology
from locations.models import Room, Measurement
from inventory.models import InventoryItem

# ====== AnalysisRequest Model ======
class AnalysisRequest(models.Model):
    title = models.CharField(max_length=255, help_text="Title of the analysis request")
    requested_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='analysis_requests',
        help_text="User (client) who made the analysis request"
    )
    methodologies = models.ManyToManyField(
        Methodology,
        related_name='analysis_requests',
        help_text="Methodologies to be applied to the samples"
    )
    comments = models.TextField(blank=True, null=True, help_text="Additional instructions or comments from the client")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the analysis request was created")
    sample_image = models.ImageField(
        upload_to='request_images/',
        blank=True,
        null=True,
        help_text="Image of the sample related to the request"
    )
    history = HistoricalRecords()

    class Meta:
        permissions = [
            ("can_view_analysisrequest", "Can view analysis requests"),
            ("can_add_analysisrequest", "Can add analysis requests"),
            ("can_change_analysisrequest", "Can change analysis requests"),
            ("can_delete_analysisrequest", "Can delete analysis requests"),
        ]
        verbose_name = "Analysis Request"
        verbose_name_plural = "Analysis Requests"

    def __str__(self):
        return f"Analysis Request: {self.title} by {self.requested_by.get_full_name() if self.requested_by else 'Unknown'}"

# ====== ReceptionItem Model ======
class ReceptionItem(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the received item")
    serial_number = models.CharField(max_length=100, unique=True, blank=True, null=True, help_text="Serial number of the item")
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Weight of the item")
    analysis_request = models.ForeignKey(
        AnalysisRequest,
        on_delete=models.CASCADE,
        related_name='reception_items',
        help_text="Analysis request associated with the item"
    )
    received_at = models.DateTimeField(auto_now_add=True)
    received_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_items'
    )
    condition = models.CharField(max_length=255, help_text="Condition of the item upon reception")
    sample_image = models.ImageField(
        upload_to='reception_images/',
        blank=True,
        null=True,
        help_text="Image of the received sample"
    )
    shipment_date = models.DateField(null=True, blank=True, help_text="Date of shipment")
    shipment_location = models.CharField(max_length=255, null=True, blank=True, help_text="Location of shipment")
    max_days_for_result = models.IntegerField(null=True, blank=True, help_text="Maximum number of days for the result")
    history = HistoricalRecords()

    class Meta:
        permissions = [
            ("can_view_receptionitem", "Can view reception items"),
            ("can_add_receptionitem", "Can add reception items"),
            ("can_change_receptionitem", "Can change reception items"),
            ("can_delete_receptionitem", "Can delete reception items"),
        ]
        verbose_name = "Reception Item"
        verbose_name_plural = "Reception Items"

    def save(self, *args, **kwargs):
        if not self.serial_number:
            self.serial_number = get_random_string(length=12)
        super(ReceptionItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"Reception of {self.name} for {self.analysis_request.title}"

# ====== Analysis Model ======
class Analysis(models.Model):
    item = models.ForeignKey(
        ReceptionItem,
        on_delete=models.CASCADE,
        related_name='analysis_records',
        help_text="Reception item being analyzed"
    )
    methodology = models.ForeignKey(
        Methodology,
        on_delete=models.CASCADE,
        related_name='analyses',
        help_text="Methodology used for the analysis"
    )
    analysis_type = models.CharField(max_length=255, help_text="Type of analysis performed")
    conformity = models.BooleanField(default=True, help_text="Indicates if the analysis is compliant with expected results")
    analyzed_at = models.DateTimeField(auto_now_add=True)
    analyzed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='analyzed_items'
    )
    results = models.JSONField(help_text="Analysis results in JSON format")
    approved_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_analyses',
        help_text="User who approved the analysis",
        default=None
    )
    approval_date = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        permissions = [
            ("can_view_analysis", "Can view analyses"),
            ("can_add_analysis", "Can add analyses"),
            ("can_change_analysis", "Can change analyses"),
            ("can_delete_analysis", "Can delete analyses"),
        ]
        verbose_name = "Analysis"
        verbose_name_plural = "Analyses"

    def save(self, *args, **kwargs):
        self.verify_calibration()
        if not self.pk:
            self.decrement_supplies()
        super(Analysis, self).save(*args, **kwargs)

    def decrement_supplies(self):
        supplies = self.methodology.supplies.all()
        for supply_item in supplies:
            inventory_item = supply_item.supply
            if inventory_item.item_type == 'SUPPLY' and inventory_item.quantity is not None:
                new_quantity = inventory_item.quantity - supply_item.quantity
                if new_quantity < 0:
                    raise ValidationError(f"Insufficient quantity of {inventory_item.name}. Available: {inventory_item.quantity}, needed: {supply_item.quantity}.")
                inventory_item.quantity = new_quantity
                inventory_item.save()

    def verify_calibration(self):
        equipment_items = self.methodology.equipment.all()
        today = timezone.now().date()
        for equipment in equipment_items:
            calibration_records = equipment.calibration_records.filter(
                date__date=today,
                calibrated_by=self.analyzed_by
            )
            if not calibration_records.exists():
                raise ValidationError(f"{equipment.name} was not calibrated today by {self.analyzed_by}.")

    def approve(self, user):
        if not user.has_perm('can_approve_analysis'):
            raise PermissionDenied("You do not have permission to approve this analysis.")
        self.approved_by = user
        self.approval_date = timezone.now()
        self.save()

    def __str__(self):
        return f"Analysis of {self.item.name} using {self.methodology.title}"

# ====== AnalysisApproval Model ======
class AnalysisApproval(models.Model):
    analysis = models.OneToOneField(
        Analysis, 
        on_delete=models.CASCADE, 
        related_name='approval'
    )
    approved_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='approvals'
    )
    approval_date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=50, 
        choices=[('approved', 'Approved'), ('rejected', 'Rejected')]
    )

    class Meta:
        permissions = [
            ("can_view_analysisapproval", "Can view analysis approvals"),
            ("can_add_analysisapproval", "Can add analysis approvals"),
            ("can_change_analysisapproval", "Can change analysis approvals"),
            ("can_delete_analysisapproval", "Can delete analysis approvals"),
        ]

    def save(self, *args, **kwargs):
        self.analysis.approved_by = self.approved_by
        self.analysis.approval_date = self.approval_date
        self.analysis.save(update_fields=['approved_by', 'approval_date'])
        super(AnalysisApproval, self).save(*args, **kwargs)

    def __str__(self):
        return f"Approval for {self.analysis.item.name} by {self.approved_by.get_full_name()}"

# ====== Disposal Model ======
class Disposal(models.Model):
    item = models.ForeignKey(
        ReceptionItem, 
        on_delete=models.CASCADE, 
        related_name='disposals'
    )
    analysis = models.ForeignKey(
        Analysis,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='disposal_records'
    )
    disposed_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='disposed_items'
    )
    disposal_date = models.DateTimeField(default=timezone.now)
    reason = models.TextField()
    comments = models.TextField(blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        permissions = [
            ("can_view_disposal", "Can view disposals"),
            ("can_add_disposal", "Can add disposals"),
            ("can_change_disposal", "Can change disposals"),
            ("can_delete_disposal", "Can delete disposals"),
        ]
        verbose_name = "Disposal"
        verbose_name_plural = "Disposals"

    def save(self, *args, **kwargs):
        if self.disposed_by and not self.disposed_by.has_perm('can_add_disposal'):
            raise PermissionDenied("You do not have permission to register the disposal.")
        super(Disposal, self).save(*args, **kwargs)

    def __str__(self):
        return f"Disposal of {self.item.name} by {self.disposed_by.get_full_name()} on {self.disposal_date.strftime('%d/%m/%Y %H:%M')}"
