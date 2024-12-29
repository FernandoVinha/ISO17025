# accounts/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from datetime import timedelta
from simple_history.models import HistoricalRecords
import uuid


class RelationshipType(models.Model):
    """
    Represents the types of relationships in the system.
    """
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Name"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Relationship Type")
        verbose_name_plural = _("Relationship Types")
        permissions = [
            ("create_relationshiptype", _("Can create relationship type")),
            ("edit_relationshiptype", _("Can edit relationship type")),
            ("can_view_relationshiptype", _("Can view relationship types")),
            ("can_delete_relationshiptype", _("Can delete relationship type")),
        ]

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    """
    Custom manager for handling user creation.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("An email address is required."))
        if not password:
            raise ValueError(_("A password is required."))

        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_("Superuser must have is_staff=True."))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with additional fields and roles.
    """
    ROLE_CHOICES = [
        ('client', _("Client")),
        ('supplier', _("Supplier")),
        ('maintenance', _("Maintenance")),
        ('employee', _("Employee")),
    ]

    email = models.EmailField(unique=True, verbose_name=_("Email Address"))
    first_name = models.CharField(max_length=30, blank=True, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=30, blank=True, verbose_name=_("Last Name"))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee', verbose_name=_("Role"))
    profile_image = models.ImageField(upload_to='user_profiles/', blank=True, null=True, verbose_name=_("Profile Image"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Is Staff"))
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Joined"))
    history = HistoricalRecords()

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _("Custom User")
        verbose_name_plural = _("Custom Users")
        permissions = [
            ("can_generate_invite", _("Can generate invitation link")),
            ("can_view_accounts", _("Can view accounts")),
            ("can_add_account", _("Can add account")),
            ("can_change_account", _("Can change account")),
            ("can_delete_account", _("Can delete account")),
        ]

    def __str__(self):
        return self.get_full_name() or self.email

    def get_full_name(self):
        """Returns the full name of the user."""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.email

    def get_short_name(self):
        """Returns the first name of the user or email as a fallback."""
        return self.first_name if self.first_name else self.email


class Invitation(models.Model):
    """
    Represents an invitation to join the system.
    """
    ROLE_CHOICES = CustomUser.ROLE_CHOICES

    email = models.EmailField(unique=True, verbose_name=_("Email Address"))
    token = models.CharField(max_length=32, unique=True, blank=True, verbose_name=_("Token"))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client', verbose_name=_("Role"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    used = models.BooleanField(default=False, verbose_name=_("Used"))
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Expires At"))
    history = HistoricalRecords()

    EXPIRATION_DAYS = 7

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_unique_token()
        if not self.expires_at:
            self.expires_at = now() + timedelta(days=self.EXPIRATION_DAYS)
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_token():
        """
        Generates a unique token for invitations.
        Ensures no duplication in the database.
        """
        token = get_random_string(length=32)
        while Invitation.objects.filter(token=token).exists():
            token = get_random_string(length=32)
        return token

    def mark_as_used(self):
        """
        Marks the invitation as used.
        """
        if self.used:
            raise ValueError(_("This invitation has already been used."))
        self.used = True
        self.save()

    def is_expired(self):
        """
        Checks if the invitation has expired based on the creation date.
        """
        return now() > self.expires_at

    def __str__(self):
        return f"Invitation for {self.email}"

    class Meta:
        verbose_name = _("Invitation")
        verbose_name_plural = _("Invitations")
        permissions = [
            ("can_view_invitation", _("Can view invitations")),
            ("can_add_invitation", _("Can add invitation")),
            ("can_change_invitation", _("Can change invitation")),
            ("can_delete_invitation", _("Can delete invitation")),
        ]


class Company(models.Model):
    """
    Represents a Company account in the system.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Company Name"))
    email = models.EmailField(verbose_name=_("Email Address"))
    phone = models.CharField(max_length=20, verbose_name=_("Phone"))
    address = models.CharField(max_length=255, verbose_name=_("Address"))
    profile_image = models.ImageField(upload_to='company_profiles/', blank=True, null=True, verbose_name=_("Profile Image"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        permissions = [
            ("can_view_company", _("Can view companies")),
            ("can_add_company", _("Can add company")),
            ("can_change_company", _("Can change company")),
            ("can_delete_company", _("Can delete company")),
        ]

    def __str__(self):
        return self.name
