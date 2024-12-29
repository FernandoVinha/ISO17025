# maintenance/context_processors.py

def maintenance_permissions(request):
    permissions = {}

    if request.user.is_authenticated:
        # Define modelos e ações de forma programática
        models_permissions = {
            'Maintenance': ['view', 'add', 'change', 'delete'],
            'Calibration': ['view', 'add', 'change', 'delete'],
            'CalibrationStandard': ['view', 'add', 'change', 'delete'],
            'Training': ['view', 'add', 'change', 'delete'],
            'StandardOperatingProcedure': ['view', 'add', 'change', 'delete'],
            'DailyVerification': ['view', 'add', 'change', 'delete'],
        }

        # Mapeamento de nomes de modelos para abreviações ou formatos específicos
        model_short_names = {
            'StandardOperatingProcedure': 'sop',
            'DailyVerification': 'dailyverification',  # Ajuste conforme a nomenclatura desejada
            # Adicione outros mapeamentos conforme necessário
        }

        # Itera sobre cada modelo e suas ações para gerar permissões
        for model, actions in models_permissions.items():
            model_key = model_short_names.get(model, model.lower())
            for action in actions:
                perm_code = f'maintenance.{action}_{model_key}'
                permissions[f'can_{action}_{model_key}'] = request.user.has_perm(perm_code)

    return {'maintenance_permissions': permissions}
