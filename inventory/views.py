from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import InventoryItem
from .forms import InventoryItemForm
from .filters import InventoryItemFilter

# ====== InventoryItem Views ======

@login_required
@permission_required('locations.view_inventoryitem', raise_exception=True)
def inventoryitem_list(request):
    """
    Display a list of all inventory items with optional search and filter functionality.
    Items with expiration dates are listed first, followed by those without.
    """
    inventory_items = InventoryItem.objects.all()
    
    # Aplicar filtros
    inventory_filter = InventoryItemFilter(request.GET, queryset=inventory_items)
    inventory_items = inventory_filter.qs

    # Ordenar os itens: primeiros com data de validade e depois os sem
    inventory_items = sorted(inventory_items, key=lambda x: (x.expiration_date is None, x.expiration_date))

    return render(request, 'inventory/inventoryitem_list.html', {
        'inventory_items': inventory_items,
        'filter': inventory_filter,
    })

@login_required
@permission_required('locations.add_inventoryitem', raise_exception=True)
def inventoryitem_create(request):
    """
    Handle the creation of a new inventory item.
    """
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Inventory item created successfully!")
            return redirect('inventoryitem_list')
    else:
        form = InventoryItemForm()
    return render(request, 'inventory/inventoryitem_form.html', {
        'form': form,
        'title': 'Add Inventory Item',
        'button_label': 'Save'
    })

@login_required
@permission_required('locations.change_inventoryitem', raise_exception=True)
def inventoryitem_edit(request, pk):
    """
    Handle the editing of an existing inventory item.
    """
    inventory_item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES, instance=inventory_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Inventory item updated successfully!")
            return redirect('inventoryitem_list')
    else:
        form = InventoryItemForm(instance=inventory_item)
    return render(request, 'inventory/inventoryitem_form.html', {
        'form': form,
        'inventory_item': inventory_item,
        'title': 'Edit Inventory Item',
        'button_label': 'Update'
    })

@login_required
@permission_required('locations.delete_inventoryitem', raise_exception=True)
def inventoryitem_delete(request, pk):
    """
    Handle the deletion of an existing inventory item.
    """
    inventory_item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        inventory_item.delete()
        messages.success(request, "Inventory item deleted successfully!")
        return redirect('inventoryitem_list')
    return render(request, 'confirm_delete.html', {
        'item_name': inventory_item.name,
        'delete_url': request.path,
        'cancel_url': 'inventoryitem_list'
    })
