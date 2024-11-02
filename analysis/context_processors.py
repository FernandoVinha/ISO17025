def analysis_permissions(request):
    permissions = {}

    if request.user.is_authenticated:
        # Lista de modelos e suas permissões
        models_permissions = {
            'AnalysisRequest': ['view', 'add', 'change', 'delete'],
            'ReceptionItem': ['view', 'add', 'change', 'delete'],
            'Analysis': ['view', 'add', 'change', 'delete', 'approve'],  # Inclui permissão de aprovação
            'AnalysisApproval': ['view', 'add', 'change', 'delete'],
            'Disposal': ['view', 'add', 'change', 'delete'],
        }

        # Itera sobre cada modelo e verifica as permissões
        for model, actions in models_permissions.items():
            for action in actions:
                perm_code = f'analysis.can_{action}_{model.lower()}'
                permissions[f'can_{action}_{model.lower()}'] = request.user.has_perm(perm_code)

    return {
        'analysis_permissions': permissions
    }
