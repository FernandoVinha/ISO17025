import django_filters
from .models import InventoryItem

class InventoryItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Name')
    serial_number = django_filters.CharFilter(field_name='serial_number', lookup_expr='icontains', label='Serial Number')

    class Meta:
        model = InventoryItem
        fields = ['name', 'serial_number']
