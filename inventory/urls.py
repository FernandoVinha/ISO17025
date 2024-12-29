# inventory/urls.py
from django.urls import path
from . import views

app_name = 'inventory'  # Ensure this namespace is defined

urlpatterns = [
    path('', views.inventoryitem_list, name='inventoryitem_list'),
    path('add/', views.inventoryitem_create, name='inventoryitem_create'),
    path('edit/<int:pk>/', views.inventoryitem_edit, name='inventoryitem_edit'),
    path('delete/<int:pk>/', views.inventoryitem_delete, name='inventoryitem_delete'),  # Correct URL for deletion
]
