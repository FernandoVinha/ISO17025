# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, Companies, Contacts, RelationshipType, Invitation

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active', 'profile_image_tag')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role', 'profile_image')}),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'user_permissions'),
            'description': 'Manage user permissions here, including custom permissions for Sample Reception, Storage, Analysis, and Reports.'
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'role')}
        ),
    )
    readonly_fields = ('date_joined', 'profile_image_tag')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('user_permissions',)

    def profile_image_tag(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.profile_image.url))
        return "-"
    profile_image_tag.short_description = 'Profile Image'

class CompaniesAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'relationship_type', 'related_contacts')
    search_fields = ('name', 'email')
    list_filter = ('relationship_type',)

    def related_contacts(self, obj):
        return ", ".join([contact.name for contact in obj.company_contacts.all()])
    related_contacts.short_description = 'Contacts'

class ContactsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'position', 'company')
    search_fields = ('name', 'email', 'position')
    list_filter = ('company',)

class RelationshipTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'token', 'created_at', 'used')
    search_fields = ('email', 'token')
    list_filter = ('used',)
    actions = ['mark_as_used']

    @admin.action(description='Mark selected invitations as used')
    def mark_as_used(self, request, queryset):
        queryset.update(used=True)
        self.message_user(request, "Selected invitations have been marked as used.")

# Registre os modelos no admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Companies, CompaniesAdmin)
admin.site.register(Contacts, ContactsAdmin)
admin.site.register(RelationshipType, RelationshipTypeAdmin)
admin.site.register(Invitation, InvitationAdmin)
