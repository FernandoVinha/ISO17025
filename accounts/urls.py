# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'  # Define o namespace para facilitar a referência nas templates

urlpatterns = [
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/<str:token>/', views.register_view, name='register'),  # Certifique-se de que a URL aceita 'token'

    # Convite
    path('invite/', views.invite_user_view, name='invite_user'),

    # Accounts Views
    path('', views.accounts_list_view, name='accounts_list'),  # Lista consolidada de contas
    path('<int:account_id>/edit/', views.account_edit_view, name='account_edit'),
    path('<int:account_id>/delete/', views.account_delete_view, name='account_delete'),

    # RelationshipType Views
    path('relationshiptypes/', views.relationshiptype_list, name='relationshiptype_list'),
    path('relationshiptypes/add/', views.relationshiptype_create, name='relationshiptype_create'),
    path('relationshiptypes/<int:pk>/edit/', views.relationshiptype_edit, name='relationshiptype_edit'),
    path('relationshiptypes/<int:pk>/delete/', views.relationshiptype_delete, name='relationshiptype_delete'),

    # Perfil
    path('profile/', views.profile_update_view, name='profile'),
]
