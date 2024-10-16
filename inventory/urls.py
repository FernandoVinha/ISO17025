from django.urls import path
from .views import (
    inventoryitem_list,
    inventoryitem_create,
    inventoryitem_edit,
    inventoryitem_delete,
)

urlpatterns = [
    path('', inventoryitem_list, name='inventoryitem_list'),  # Lista de itens de inventário
    path('add/', inventoryitem_create, name='inventoryitem_create'),  # Adicionar novo item
    path('edit/<int:pk>/', inventoryitem_edit, name='inventoryitem_edit'),  # Editar item existente
    path('delete/<int:pk>/', inventoryitem_delete, name='inventoryitem_delete'),  # Deletar item
]
