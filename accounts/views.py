#accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.urls import reverse
from .forms import (
    CustomUserCreationForm,
    AccountEditForm,
    RelationshipTypeForm,
    InvitationForm,
    ProfileUpdateForm,
)
from .models import CustomUser, RelationshipType, Invitation
from simple_history.utils import update_change_reason
from django.core.paginator import Paginator


# Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'accounts/login.html')


# Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


# User Registration View
def register_view(request, token):
    invitation = get_object_or_404(Invitation, token=token, used=False)
    if invitation.is_expired():
        messages.error(request, 'This invitation has expired.')
        return redirect('accounts:login')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = invitation.role
            user.save()
            invitation.mark_as_used()
            messages.success(request, 'Registration completed successfully.')
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm(initial={'email': invitation.email, 'role': invitation.role})

    return render(request, 'accounts/register.html', {
        'form': form,
        'simple_history': invitation.history.all()[:30],
    })


# Accounts List View
@login_required
@permission_required('accounts.can_view_accounts', raise_exception=True)
def accounts_list_view(request):
    search_query = request.GET.get('search', '')
    account_type = request.GET.get('type', 'all')

    if account_type == 'all':
        accounts = CustomUser.objects.all()
    else:
        accounts = CustomUser.objects.filter(role=account_type)

    if search_query:
        accounts = accounts.filter(email__icontains=search_query)

    paginator = Paginator(accounts.order_by('id'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    simple_history = CustomUser.history.select_related('history_user')[:30]

    return render(request, 'accounts/accounts_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'account_type': account_type,
        'permissions': {
            'can_add_account': request.user.has_perm('accounts.can_add_account'),
        },
        'simple_history': simple_history,
    })


# Account Edit View
@login_required
@permission_required('accounts.can_change_account', raise_exception=True)
def account_edit_view(request, account_id):
    account = get_object_or_404(CustomUser, id=account_id)

    can_edit = request.user.has_perm('accounts.can_change_account')

    if request.method == 'POST' and can_edit:
        form = AccountEditForm(request.POST, request.FILES, instance=account)
        if form.is_valid():
            form.save()
            update_change_reason(account, f"Account updated by {request.user.email}")
            messages.success(request, 'Account updated successfully.')
            return redirect('accounts:accounts_list')
    else:
        form = AccountEditForm(instance=account)

    return render(request, 'accounts/account_edit.html', {
        'form': form,
        'account': account,
        'can_edit': can_edit,
        'simple_history': account.history.all()[:30],
    })


# Account Delete View
@login_required
@permission_required('accounts.can_delete_account', raise_exception=True)
def account_delete_view(request, account_id):
    account = get_object_or_404(CustomUser, id=account_id)
    if request.method == 'POST':
        account.delete()
        messages.success(request, 'Account deleted successfully.')
        return redirect('accounts:accounts_list')

    return render(request, 'accounts/account_confirm_delete.html', {
        'account': account,
        'simple_history': account.history.all()[:30],
    })


# RelationshipType Views
@login_required
@permission_required('accounts.can_add_relationshiptype', raise_exception=True)
def relationshiptype_create(request):
    if request.method == 'POST':
        form = RelationshipTypeForm(request.POST)
        if form.is_valid():
            relationship_type = form.save()
            update_change_reason(relationship_type, "Created relationship type")
            messages.success(request, 'Relationship type created successfully.')
            return redirect('accounts:relationshiptype_list')
    else:
        form = RelationshipTypeForm()

    return render(request, 'accounts/relationshiptype_form.html', {
        'form': form,
        'title': 'Add Relationship Type',
    })


@login_required
@permission_required('accounts.can_view_relationshiptype', raise_exception=True)
def relationshiptype_list(request):
    relationship_types = RelationshipType.objects.all()
    return render(request, 'accounts/relationshiptype_list.html', {
        'relationship_types': relationship_types,
    })


@login_required
@permission_required('accounts.can_change_relationshiptype', raise_exception=True)
def relationshiptype_edit(request, pk):
    relationship_type = get_object_or_404(RelationshipType, pk=pk)
    if request.method == 'POST':
        form = RelationshipTypeForm(request.POST, instance=relationship_type)
        if form.is_valid():
            form.save()
            update_change_reason(relationship_type, "Updated relationship type")
            messages.success(request, 'Relationship type updated successfully.')
            return redirect('accounts:relationshiptype_list')
    else:
        form = RelationshipTypeForm(instance=relationship_type)

    return render(request, 'accounts/relationshiptype_form.html', {
        'form': form,
        'title': 'Edit Relationship Type',
        'simple_history': relationship_type.history.all()[:30],
    })


@login_required
@permission_required('accounts.can_delete_relationshiptype', raise_exception=True)
def relationshiptype_delete(request, pk):
    relationship_type = get_object_or_404(RelationshipType, pk=pk)
    if request.method == 'POST':
        relationship_type.delete()
        messages.success(request, 'Relationship type deleted successfully.')
        return redirect('accounts:relationshiptype_list')

    return render(request, 'accounts/relationshiptype_confirm_delete.html', {
        'relationship_type': relationship_type,
        'simple_history': relationship_type.history.all()[:30],
    })


# Invite User View
@login_required
def invite_user_view(request):
    if not request.user.has_perm('accounts.can_generate_invite'):
        messages.error(request, 'You do not have permission to generate invites.')
        return redirect('home')

    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.save()
            history = invitation.history.first()
            if history:
                history.history_user = request.user
                history.history_change_reason = f"Invitation created by {request.user.email}"
                history.save()

            invite_link = request.build_absolute_uri(
                reverse('accounts:register', args=[invitation.token])
            )
            messages.success(request, f'Invitation generated for {invitation.email}. Link: {invite_link}')
            return redirect('accounts:invite_user')
    else:
        form = InvitationForm()

    invitations = Invitation.objects.all()
    return render(request, 'accounts/invite_user.html', {
        'form': form,
        'invitations': invitations,
        'simple_history': [invitation.history.all()[:30] for invitation in invitations],
    })


# Profile Update View
@login_required
def profile_update_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            update_change_reason(user, "Updated profile")
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'accounts/profile_update.html', {
        'form': form,
        'simple_history': user.history.all()[:30],
    })
