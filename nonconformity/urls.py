# nonconformity/urls.py

from django.urls import path
from .views import create_nonconformity, nonconformity_list, delete_nonconformity

urlpatterns = [
    path('create/', create_nonconformity, name='create_nonconformity'),
    path('list/', nonconformity_list, name='nonconformity_list'),
    path('delete/<int:pk>/', delete_nonconformity, name='delete_nonconformity'),
]
