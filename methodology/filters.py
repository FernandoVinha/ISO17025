# filters.py
import django_filters
from .models import Methodology

class MethodologyFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Título')
    author = django_filters.CharFilter(field_name='author__first_name', lookup_expr='icontains', label='Autor')
    equipment = django_filters.CharFilter(field_name='equipment__name', lookup_expr='icontains', label='Equipamento')

    class Meta:
        model = Methodology
        fields = ['title', 'author', 'equipment']
