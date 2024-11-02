#inventory/models.py
from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords

class InventoryItem(models.Model):
    ITEM_TYPE_CHOICES = [
        ('SIMPLE', 'Simple Item'),
        ('SUPPLY', 'Supply'),
        ('TOOL', 'Tool'),
        ('MEASURING', 'Measuring Equipment'),
        ('ELECTRONIC', 'Electronic Equipment'),
        ('MACHINE', 'Machine'),
        ('FURNITURE', 'Furniture'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=100, unique=True, help_text="Equipment serial number", db_index=True)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES, db_index=True)
    supplier = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturing_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    reception_date = models.DateField(auto_now_add=True)
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Used only for supplies")
    unit = models.CharField(max_length=2, choices=[('L', 'Liters'), ('G', 'Grams'), ('U', 'Unit')], null=True, blank=True, help_text="Used only for supplies")
    image = models.ImageField(upload_to='inventory_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    responsible_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='responsible_inventory_items', help_text="User responsible for the equipment")
    room = models.ForeignKey('locations.Room', on_delete=models.SET_NULL, null=True, blank=True, related_name='inventory_items', help_text="Room where the equipment is located")
    history = HistoricalRecords()

    class Meta:
        permissions = [
            ("can_view_inventoryitem", "Can view inventory items"),
            ("can_add_inventoryitem", "Can add inventory items"),
            ("can_change_inventoryitem", "Can change inventory items"),
            ("can_delete_inventoryitem", "Can delete inventory items"),
        ]

    def save(self, *args, **kwargs):
        # Ensure expiration date is not earlier than manufacturing date
        if self.expiration_date and self.expiration_date < self.manufacturing_date:
            raise ValueError("Expiration date cannot be earlier than manufacturing date.")

        # For supplies, ensure a valid quantity is provided
        if self.item_type == 'SUPPLY' and (self.quantity is None or self.quantity <= 0):
            raise ValueError("Supplies must have a valid quantity.")

        # Allow serial number to be optional for certain types
        if self.item_type in ['SIMPLE', 'SUPPLY'] and not self.serial_number:
            self.serial_number = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.serial_number or 'No Serial Number'})"
