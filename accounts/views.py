from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import RelationshipType, Invitation
from .forms import RelationshipTypeForm, InvitationForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, ProfileUpdateForm

# ====== Login and Logout Views ======

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirects authenticated users to the home page

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

# Logout view
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Redirects to the login page after logout

# ====== Invitation View ======

@login_required
@permission_required('accounts.can_generate_invite', raise_exception=True)
def invite_user_view(request):
    invite_link = None
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.save()
            # Generate invite link using the token
            invite_link = request.build_absolute_uri(
                reverse('register', args=[invitation.token])
            )
            messages.success(request, f"Invitation successfully generated for {invitation.email}!")
    else:
        form = InvitationForm()

    return render(request, 'accounts/invite_user.html', {'form': form, 'invite_link': invite_link})

# ====== RelationshipType Views ======

@login_required
@permission_required('accounts.view_relationshiptype', raise_exception=True)
def relationshiptype_list(request):
    relationship_types = RelationshipType.objects.all()
    return render(request, 'accounts/relationshiptype_list.html', {'relationship_types': relationship_types})

@login_required
@permission_required('accounts.create_relationshiptype', raise_exception=True)
def relationshiptype_create(request):
    if request.method == 'POST':
        form = RelationshipTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Relationship Type created successfully!")
            return redirect('relationshiptype_list')
    else:
        form = RelationshipTypeForm()
    return render(request, 'accounts/relationshiptype_form.html', {'form': form})

@login_required
@permission_required('accounts.edit_relationshiptype', raise_exception=True)
def relationshiptype_edit(request, pk):
    relationship_type = get_object_or_404(RelationshipType, pk=pk)
    if request.method == 'POST':
        form = RelationshipTypeForm(request.POST, instance=relationship_type)
        if form.is_valid():
            form.save()
            messages.success(request, "Relationship Type updated successfully!")
            return redirect('relationshiptype_list')
    else:
        form = RelationshipTypeForm(instance=relationship_type)
    return render(request, 'accounts/relationshiptype_form.html', {'form': form})

@login_required
@permission_required('accounts.delete_relationshiptype', raise_exception=True)
def relationshiptype_delete(request, pk):
    relationship_type = get_object_or_404(RelationshipType, pk=pk)
    if request.method == 'POST':
        relationship_type.delete()
        messages.success(request, "Relationship Type deleted successfully!")
        return redirect('relationshiptype_list')
    return render(request, 'confirm_delete.html', {
        'item_name': relationship_type.name,
        'delete_url': request.path,
        'cancel_url': 'relationshiptype_list'
    })

# Home page view
def home_view(request):
    return render(request, 'home.html')

# ====== Registration and Profile Views ======

def register_view(request, token):
    try:
        # Verifica se o token de convite é válido
        invitation = Invitation.objects.get(token=token)
    except Invitation.DoesNotExist:
        messages.error(request, "Invalid or expired invitation token.")
        return redirect('login')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = invitation.email  # Associa o email do convite ao usuário
            user.role = 'employee'  # Define o valor padrão para 'role'
            user.save()
            login(request, user)  # Autentica o usuário automaticamente após o registro
            messages.success(request, f"Welcome, {user.first_name}! Your account has been created.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form, 'token': token})

@login_required
def profile_update_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')  # Redireciona para a página de perfil
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/profile_update.html', {'form': form})
