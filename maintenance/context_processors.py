# maintenance/context_processors.py

def maintenance_permissions(request):
    permissions = {}

    if request.user.is_authenticated:
        permissions['can_view_maintenance'] = request.user.has_perm('maintenance.can_view_maintenance')
        permissions['can_add_maintenance'] = request.user.has_perm('maintenance.can_add_maintenance')
        permissions['can_change_maintenance'] = request.user.has_perm('maintenance.can_change_maintenance')
        permissions['can_delete_maintenance'] = request.user.has_perm('maintenance.can_delete_maintenance')
        permissions['can_view_calibration'] = request.user.has_perm('maintenance.can_view_calibration')
        permissions['can_add_calibration'] = request.user.has_perm('maintenance.can_add_calibration')
        permissions['can_change_calibration'] = request.user.has_perm('maintenance.can_change_calibration')
        permissions['can_delete_calibration'] = request.user.has_perm('maintenance.can_delete_calibration')
        permissions['can_view_calibrationstandard'] = request.user.has_perm('maintenance.can_view_calibrationstandard')
        permissions['can_add_calibrationstandard'] = request.user.has_perm('maintenance.can_add_calibrationstandard')
        permissions['can_change_calibrationstandard'] = request.user.has_perm('maintenance.can_change_calibrationstandard')
        permissions['can_delete_calibrationstandard'] = request.user.has_perm('maintenance.can_delete_calibrationstandard')

    return {
        'maintenance_permissions': permissions
    }
