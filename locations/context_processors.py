import logging

logger = logging.getLogger(__name__)

def locations_permissions(request):
    permissions = {}

    if request.user.is_authenticated:
        # Defina os modelos e ações de forma programática
        models_permissions = {
            'Building': ['view', 'add', 'change', 'delete'],
            'Room': ['view', 'add', 'change', 'delete'],
            'Measurement': ['view', 'add', 'change', 'delete'],
        }

        # Itera sobre cada modelo e suas ações para gerar permissões
        for model, actions in models_permissions.items():
            for action in actions:
                perm_code = f'locations.{action}_{model.lower()}'
                permissions[f'can_{action}_{model.lower()}'] = request.user.has_perm(perm_code)

        # Log as permissões (apenas para depuração; remova em produção)
        logger.debug(f"Permissions for user {request.user}: {permissions}")

    return {'locations_permissions': permissions}
