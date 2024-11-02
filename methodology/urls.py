from django.urls import path
from .views import methodology_list, methodology_edit_or_view, methodology_create, methodology_delete, methodology_supply_delete

urlpatterns = [
    path('methodologies/', methodology_list, name='methodology_list'),
    path('methodology/new/', methodology_create, name='methodology_create'),
    path('methodology/<int:pk>/', methodology_edit_or_view, name='methodology_edit'),
    path('methodology/delete/<int:pk>/', methodology_delete, name='methodology_delete'),
    path('methodology/supply/delete/<int:pk>/', methodology_supply_delete, name='methodology_supply_delete'),
]
