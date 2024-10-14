# accounts/context_processors.py
from django.contrib.auth.models import Permission
from django.conf import settings

def user_permissions(request):
    permissions = {}

    if request.user.is_authenticated:
        # Permissões existentes
        permissions['can_access_samplereception'] = request.user.has_perm('app_label.can_access_samplereception')
        permissions['can_access_samplestorage'] = request.user.has_perm('app_label.can_access_samplestorage')
        permissions['can_access_sampleanalysis'] = request.user.has_perm('app_label.can_access_sampleanalysis')
        permissions['can_access_analysisreport'] = request.user.has_perm('app_label.can_access_analysisreport')
        permissions['can_view_companies'] = request.user.has_perm('accounts.view_companies')
        permissions['can_view_contacts'] = request.user.has_perm('accounts.view_contacts')
        permissions['can_generate_invite'] = request.user.has_perm('accounts.can_generate_invite')

        # Novas permissões para Locations
        permissions['can_view_building'] = request.user.has_perm('locations.view_building')
        permissions['can_view_room'] = request.user.has_perm('locations.view_room')
        permissions['can_view_measurement'] = request.user.has_perm('locations.view_measurement')
        # Adicione outras permissões de Locations conforme necessário

    # Informações do usuário
    user_info = {
        'full_name': request.user.get_full_name(),
        'email': request.user.email,
        'role': getattr(request.user, 'role', None),
    } if request.user.is_authenticated else {}

    # Informações do projeto
    project_info = {
        'project_name': getattr(settings, 'PROJECT_NAME', 'ISO17025 Project'),
        'contact_email': getattr(settings, 'CONTACT_EMAIL', 'contact@example.com'),
        'support_phone': getattr(settings, 'SUPPORT_PHONE', '+1 (555) 555-5555'),
        'address': getattr(settings, 'ADDRESS', '1234 Main St, Anytown, USA'),
        'social_links': {
            'facebook': getattr(settings, 'FACEBOOK_URL', 'https://facebook.com'),
            'twitter': getattr(settings, 'TWITTER_URL', 'https://twitter.com'),
            'linkedin': getattr(settings, 'LINKEDIN_URL', 'https://linkedin.com'),
        }
    }

    return {
        'permissions': permissions,
        'user_info': user_info,
        'project_info': project_info,
    }
