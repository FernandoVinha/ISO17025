# inventory/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import JsonResponse
from .models import InventoryItem
from .forms import InventoryItemForm
from .filters import InventoryItemFilter
from simple_history.utils import update_change_reason

# ====== InventoryItem Views ======

@login_required
@permission_required('inventory.can_view_inventoryitem', raise_exception=True)
def inventoryitem_list(request):
    """
    Exibe uma lista paginada de InventoryItems com funcionalidade de filtro.
    """
    inventory_items = InventoryItem.objects.all()

    # Aplicar filtros
    inventory_filter = InventoryItemFilter(request.GET, queryset=inventory_items)
    inventory_items = inventory_filter.qs

    # Ordenar itens por data de expiração (itens sem data de expiração aparecem no final)
    inventory_items = inventory_items.order_by('expiration_date')

    # Paginar os itens de inventário
    paginator = Paginator(inventory_items, 50)  # 50 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/inventoryitem_list.html', {
        'inventory_items': page_obj,
        'filter': inventory_filter,
        'page_obj': page_obj,
        # Evitar passar o histórico diretamente para o template para otimizar performance
    })


@login_required
@permission_required('inventory.can_add_inventoryitem', raise_exception=True)
def inventoryitem_create(request):
    """
    Trata a criação de um novo InventoryItem.
    O botão de exclusão não estará disponível nesta view.
    """
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES)
        if form.is_valid():
            inventory_item = form.save()
            update_change_reason(inventory_item, f"Item adicionado por {request.user.get_full_name()}")
            messages.success(request, "Inventory item criado com sucesso!")
            return redirect('inventory:inventoryitem_list')  # URL com namespace correto
    else:
        form = InventoryItemForm()

    return render(request, 'inventory/inventoryitem_form.html', {
        'form': form,
        'title': 'Adicionar Inventory Item',
        'button_label': 'Salvar',
        'inventory_item': None,  # Indicando criação
    })


@login_required
@permission_required('inventory.can_change_inventoryitem', raise_exception=True)
def inventoryitem_edit(request, pk):
    """
    Trata a edição de um InventoryItem existente.
    O botão de exclusão estará disponível nesta view.
    """
    inventory_item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES, instance=inventory_item)
        if form.is_valid():
            form.save()
            update_change_reason(inventory_item, f"Item atualizado por {request.user.get_full_name()}")
            messages.success(request, "Inventory item atualizado com sucesso!")
            return redirect('inventory:inventoryitem_list')  # URL com namespace correto
    else:
        form = InventoryItemForm(instance=inventory_item)

    return render(request, 'inventory/inventoryitem_form.html', {
        'form': form,
        'inventory_item': inventory_item,
        'title': 'Editar Inventory Item',
        'button_label': 'Atualizar',
        'simple_history': inventory_item.history.all()[:30],  # Exibe o histórico (opcional)
    })


@login_required
@permission_required('inventory.can_delete_inventoryitem', raise_exception=True)
def inventoryitem_delete(request, pk):
    """
    Trata a exclusão de um InventoryItem existente.
    """
    inventory_item = get_object_or_404(InventoryItem, pk=pk)

    if request.method == 'POST':
        update_change_reason(inventory_item, f"Item deletado por {request.user.get_full_name()}")
        inventory_item.delete()
        messages.success(request, "Inventory item deletado com sucesso!")
        return redirect('inventory:inventoryitem_list')  # Redireciona para a lista após a exclusão

    return render(request, 'confirm_delete.html', {
        'item_name': inventory_item.name,
        'delete_url': reverse('inventory:inventoryitem_delete', args=[inventory_item.id]),
        'cancel_url': reverse('inventory:inventoryitem_list'),
        'simple_history': inventory_item.history.all()[:30],  # Exibe o histórico (opcional)
    })
