# accounts/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    # Página inicial
    path('', home_view, name='home'),

    # Autenticação
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/<str:token>/', register_view, name='register'),  # Certifique-se de que a URL aceita 'token'

    # Convite
    path('invite/', invite_user_view, name='invite_user'),

    # RelationshipType Views
    path('relationshiptypes/', relationshiptype_list, name='relationshiptype_list'),
    path('relationshiptypes/add/', relationshiptype_create, name='relationshiptype_create'),
    path('relationshiptypes/<int:pk>/edit/', relationshiptype_edit, name='relationshiptype_edit'),
    path('relationshiptypes/<int:pk>/delete/', relationshiptype_delete, name='relationshiptype_delete'),

    path('profile/', profile_update_view, name='profile'),
]
