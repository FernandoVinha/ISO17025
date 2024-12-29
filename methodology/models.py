#methodology/models.py


from django.db import models
from simple_history.models import HistoricalRecords
from inventory.models import InventoryItem  # Import inventory items
from accounts.models import CustomUser  # Import users who create the methodology
from django.core.exceptions import PermissionDenied

class Methodology(models.Model):
    title = models.CharField(max_length=255, help_text="Title of the Methodology")
    description = models.TextField(help_text="Detailed description of the methodology")
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='methodologies',
        help_text="User who created the methodology"
    )
    equipment = models.ManyToManyField(
        InventoryItem,
        related_name='methodology_equipment',
        blank=True,
        help_text="List of equipment used in the methodology"
    )
    history = HistoricalRecords()

    class Meta:
        permissions = [
            ("can_view_methodology", "Can view methodologies"),
            ("can_add_methodology", "Can add methodologies"),
            ("can_change_methodology", "Can change methodologies"),
            ("can_delete_methodology", "Can delete methodologies"),
        ]

    def __str__(self):
        return self.title

class MethodologySupply(models.Model):
    methodology = models.ForeignKey(Methodology, on_delete=models.CASCADE, related_name='supplies', help_text="Methodology to which the supply belongs")
    supply = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='used_in_methodologies', help_text="Supply used")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantity of the supply used")
    unit = models.CharField(max_length=10, help_text="Unit of measurement, e.g., liters, grams", default="Unit")
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        # Check if the user creating/editing has permission to modify the methodology
        if not self.methodology.author.has_perm('can_change_methodology'):
            raise PermissionDenied("You do not have permission to edit supplies for this methodology.")
        super(MethodologySupply, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Check if the user has permission to delete the methodology
        if not self.methodology.author.has_perm('can_delete_methodology'):
            raise PermissionDenied("You do not have permission to delete supplies for this methodology.")
        super(MethodologySupply, self).delete(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.supply.name} for {self.methodology.title}"

    class Meta:
        unique_together = ('methodology', 'supply')
        permissions = [
            ("can_view_methodology_supply", "Can view methodology supplies"),
        ]