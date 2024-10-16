from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import RelationshipType, Companies, Contacts, Invitation
from .forms import RelationshipTypeForm, CompaniesForm, ContactsForm, InvitationForm
from django.contrib.auth.forms import AuthenticationForm

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

# ====== Companies Views ======

@login_required
@permission_required('accounts.view_companies', raise_exception=True)
def companies_list(request):
    search_query = request.GET.get('search', '')
    companies = Companies.objects.filter(name__icontains=search_query) if search_query else Companies.objects.all()
    return render(request, 'accounts/companies_list.html', {'companies': companies})

@login_required
@permission_required('accounts.create_companies', raise_exception=True)
def companies_create(request):
    relationship_types = RelationshipType.objects.all()

    if request.method == 'POST':
        form = CompaniesForm(request.POST, request.FILES)  # Include `request.FILES` for file upload
        if form.is_valid():
            form.save()
            messages.success(request, "Company created successfully!")
            return redirect('companies_list')
    else:
        form = CompaniesForm()

    return render(request, 'accounts/companies_form.html', {
        'form': form,
        'relationship_types': relationship_types
    })

@login_required
@permission_required('accounts.edit_companies', raise_exception=True)
def companies_edit(request, pk):
    company = get_object_or_404(Companies, pk=pk)
    relationship_types = RelationshipType.objects.all()

    if request.method == 'POST':
        form = CompaniesForm(request.POST, request.FILES, instance=company)  # Include `request.FILES`
        if form.is_valid():
            form.save()
            messages.success(request, "Company updated successfully!")
            return redirect('companies_list')
    else:
        form = CompaniesForm(instance=company)

    return render(request, 'accounts/companies_form.html', {
        'form': form,
        'company': company,
        'relationship_types': relationship_types
    })

@login_required
@permission_required('accounts.delete_companies', raise_exception=True)
def companies_delete(request, pk):
    company = get_object_or_404(Companies, pk=pk)
    if request.method == 'POST':
        company.delete()
        messages.success(request, "Company deleted successfully!")
        return redirect('companies_list')
    return render(request, 'confirm_delete.html', {
        'item_name': company.name,
        'delete_url': request.path,
        'cancel_url': 'companies_list'
    })

# ====== Contacts Views ======

@login_required
@permission_required('accounts.view_contacts', raise_exception=True)
def contacts_list(request):
    search_query = request.GET.get('search', '')
    contacts = Contacts.objects.filter(name__icontains=search_query) if search_query else Contacts.objects.all()
    return render(request, 'accounts/contacts_list.html', {'contacts': contacts})

@login_required
@permission_required('accounts.create_contacts', raise_exception=True)
def contacts_create(request):
    companies = Companies.objects.all()  # Fetch the list of companies
    if request.method == 'POST':
        form = ContactsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact created successfully!")
            return redirect('contacts_list')
    else:
        form = ContactsForm()
    
    return render(request, 'accounts/contacts_form.html', {
        'form': form,
        'companies': companies,  # Pass the companies list to the template
        'title': 'Add Contact', 
        'button_label': 'Save'
    })

@login_required
@permission_required('accounts.edit_contacts', raise_exception=True)
def contacts_edit(request, pk):
    contact = get_object_or_404(Contacts, pk=pk)
    companies = Companies.objects.all()  # Fetch the list of companies

    if request.method == 'POST':
        form = ContactsForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact updated successfully!")
            return redirect('contacts_list')
    else:
        form = ContactsForm(instance=contact)

    return render(request, 'accounts/contacts_form.html', {
        'form': form,
        'companies': companies,  # Pass the companies list to the template
        'contact': contact,
        'title': 'Edit Contact', 
        'button_label': 'Update'
    })

@login_required
@permission_required('accounts.delete_contacts', raise_exception=True)
def contacts_delete(request, pk):
    contact = get_object_or_404(Contacts, pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, "Contact deleted successfully!")
        return redirect('contacts_list')
    return render(request, 'confirm_delete.html', {
        'item_name': contact.name,
        'delete_url': request.path,
        'cancel_url': 'contacts_list'
    })

# Home page view
@login_required
def home_view(request):
    return render(request, 'home.html')
