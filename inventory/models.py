from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords

class InventoryItem(models.Model):
    ITEM_TYPE_CHOICES = [
        ('SIMPLE', 'Simple Item'),
        ('SUPPLY', 'Supply'),
    ]

    name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=100, unique=True, help_text="Número de série do equipamento")
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    supplier = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturing_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    reception_date = models.DateField(auto_now_add=True)
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Usado apenas para suprimentos
    unit = models.CharField(max_length=2, choices=[('L', 'Liters'), ('G', 'Grams')], null=True, blank=True)  # Usado apenas para suprimentos
    image = models.ImageField(upload_to='inventory_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    responsible_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='responsible_inventory_items', help_text="Usuário responsável pelo equipamento")
    room = models.ForeignKey('locations.Room', on_delete=models.SET_NULL, null=True, blank=True, related_name='inventory_items', help_text="Sala onde o equipamento está localizado")

    history = HistoricalRecords()

    class Meta:
        permissions = [
            ("can_view_inventoryitem", "Pode visualizar itens de inventário"),
            ("can_add_inventoryitem", "Pode adicionar itens de inventário"),
            ("can_change_inventoryitem", "Pode alterar itens de inventário"),
            ("can_delete_inventoryitem", "Pode deletar itens de inventário"),
        ]

    def save(self, *args, **kwargs):
        if self.item_type == 'SUPPLY' and (self.quantity is None or self.quantity <= 0):
            self.delete()
        else:
            super(InventoryItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"
