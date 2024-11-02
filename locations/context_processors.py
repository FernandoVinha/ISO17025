def locations_permissions(request):
    permissions = {}

    if request.user.is_authenticated:
        # Verificar permissões de edifícios
        permissions['can_view_building'] = request.user.has_perm('locations.can_view_building')
        permissions['can_add_building'] = request.user.has_perm('locations.can_add_building')
        permissions['can_change_building'] = request.user.has_perm('locations.can_change_building')
        permissions['can_delete_building'] = request.user.has_perm('locations.can_delete_building')
        
        # Verificar permissões de salas
        permissions['can_view_room'] = request.user.has_perm('locations.can_view_room')
        permissions['can_add_room'] = request.user.has_perm('locations.can_add_room')
        permissions['can_change_room'] = request.user.has_perm('locations.can_change_room')
        permissions['can_delete_room'] = request.user.has_perm('locations.can_delete_room')
        
        # Verificar permissões de medições
        permissions['can_view_measurement'] = request.user.has_perm('locations.can_view_measurement')
        permissions['can_add_measurement'] = request.user.has_perm('locations.can_add_measurement')
        permissions['can_change_measurement'] = request.user.has_perm('locations.can_change_measurement')
        permissions['can_delete_measurement'] = request.user.has_perm('locations.can_delete_measurement')

    return {
        'locations_permissions': permissions
    }
