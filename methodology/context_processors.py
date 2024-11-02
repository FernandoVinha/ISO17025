from django.apps import apps

def methodology_permissions(request):
    permissions = {}

    if request.user.is_authenticated:
        # Verificar permissões de metodologias
        permissions['can_view_methodology'] = request.user.has_perm('methodology.can_view_methodology')
        permissions['can_add_methodology'] = request.user.has_perm('methodology.can_add_methodology')
        permissions['can_change_methodology'] = request.user.has_perm('methodology.can_change_methodology')
        permissions['can_delete_methodology'] = request.user.has_perm('methodology.can_delete_methodology')
        
        # Verificar permissões de insumos de metodologias
        permissions['can_view_methodology_supply'] = request.user.has_perm('methodology.can_view_methodology_supply')

    return {
        'methodology_permissions': permissions
    }
