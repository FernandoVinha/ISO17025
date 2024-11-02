from django.contrib import admin
from .models import RelationshipType, CustomUser, Invitation

# Admin para RelationshipType
@admin.register(RelationshipType)
class RelationshipTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']

# Admin para CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['role', 'is_active', 'is_staff']
    ordering = ['email']
    readonly_fields = ['date_joined']
    filter_horizontal = ('groups', 'user_permissions')

# Admin para Invitation
@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['email', 'token', 'created_at', 'used']
    search_fields = ['email', 'token']
    list_filter = ['used']
    ordering = ['created_at']
