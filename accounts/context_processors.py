# accounts/context_processors.py

from django.apps import apps
from django.conf import settings

def user_permissions(request):
    permissions = {}

    if request.user.is_authenticated:
        # Itera sobre todos os apps instalados
        for app_config in apps.get_app_configs():
            app_label = app_config.label
            # Adiciona permissões específicas para cada app no contexto
            permissions[f'can_view_{app_label}'] = request.user.has_perm(f'{app_label}.view_{app_label}')
            permissions[f'can_add_{app_label}'] = request.user.has_perm(f'{app_label}.add_{app_label}')
            permissions[f'can_change_{app_label}'] = request.user.has_perm(f'{app_label}.change_{app_label}')
            permissions[f'can_delete_{app_label}'] = request.user.has_perm(f'{app_label}.delete_{app_label}')

    # Informações do usuário logado
    user_info = {
        'full_name': request.user.get_full_name(),
        'email': request.user.email,
        'role': getattr(request.user, 'role', None),
    } if request.user.is_authenticated else {}

    # Informações sobre o projeto
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
