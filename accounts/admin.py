# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Company, RelationshipType, Invitation
from simple_history.admin import SimpleHistoryAdmin
from django.utils.translation import gettext_lazy as _

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, SimpleHistoryAdmin):
    history_list_display = ['email', 'first_name', 'last_name', 'role', 'is_staff']
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']
    
    # Define campos de leitura somente
    readonly_fields = ('last_login', 'date_joined')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'profile_image')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Role'), {'fields': ('role',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )

@admin.register(Company)
class CompanyAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'email', 'phone', 'address']
    search_fields = ['name', 'email', 'phone', 'address']
    ordering = ['name']

@admin.register(RelationshipType)
class RelationshipTypeAdmin(SimpleHistoryAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Invitation)
class InvitationAdmin(SimpleHistoryAdmin):
    list_display = ['email', 'role', 'token', 'created_at', 'used', 'is_expired']
    search_fields = ['email', 'token']
    list_filter = ['role', 'used', 'created_at']
    ordering = ['-created_at']

    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'
