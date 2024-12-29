# inventory/context_processors.py

def inventory_permissions(request):
    permissions = {}

    if request.user.is_authenticated:
        # Defina as permissões de forma dinâmica
        models_permissions = {
            'InventoryItem': ['view', 'add', 'change', 'delete'],
        }

        # Itera sobre cada modelo e suas ações para gerar permissões
        for model, actions in models_permissions.items():
            for action in actions:
                perm_code = f'inventory.{action}_{model.lower()}'
                permissions[f'can_{action}_{model.lower()}'] = request.user.has_perm(perm_code)

    return {'inventory_permissions': permissions}
