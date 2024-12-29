# accounts/context_processors.py

from django.conf import settings

def user_permissions(request):
    permissions = {}

    if request.user.is_authenticated:
        # Defina explicitamente as permissões personalizadas
        custom_permissions = [
            'can_view_accounts',
            'can_add_account',
            'can_change_account',
            'can_delete_account',
            'can_view_companies',
            'can_view_contacts',
            'can_view_relationshiptype',
            'can_view_profile',
            'can_generate_invite',
            # Adicione outras permissões personalizadas conforme necessário
        ]

        for perm in custom_permissions:
            permissions[perm] = request.user.has_perm(f'accounts.{perm}')

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
