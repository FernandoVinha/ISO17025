# ISO17025/accounts/views.py

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import RelationshipType, Companies, Contacts
from .forms import RelationshipTypeForm, CompaniesForm, ContactsForm

# ====== RelationshipType Views ======

# View para listar RelationshipTypes (requer permissão de visualização)
@login_required
@permission_required('accounts.view_relationshiptype', raise_exception=True)
def relationshiptype_list(request):
    relationship_types = RelationshipType.objects.all()
    return render(request, 'accounts/relationshiptype_list.html', {'relationship_types': relationship_types})

# View para criar RelationshipType (requer permissão de criação)
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

# View para editar RelationshipType (requer permissão de edição)
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

# View para excluir RelationshipType (requer permissão de exclusão)
@login_required
@permission_required('accounts.delete_relationshiptype', raise_exception=True)
def relationshiptype_delete(request, pk):
    relationship_type = get_object_or_404(RelationshipType, pk=pk)
    if request.method == 'POST':
        relationship_type.delete()
        messages.success(request, "Relationship Type deleted successfully!")
        return redirect('relationshiptype_list')
    return render(request, 'accounts/relationshiptype_confirm_delete.html', {'relationship_type': relationship_type})


# ====== Companies Views ======

# View para listar Companies (requer permissão de visualização)
@login_required
@permission_required('accounts.view_companies', raise_exception=True)
def companies_list(request):
    companies = Companies.objects.all()
    return render(request, 'accounts/companies_list.html', {'companies': companies})

# View para criar Company (requer permissão de criação)
@login_required
@permission_required('accounts.create_companies', raise_exception=True)
def companies_create(request):
    if request.method == 'POST':
        form = CompaniesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Company created successfully!")
            return redirect('companies_list')
    else:
        form = CompaniesForm()
    return render(request, 'accounts/companies_form.html', {'form': form})

# View para editar Company (requer permissão de edição)
@login_required
@permission_required('accounts.edit_companies', raise_exception=True)
def companies_edit(request, pk):
    company = get_object_or_404(Companies, pk=pk)
    if request.method == 'POST':
        form = CompaniesForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, "Company updated successfully!")
            return redirect('companies_list')
    else:
        form = CompaniesForm(instance=company)
    return render(request, 'accounts/companies_form.html', {'form': form})

# View para excluir Company (requer permissão de exclusão)
@login_required
@permission_required('accounts.delete_companies', raise_exception=True)
def companies_delete(request, pk):
    company = get_object_or_404(Companies, pk=pk)
    if request.method == 'POST':
        company.delete()
        messages.success(request, "Company deleted successfully!")
        return redirect('companies_list')
    return render(request, 'accounts/companies_confirm_delete.html', {'company': company})


# ====== Contacts Views ======

# View para listar Contacts (requer permissão de visualização)
@login_required
@permission_required('accounts.view_contacts', raise_exception=True)
def contacts_list(request):
    contacts = Contacts.objects.all()
    return render(request, 'accounts/contacts_list.html', {'contacts': contacts})

# View para criar Contact (requer permissão de criação)
@login_required
@permission_required('accounts.create_contacts', raise_exception=True)
def contacts_create(request):
    if request.method == 'POST':
        form = ContactsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact created successfully!")
            return redirect('contacts_list')
    else:
        form = ContactsForm()
    return render(request, 'accounts/contacts_form.html', {'form': form})

# View para editar Contact (requer permissão de edição)
@login_required
@permission_required('accounts.edit_contacts', raise_exception=True)
def contacts_edit(request, pk):
    contact = get_object_or_404(Contacts, pk=pk)
    if request.method == 'POST':
        form = ContactsForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact updated successfully!")
            return redirect('contacts_list')
    else:
        form = ContactsForm(instance=contact)
    return render(request, 'accounts/contacts_form.html', {'form': form})

# View para excluir Contact (requer permissão de exclusão)
@login_required
@permission_required('accounts.delete_contacts', raise_exception=True)
def contacts_delete(request, pk):
    contact = get_object_or_404(Contacts, pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, "Contact deleted successfully!")
        return redirect('contacts_list')
    return render(request, 'accounts/contacts_confirm_delete.html', {'contact': contact})
