from django.urls import path
from .views import (
    home_view, 
    login_view, 
    logout_view, 
    invite_user_view,
    relationshiptype_list,
    relationshiptype_create,
    relationshiptype_edit,
    relationshiptype_delete,
    companies_list,
    companies_create,
    companies_edit,
    companies_delete,
    contacts_list,
    contacts_create,
    contacts_edit,
    contacts_delete
)

urlpatterns = [
    # Página inicial
    path('', home_view, name='home'),

    # Autenticação
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Convite
    path('invite/', invite_user_view, name='invite_user'),

    # RelationshipType Views
    path('relationshiptypes/', relationshiptype_list, name='relationshiptype_list'),
    path('relationshiptypes/add/', relationshiptype_create, name='relationshiptype_create'),
    path('relationshiptypes/<int:pk>/edit/', relationshiptype_edit, name='relationshiptype_edit'),
    path('relationshiptypes/<int:pk>/delete/', relationshiptype_delete, name='relationshiptype_delete'),

    # Companies Views
    path('companies/', companies_list, name='companies_list'),
    path('companies/add/', companies_create, name='companies_create'),
    path('companies/<int:pk>/edit/', companies_edit, name='companies_edit'),
    path('companies/<int:pk>/delete/', companies_delete, name='companies_delete'),

    # Contacts Views
    path('contacts/', contacts_list, name='contacts_list'),
    path('contacts/add/', contacts_create, name='contacts_create'),
    path('contacts/<int:pk>/edit/', contacts_edit, name='contacts_edit'),
    path('contacts/<int:pk>/delete/', contacts_delete, name='contacts_delete'),
]
