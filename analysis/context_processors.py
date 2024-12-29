#analysis/context_processors.py
def analysis_permissions(request):
    permissions = {}

    if request.user.is_authenticated:
        models_permissions = {
            'AnalysisRequest': ['view', 'add', 'change', 'delete'],
            'ReceptionItem': ['view', 'add', 'change', 'delete'],
            'Analysis': ['view', 'add', 'change', 'delete', 'approve'],
            'AnalysisApproval': ['view', 'add', 'change', 'delete'],
            'Disposal': ['view', 'add', 'change', 'delete'],
        }

        for model, actions in models_permissions.items():
            for action in actions:
                perm_code = f'analysis.{action}_{model.lower()}'
                permissions[f'can_{action}_{model.lower()}'] = request.user.has_perm(perm_code)

    return {'analysis_permissions': permissions}
