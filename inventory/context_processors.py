def inventory_permissions(request):
    permissions = {}

    if request.user.is_authenticated:
        # Verificar permissões de itens de inventário
        permissions['can_view_inventoryitem'] = request.user.has_perm('inventory.can_view_inventoryitem')
        permissions['can_add_inventoryitem'] = request.user.has_perm('inventory.can_add_inventoryitem')
        permissions['can_change_inventoryitem'] = request.user.has_perm('inventory.can_change_inventoryitem')
        permissions['can_delete_inventoryitem'] = request.user.has_perm('inventory.can_delete_inventoryitem')

    return {
        'inventory_permissions': permissions
    }
